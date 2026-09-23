"""
train_svm.py — Train the standalone SVM classifier on UNSW-NB15.

Steps:
  1. Load feature-selected training arrays.
  2. Build the SVM (RBF kernel, C=1.0, gamma='scale').
  3. Train and record training time.
  4. Save trained model to disk.

Note on performance:
  RBF SVM on 175,341 training samples can take several minutes.
  This is expected — no optimisation or approximate solver is used,
  preserving scientific integrity for the preliminary experiment.
"""

import os
import sys
import time
import numpy as np
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    SELECTED_TRAIN_X, PROCESSED_TRAIN_Y,
    SVM_MODEL_PATH, MODELS_DIR,
    RANDOM_SEED, get_logger, ensure_dirs,
)
from svm_model import build_svm

log = get_logger("train_svm")


def run_train_svm():
    ensure_dirs()

    # --- Load data ---
    log.info("Loading feature-selected training data...")
    X_train = np.load(SELECTED_TRAIN_X)
    y_train = np.load(PROCESSED_TRAIN_Y)

    log.info("X_train shape: %s", X_train.shape)
    log.info("Training label distribution: Normal=%d, Attack=%d",
             int((y_train == 0).sum()), int((y_train == 1).sum()))

    # --- Build SVM ---
    svm = build_svm(random_state=RANDOM_SEED)
    log.info("SVM configuration: kernel=%s, C=%.1f, gamma=%s",
             svm.kernel, svm.C, svm.gamma)

    # --- Train ---
    log.info("Starting SVM training on %d samples...", X_train.shape[0])
    log.info("(This may take several minutes for RBF kernel on large data.)")
    t_start = time.perf_counter()

    svm.fit(X_train, y_train)

    t_end = time.perf_counter()
    training_time_sec = t_end - t_start
    log.info("SVM training complete. Time: %.2f seconds", training_time_sec)
    log.info("Number of support vectors: %d", svm.n_support_.sum())

    # --- Save ---
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(svm, SVM_MODEL_PATH)
    log.info("SVM model saved to: %s", SVM_MODEL_PATH)

    return svm, training_time_sec


if __name__ == "__main__":
    run_train_svm()
