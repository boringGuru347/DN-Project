"""
utils.py — Shared constants, paths, and helpers.

All other scripts import from this module to ensure consistency across the
entire experimental pipeline.
"""

import os
import json
import logging

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Resolve project root relative to this file's location (src/)
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(_SRC_DIR)

DATA_RAW_DIR       = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
RESULTS_DIR        = os.path.join(PROJECT_ROOT, "results")
MODELS_DIR         = os.path.join(PROJECT_ROOT, "results", "models")
CM_DIR             = os.path.join(PROJECT_ROOT, "results", "confusion_matrices")
GRAPHS_DIR         = os.path.join(PROJECT_ROOT, "graphs")
DIAGRAMS_DIR       = os.path.join(PROJECT_ROOT, "diagrams")

# UNSW-NB15 CSV filenames (place these in data/raw/)
TRAIN_CSV = os.path.join(DATA_RAW_DIR, "UNSW_NB15_training-set.csv")
TEST_CSV  = os.path.join(DATA_RAW_DIR, "UNSW_NB15_testing-set.csv")

# Processed numpy arrays saved as .npy
PROCESSED_TRAIN_X = os.path.join(DATA_PROCESSED_DIR, "X_train.npy")
PROCESSED_TRAIN_Y = os.path.join(DATA_PROCESSED_DIR, "y_train.npy")
PROCESSED_TEST_X  = os.path.join(DATA_PROCESSED_DIR, "X_test.npy")
PROCESSED_TEST_Y  = os.path.join(DATA_PROCESSED_DIR, "y_test.npy")

# Feature-selected arrays
SELECTED_TRAIN_X  = os.path.join(DATA_PROCESSED_DIR, "X_train_selected.npy")
SELECTED_TEST_X   = os.path.join(DATA_PROCESSED_DIR, "X_test_selected.npy")

# Scaler and selector
SCALER_PATH   = os.path.join(MODELS_DIR, "scaler.joblib")
SELECTOR_PATH = os.path.join(MODELS_DIR, "feature_selector.joblib")

# Model save paths
CNN_MODEL_PATH         = os.path.join(MODELS_DIR, "cnn_model.keras")
SVM_MODEL_PATH         = os.path.join(MODELS_DIR, "svm_model.joblib")
CNN_EXTRACTOR_PATH     = os.path.join(MODELS_DIR, "cnn_extractor.keras")
CNN_SVM_MODEL_PATH     = os.path.join(MODELS_DIR, "cnn_svm_classifier.joblib")
CNN_HISTORY_PATH       = os.path.join(MODELS_DIR, "cnn_training_history.json")
FEATURE_SWEEP_PATH     = os.path.join(RESULTS_DIR, "feature_sweep.json")

# Results
METRICS_CSV     = os.path.join(RESULTS_DIR, "metrics.csv")
COMPARISON_CSV  = os.path.join(RESULTS_DIR, "model_comparison.csv")

# ---------------------------------------------------------------------------
# Dataset configuration
# ---------------------------------------------------------------------------
# Columns to drop — not useful as features
COLUMNS_TO_DROP = ["id", "attack_cat"]
TARGET_COLUMN   = "label"

# Categorical columns in UNSW-NB15 that need encoding
CATEGORICAL_COLUMNS = ["proto", "service", "state"]

# Number of features to select for the main experiment
SELECTED_K = 20

# Feature sweep range (for Graph 4)
FEATURE_SWEEP_RANGE = [10, 15, 20, 25, 30, 35]

# Class names for visualisation
CLASS_NAMES = ["Normal", "Attack"]

# ---------------------------------------------------------------------------
# Directory creation helper
# ---------------------------------------------------------------------------
def ensure_dirs():
    """Create all necessary output directories if they don't exist."""
    dirs = [
        DATA_RAW_DIR,
        DATA_PROCESSED_DIR,
        RESULTS_DIR,
        MODELS_DIR,
        CM_DIR,
        GRAPHS_DIR,
        DIAGRAMS_DIR,
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# Logging helper
# ---------------------------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """Return a consistently formatted logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger(name)

# ---------------------------------------------------------------------------
# JSON save/load helpers
# ---------------------------------------------------------------------------
def save_json(data: dict, path: str):
    """Save a dictionary to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path: str) -> dict:
    """Load a JSON file as a dictionary."""
    with open(path, "r") as f:
        return json.load(f)
