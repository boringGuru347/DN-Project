"""
feature_selection.py — ANOVA F-score feature selection (SelectKBest).

Steps:
  1. Load preprocessed (scaled) training and testing arrays from disk.
  2. Sweep k ∈ FEATURE_SWEEP_RANGE to understand the accuracy vs. features
     trade-off (used for Graph 4).
  3. Select the working k = SELECTED_K features using SelectKBest fitted on
     the training data only.
  4. Save the selected feature arrays and the fitted selector to disk.

The selector is fitted exclusively on the training split to prevent leakage.
"""

import os
import sys
import numpy as np
import joblib
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    PROCESSED_TRAIN_X, PROCESSED_TRAIN_Y,
    PROCESSED_TEST_X,  PROCESSED_TEST_Y,
    SELECTED_TRAIN_X, SELECTED_TEST_X,
    SELECTOR_PATH, FEATURE_SWEEP_PATH,
    SELECTED_K, FEATURE_SWEEP_RANGE,
    RANDOM_SEED, DATA_PROCESSED_DIR,
    get_logger, ensure_dirs, save_json,
)

log = get_logger("feature_selection")


# ---------------------------------------------------------------------------
# Feature sweep — evaluate a lightweight SVM across multiple k values
# ---------------------------------------------------------------------------
def feature_sweep(X_train: np.ndarray, y_train: np.ndarray,
                  X_test: np.ndarray,  y_test: np.ndarray) -> dict:
    """
    Train a quick LinearSVC at each k in FEATURE_SWEEP_RANGE.
    Returns a dict mapping k → {accuracy, f1}.

    NOTE: We use a LinearSVC (faster) for the sweep only.
    The main experiment uses RBF SVM with the selected SELECTED_K features.
    This sweep is purely for the feature-reduction graph (Graph 4).
    """
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import Pipeline

    results = {}
    log.info("Starting feature sweep over k = %s", FEATURE_SWEEP_RANGE)
    for k in FEATURE_SWEEP_RANGE:
        selector = SelectKBest(f_classif, k=k)
        X_tr_k = selector.fit_transform(X_train, y_train)
        X_te_k = selector.transform(X_test)

        # Quick LinearSVC for sweep speed
        clf = LinearSVC(C=1.0, max_iter=2000, random_state=RANDOM_SEED)
        clf.fit(X_tr_k, y_train)
        y_pred = clf.predict(X_te_k)

        acc = float(accuracy_score(y_test, y_pred))
        f1  = float(f1_score(y_test, y_pred, average="binary"))
        results[k] = {"accuracy": acc, "f1": f1}
        log.info("  k=%2d  |  accuracy=%.4f  |  f1=%.4f", k, acc, f1)

    return results


# ---------------------------------------------------------------------------
# Main feature selection using SELECTED_K
# ---------------------------------------------------------------------------
def select_features(X_train: np.ndarray, y_train: np.ndarray,
                    X_test: np.ndarray, k: int):
    """
    Fit SelectKBest (f_classif) on training data and transform both splits.
    Returns reduced X_train, X_test and the fitted selector.
    """
    log.info("Fitting SelectKBest (k=%d) on training data...", k)
    selector = SelectKBest(f_classif, k=k)
    X_train_sel = selector.fit_transform(X_train, y_train)
    X_test_sel  = selector.transform(X_test)

    # Report which features were selected (indices)
    selected_indices = selector.get_support(indices=True)
    log.info("Selected feature indices: %s", selected_indices.tolist())
    log.info("Reduced feature count: %d → %d", X_train.shape[1], k)

    return X_train_sel.astype(np.float32), X_test_sel.astype(np.float32), selector


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------
def run_feature_selection():
    ensure_dirs()

    # Load preprocessed data
    X_train = np.load(PROCESSED_TRAIN_X)
    y_train = np.load(PROCESSED_TRAIN_Y)
    X_test  = np.load(PROCESSED_TEST_X)
    y_test  = np.load(PROCESSED_TEST_Y)

    log.info("Loaded preprocessed data. Shapes — X_train: %s, X_test: %s",
             X_train.shape, X_test.shape)

    # Feature sweep (for Graph 4)
    sweep_results = feature_sweep(X_train, y_train, X_test, y_test)
    save_json({str(k): v for k, v in sweep_results.items()}, FEATURE_SWEEP_PATH)
    log.info("Feature sweep results saved to: %s", FEATURE_SWEEP_PATH)

    # Select working k for main experiment
    X_train_sel, X_test_sel, selector = select_features(
        X_train, y_train, X_test, k=SELECTED_K
    )

    # Save
    np.save(SELECTED_TRAIN_X, X_train_sel)
    np.save(SELECTED_TEST_X,  X_test_sel)
    joblib.dump(selector, SELECTOR_PATH)

    log.info("Selected feature arrays saved to: %s", DATA_PROCESSED_DIR)
    log.info("Selector saved to: %s", SELECTOR_PATH)
    log.info("Feature selection complete. Using %d features for main experiment.", SELECTED_K)

    return X_train_sel, y_train, X_test_sel, y_test


if __name__ == "__main__":
    run_feature_selection()
