"""
preprocessing.py — Data loading, cleaning, encoding and scaling for UNSW-NB15.

Pipeline:
  1. Load the pre-defined train/test CSVs.
  2. Drop identifier and multi-class columns (id, attack_cat).
  3. Handle missing and infinite values.
  4. Label-encode categorical columns (proto, service, state).
  5. Separate features (X) from binary target (y).
  6. Fit StandardScaler on training data only; apply to both splits.
  7. Save scaled arrays and the fitted scaler to disk.

All transformations that depend on statistics (mean, std, encoder mappings)
are fitted exclusively on the training set to avoid data leakage.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Allow running this script directly from the project root or from src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    TRAIN_CSV, TEST_CSV,
    PROCESSED_TRAIN_X, PROCESSED_TRAIN_Y,
    PROCESSED_TEST_X, PROCESSED_TEST_Y,
    SCALER_PATH,
    COLUMNS_TO_DROP, TARGET_COLUMN, CATEGORICAL_COLUMNS,
    DATA_PROCESSED_DIR, MODELS_DIR,
    get_logger, ensure_dirs,
)

log = get_logger("preprocessing")


# ---------------------------------------------------------------------------
# Step 1 — Load CSVs
# ---------------------------------------------------------------------------
def load_raw_data(train_path: str, test_path: str):
    """Load the UNSW-NB15 training and testing CSV files."""
    log.info("Loading training CSV: %s", train_path)
    if not os.path.isfile(train_path):
        raise FileNotFoundError(
            f"\n\n[ERROR] Training CSV not found at:\n  {train_path}\n"
            "Please download UNSW_NB15_training-set.csv and place it in data/raw/\n"
            "See data/dataset_instructions.md for download instructions.\n"
        )
    if not os.path.isfile(test_path):
        raise FileNotFoundError(
            f"\n\n[ERROR] Testing CSV not found at:\n  {test_path}\n"
            "Please download UNSW_NB15_testing-set.csv and place it in data/raw/\n"
            "See data/dataset_instructions.md for download instructions.\n"
        )

    df_train = pd.read_csv(train_path, low_memory=False)
    df_test  = pd.read_csv(test_path,  low_memory=False)

    log.info("Training set shape: %s", df_train.shape)
    log.info("Testing  set shape: %s", df_test.shape)
    return df_train, df_test


# ---------------------------------------------------------------------------
# Step 2 — Drop irrelevant columns
# ---------------------------------------------------------------------------
def drop_irrelevant_columns(df: pd.DataFrame, cols_to_drop: list) -> pd.DataFrame:
    """Drop columns that are identifiers or not needed for binary classification."""
    present = [c for c in cols_to_drop if c in df.columns]
    if present:
        log.info("Dropping columns: %s", present)
        df = df.drop(columns=present)
    return df


# ---------------------------------------------------------------------------
# Step 3 — Handle missing and infinite values
# ---------------------------------------------------------------------------
def handle_missing_and_inf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace infinite values with NaN, then fill NaN with column median
    (computed from the same frame — caller must ensure only train stats
    are used across train/test).
    """
    n_inf = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
    n_nan = df.isnull().sum().sum()
    if n_inf > 0:
        log.warning("Found %d infinite value(s) — replacing with NaN", n_inf)
    if n_nan > 0:
        log.warning("Found %d NaN value(s) — filling with column median", n_nan)

    # Replace inf
    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def fill_missing_with_median(df_train: pd.DataFrame, df_test: pd.DataFrame):
    """
    Compute medians from the training set and fill NaNs in both splits.
    Numeric columns only — categorical handled separately.
    """
    numeric_cols = df_train.select_dtypes(include=[np.number]).columns.tolist()
    # Exclude the target column from median imputation
    if TARGET_COLUMN in numeric_cols:
        numeric_cols.remove(TARGET_COLUMN)

    medians = df_train[numeric_cols].median()
    df_train[numeric_cols] = df_train[numeric_cols].fillna(medians)
    df_test[numeric_cols]  = df_test[numeric_cols].fillna(medians)
    return df_train, df_test


