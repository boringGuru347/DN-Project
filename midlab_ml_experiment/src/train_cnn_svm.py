"""
train_cnn_svm.py — Train CNN+SVM pipeline (sklearn MLP + sklearn SVM).
"""

import os
import sys
import time
import numpy as np
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    SELECTED_TRAIN_X, PROCESSED_TRAIN_Y,
    CNN_MODEL_PATH, CNN_SVM_MODEL_PATH,
    MODELS_DIR, RANDOM_SEED, SELECTED_K,
    get_logger, ensure_dirs,
)
from cnn_model import build_cnn_classifier
from cnn_svm_model import train_cnn_svm

log = get_logger("train_cnn_svm")

CNN_MODEL_SKLEARN_PATH = CNN_MODEL_PATH.replace(".keras", "_mlp.joblib")


def run_train_cnn_svm():
    ensure_dirs()

    X_train = np.load(SELECTED_TRAIN_X)
    y_train = np.load(PROCESSED_TRAIN_Y)
    log.info("X_train shape: %s", X_train.shape)

    if not os.path.isfile(CNN_MODEL_SKLEARN_PATH):
        raise FileNotFoundError(
            f"Trained MLP not found at {CNN_MODEL_SKLEARN_PATH}. "
            "Run train_cnn.py first."
        )
    log.info("Loading trained MLP from: %s", CNN_MODEL_SKLEARN_PATH)
    cnn_model = joblib.load(CNN_MODEL_SKLEARN_PATH)

    log.info("Starting MLP feature extraction + SVM training...")
    t_start = time.perf_counter()
    svm = train_cnn_svm(cnn_model, X_train, y_train)
    t_end = time.perf_counter()
    total_time_sec = t_end - t_start

    log.info("CNN+SVM training complete. Total time: %.2f seconds", total_time_sec)
    log.info("Support vectors: %d", svm.n_support_.sum())

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(svm, CNN_SVM_MODEL_PATH)
    log.info("CNN+SVM SVM saved to: %s", CNN_SVM_MODEL_PATH)

    return cnn_model, svm, total_time_sec


if __name__ == "__main__":
    run_train_cnn_svm()
