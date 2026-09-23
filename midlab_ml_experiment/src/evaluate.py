"""
evaluate.py — Compute and save all metrics for CNN (MLP), SVM and CNN+SVM.
Pure sklearn, no TensorFlow/PyTorch dependency.
"""

import os
import sys
import ast
import time
import csv
import json
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    SELECTED_TEST_X, PROCESSED_TEST_Y,
    CNN_MODEL_PATH, SVM_MODEL_PATH, CNN_SVM_MODEL_PATH,
    CNN_HISTORY_PATH,
    METRICS_CSV, COMPARISON_CSV, CM_DIR,
    MODELS_DIR, CLASS_NAMES, SELECTED_K,
    get_logger, ensure_dirs, load_json,
)
from cnn_model import extract_hidden_features, count_parameters
from cnn_svm_model import predict_cnn_svm

log = get_logger("evaluate")

CNN_MODEL_SKLEARN_PATH = CNN_MODEL_PATH.replace(".keras", "_mlp.joblib")


def plot_confusion_matrix(cm: np.ndarray, model_name: str, save_path: str):
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=ax)
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Label", fontsize=11)
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    log.info("Confusion matrix saved: %s", save_path)


def file_size_kb(path: str) -> float:
    return os.path.getsize(path) / 1024.0 if os.path.isfile(path) else 0.0


def evaluate_cnn(X_test: np.ndarray, y_test: np.ndarray) -> dict:
    log.info("Loading MLP (CNN-equivalent) model...")
    model = joblib.load(CNN_MODEL_SKLEARN_PATH)
    n_params = count_parameters(model)

    t0 = time.perf_counter()
    y_pred = model.predict(X_test)
    t1 = time.perf_counter()
    inference_time = t1 - t0

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    training_time = 0.0
    if os.path.isfile(CNN_HISTORY_PATH):
        training_time = load_json(CNN_HISTORY_PATH).get("training_time_sec", 0.0)

    result = {
        "model": "CNN",
        "accuracy":   float(accuracy_score(y_test, y_pred)),
        "precision":  float(precision_score(y_test, y_pred, zero_division=0)),
        "recall":     float(recall_score(y_test, y_pred, zero_division=0)),
        "f1":         float(f1_score(y_test, y_pred, zero_division=0)),
        "fpr":        float(fpr),
        "training_time_s":  float(training_time),
        "inference_time_s": float(inference_time),
        "inference_per_sample_ms": float(inference_time / len(y_test) * 1000),
        "n_features": SELECTED_K,
        "n_params":   int(n_params),
        "model_size_kb": float(file_size_kb(CNN_MODEL_SKLEARN_PATH)),
        "confusion_matrix": cm.tolist(),
    }
    os.makedirs(CM_DIR, exist_ok=True)
    plot_confusion_matrix(cm, "CNN (MLP)", os.path.join(CM_DIR, "cm_cnn.png"))
    return result


def evaluate_svm(X_test: np.ndarray, y_test: np.ndarray) -> dict:
    log.info("Loading SVM model...")
    svm = joblib.load(SVM_MODEL_PATH)

    timing_path = os.path.join(MODELS_DIR, "svm_timing.json")
    training_time = 0.0
    if os.path.isfile(timing_path):
        with open(timing_path) as f:
            training_time = json.load(f).get("training_time_sec", 0.0)

    t0 = time.perf_counter()
    y_pred = svm.predict(X_test)
    t1 = time.perf_counter()
    inference_time = t1 - t0

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    result = {
        "model": "SVM",
        "accuracy":   float(accuracy_score(y_test, y_pred)),
        "precision":  float(precision_score(y_test, y_pred, zero_division=0)),
        "recall":     float(recall_score(y_test, y_pred, zero_division=0)),
        "f1":         float(f1_score(y_test, y_pred, zero_division=0)),
        "fpr":        float(fpr),
        "training_time_s":  float(training_time),
        "inference_time_s": float(inference_time),
        "inference_per_sample_ms": float(inference_time / len(y_test) * 1000),
        "n_features": SELECTED_K,
        "n_params":   0,
        "model_size_kb": float(file_size_kb(SVM_MODEL_PATH)),
        "confusion_matrix": cm.tolist(),
    }
    os.makedirs(CM_DIR, exist_ok=True)
    plot_confusion_matrix(cm, "SVM", os.path.join(CM_DIR, "cm_svm.png"))
    return result


