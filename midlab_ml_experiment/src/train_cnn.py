"""
train_cnn.py — Train the MLP classifier (CNN-equivalent) on UNSW-NB15.
"""

import os
import sys
import time
import numpy as np
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    SELECTED_TRAIN_X, PROCESSED_TRAIN_Y,
    CNN_MODEL_PATH, CNN_HISTORY_PATH,
    SELECTED_K, RANDOM_SEED, MODELS_DIR,
    get_logger, ensure_dirs, save_json,
)
from cnn_model import build_cnn_classifier, count_parameters

log = get_logger("train_cnn")

np.random.seed(RANDOM_SEED)

# Use a .joblib path instead of .keras (MLP is a sklearn object)
CNN_MODEL_SKLEARN_PATH = CNN_MODEL_PATH.replace(".keras", "_mlp.joblib")


def run_train_cnn():
    ensure_dirs()

    log.info("Loading feature-selected data...")
    X_train = np.load(SELECTED_TRAIN_X)
    y_train = np.load(PROCESSED_TRAIN_Y)
    log.info("X_train shape: %s", X_train.shape)
    log.info("Label distribution: Normal=%d, Attack=%d",
             int((y_train==0).sum()), int((y_train==1).sum()))

    model = build_cnn_classifier(SELECTED_K)
    log.info("MLP configuration: hidden_layers=%s, activation=relu, solver=adam",
             model.hidden_layer_sizes)

    log.info("Starting MLP (CNN-equivalent) training...")
    t_start = time.perf_counter()
    model.fit(X_train, y_train)
    t_end = time.perf_counter()
    training_time_sec = t_end - t_start

    n_params = count_parameters(model)
    log.info("Training complete. Time: %.2f seconds", training_time_sec)
    log.info("Epochs run: %d | Best val score: %.4f",
             model.n_iter_, model.best_validation_score_)
    log.info("Trainable parameters: %d", n_params)

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, CNN_MODEL_SKLEARN_PATH)
    log.info("MLP model saved to: %s", CNN_MODEL_SKLEARN_PATH)

    history_data = {
        "training_time_sec": training_time_sec,
        "epochs_run": int(model.n_iter_),
        "best_val_score": float(model.best_validation_score_),
        "loss_curve": [float(v) for v in model.loss_curve_],
        "final_train_loss": float(model.loss_curve_[-1]),
        "n_params": n_params,
    }
    save_json(history_data, CNN_HISTORY_PATH)
    log.info("Training history saved to: %s", CNN_HISTORY_PATH)

    return model, training_time_sec


if __name__ == "__main__":
    run_train_cnn()