# ---------------------------------------------------------------------------
# Step 4 — Encode categorical columns
# ---------------------------------------------------------------------------
def encode_categoricals(df_train: pd.DataFrame, df_test: pd.DataFrame,
                        cat_cols: list):
    """
    Fit LabelEncoder on training data; apply to both splits.
    Unknown categories in test set are mapped to a special integer
    (len(encoder.classes_)) to avoid KeyError.
    """
    encoders = {}
    for col in cat_cols:
        if col not in df_train.columns:
            log.warning("Categorical column '%s' not found — skipping", col)
            continue
        le = LabelEncoder()
        le.fit(df_train[col].astype(str))
        known_classes = set(le.classes_)

        def safe_transform(series, encoder=le, known=known_classes):
            # Map unknown labels to a new integer = len(classes)
            s = series.astype(str).map(
                lambda x: x if x in known else "__unknown__"
            )
            # Add __unknown__ to encoder if needed
            if "__unknown__" not in known:
                import numpy as _np
                encoder.classes_ = _np.append(encoder.classes_, "__unknown__")
            return encoder.transform(s)

        df_train[col] = le.transform(df_train[col].astype(str))
        df_test[col]  = safe_transform(df_test[col])
        encoders[col] = le
        log.info("Encoded categorical column '%s' (%d unique train values)",
                 col, len(le.classes_))
    return df_train, df_test, encoders


# ---------------------------------------------------------------------------
# Step 5 — Separate features and target
# ---------------------------------------------------------------------------
def split_features_labels(df: pd.DataFrame):
    """Return (X, y) as numpy arrays."""
    y = df[TARGET_COLUMN].values.astype(np.int32)
    X = df.drop(columns=[TARGET_COLUMN]).values.astype(np.float32)
    return X, y


# ---------------------------------------------------------------------------
# Step 6 — Feature scaling
# ---------------------------------------------------------------------------
def scale_features(X_train: np.ndarray, X_test: np.ndarray):
    """
    Fit StandardScaler on X_train only.
    Apply the same (fitted) scaler to X_test.
    Returns scaled arrays and the fitted scaler object.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    log.info("Feature scaling applied. Feature means (train): min=%.4f, max=%.4f",
             X_train_scaled.mean(axis=0).min(),
             X_train_scaled.mean(axis=0).max())
    return X_train_scaled.astype(np.float32), X_test_scaled.astype(np.float32), scaler


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_preprocessing():
    ensure_dirs()

    # 1. Load
    df_train, df_test = load_raw_data(TRAIN_CSV, TEST_CSV)

    # Report original feature count (before dropping targets/identifiers)
    log.info("Original columns in dataset: %d", df_train.shape[1])

    # 2. Drop irrelevant columns
    df_train = drop_irrelevant_columns(df_train, COLUMNS_TO_DROP)
    df_test  = drop_irrelevant_columns(df_test,  COLUMNS_TO_DROP)

    # 3. Handle missing and infinite values (inspect before filling)
    df_train = handle_missing_and_inf(df_train)
    df_test  = handle_missing_and_inf(df_test)

    # 4. Fill NaN using training medians only
    df_train, df_test = fill_missing_with_median(df_train, df_test)

    # 5. Encode categoricals (fitted on train only)
    df_train, df_test, _encoders = encode_categoricals(
        df_train, df_test, CATEGORICAL_COLUMNS
    )

    # 6. Separate features and labels
    X_train, y_train = split_features_labels(df_train)
    X_test,  y_test  = split_features_labels(df_test)

    log.info("Feature matrix shape — Train: %s, Test: %s",
             X_train.shape, X_test.shape)
    log.info("Label distribution — Train: Normal=%d, Attack=%d",
             int((y_train == 0).sum()), int((y_train == 1).sum()))
    log.info("Label distribution — Test:  Normal=%d, Attack=%d",
             int((y_test == 0).sum()), int((y_test == 1).sum()))

    # 7. Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # 8. Save to disk
    np.save(PROCESSED_TRAIN_X, X_train_scaled)
    np.save(PROCESSED_TRAIN_Y, y_train)
    np.save(PROCESSED_TEST_X,  X_test_scaled)
    np.save(PROCESSED_TEST_Y,  y_test)
    joblib.dump(scaler, SCALER_PATH)

    log.info("Preprocessed data saved to: %s", DATA_PROCESSED_DIR)
    log.info("Scaler saved to: %s", SCALER_PATH)
    log.info("Preprocessing complete. Feature count (before selection): %d", X_train_scaled.shape[1])

    return X_train_scaled, y_train, X_test_scaled, y_test


if __name__ == "__main__":
    run_preprocessing()