def evaluate_cnn_svm(X_test: np.ndarray, y_test: np.ndarray) -> dict:
    log.info("Loading CNN+SVM models...")
    cnn_model = joblib.load(CNN_MODEL_SKLEARN_PATH)
    svm       = joblib.load(CNN_SVM_MODEL_PATH)

    timing_path = os.path.join(MODELS_DIR, "cnn_svm_timing.json")
    training_time = 0.0
    if os.path.isfile(timing_path):
        with open(timing_path) as f:
            training_time = json.load(f).get("training_time_sec", 0.0)

    t0 = time.perf_counter()
    y_pred = predict_cnn_svm(cnn_model, svm, X_test)
    t1 = time.perf_counter()
    inference_time = t1 - t0

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    n_params = count_parameters(cnn_model)
    result = {
        "model": "CNN+SVM",
        "accuracy":   float(accuracy_score(y_test, y_pred)),
        "precision":  float(precision_score(y_test, y_pred, zero_division=0)),
        "recall":     float(recall_score(y_test, y_pred, zero_division=0)),
        "f1":         float(f1_score(y_test, y_pred, zero_division=0)),
        "fpr":        float(fpr),
        "training_time_s":  float(training_time),
        "inference_time_s": float(inference_time),
        "inference_per_sample_ms": float(inference_time / len(y_test) * 1000),
        "n_features": SELECTED_K,
        "n_params":   int(n_params),
        "model_size_kb": float(file_size_kb(CNN_MODEL_SKLEARN_PATH) +
                                file_size_kb(CNN_SVM_MODEL_PATH)),
        "confusion_matrix": cm.tolist(),
    }
    os.makedirs(CM_DIR, exist_ok=True)
    plot_confusion_matrix(cm, "CNN+SVM", os.path.join(CM_DIR, "cm_cnn_svm.png"))
    return result


def save_results(results: list):
    fieldnames = [
        "model", "accuracy", "precision", "recall", "f1", "fpr",
        "training_time_s", "inference_time_s", "inference_per_sample_ms",
        "n_features", "n_params", "model_size_kb", "confusion_matrix",
    ]
    os.makedirs(os.path.dirname(METRICS_CSV), exist_ok=True)
    with open(METRICS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in fieldnames})
    log.info("Detailed metrics saved: %s", METRICS_CSV)

    comparison_fields = [
        "model", "accuracy", "precision", "recall", "f1",
        "training_time_s", "inference_time_s", "n_features",
    ]
    with open(COMPARISON_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=comparison_fields)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "model":            r["model"],
                "accuracy":         f"{r['accuracy']:.4f}",
                "precision":        f"{r['precision']:.4f}",
                "recall":           f"{r['recall']:.4f}",
                "f1":               f"{r['f1']:.4f}",
                "training_time_s":  f"{r['training_time_s']:.2f}",
                "inference_time_s": f"{r['inference_time_s']:.4f}",
                "n_features":       r["n_features"],
            })
    log.info("Comparison table saved: %s", COMPARISON_CSV)


def print_results_table(results: list):
    header = (f"\n{'Model':<12} {'Accuracy':>10} {'Precision':>10} "
              f"{'Recall':>10} {'F1':>10} {'FPR':>8} "
              f"{'Train(s)':>10} {'Infer(s)':>10}")
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['model']:<12} {r['accuracy']:>10.4f} {r['precision']:>10.4f} "
              f"{r['recall']:>10.4f} {r['f1']:>10.4f} {r['fpr']:>8.4f} "
              f"{r['training_time_s']:>10.2f} {r['inference_time_s']:>10.4f}")
    print()


def run_evaluate():
    ensure_dirs()
    X_test = np.load(SELECTED_TEST_X)
    y_test = np.load(PROCESSED_TEST_Y)
    log.info("Test set: %s | Normal=%d Attack=%d",
             X_test.shape, int((y_test==0).sum()), int((y_test==1).sum()))

    results = []
    log.info("=== Evaluating CNN (MLP) ===")
    results.append(evaluate_cnn(X_test, y_test))
    log.info("=== Evaluating SVM ===")
    results.append(evaluate_svm(X_test, y_test))
    log.info("=== Evaluating CNN+SVM ===")
    results.append(evaluate_cnn_svm(X_test, y_test))

    print_results_table(results)
    save_results(results)
    return results


if __name__ == "__main__":
    run_evaluate()
