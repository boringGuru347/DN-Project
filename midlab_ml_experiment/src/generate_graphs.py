"""
generate_graphs.py — Generate all result graphs from actual experimental data.

Graph 1 — Model Performance Comparison (bar chart: Acc, Prec, Recall, F1)
Graph 2 — Confusion Matrices (side-by-side, all three models)
Graph 3 — Efficiency Comparison (training time + inference time)
Graph 4 — Feature Reduction vs. Performance (accuracy & F1 across k values)
Graph 5 — CNN Training History (loss and accuracy curves)

All graphs are generated from CSV/JSON files produced during training and
evaluation. No values are hardcoded or fabricated.
"""

import os
import sys
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    METRICS_CSV, COMPARISON_CSV, FEATURE_SWEEP_PATH, CNN_HISTORY_PATH,
    CM_DIR, GRAPHS_DIR, CLASS_NAMES,
    get_logger, ensure_dirs, load_json,
)

log = get_logger("generate_graphs")

# ---------------------------------------------------------------------------
# Colour palette — consistent across all graphs
# ---------------------------------------------------------------------------
COLORS = {
    "CNN":     "#2196F3",   # blue
    "SVM":     "#FF9800",   # orange
    "CNN+SVM": "#4CAF50",   # green
}
MODEL_ORDER = ["CNN", "SVM", "CNN+SVM"]

METRIC_COLORS = {
    "Accuracy":  "#1565C0",
    "Precision": "#E65100",
    "Recall":    "#2E7D32",
    "F1-score":  "#6A1B9A",
}


# ---------------------------------------------------------------------------
# Utility — load metrics CSV into a dict
# ---------------------------------------------------------------------------
def load_metrics() -> dict:
    """Load metrics.csv and return {model_name: {metric: value}} dict."""
    data = {}
    with open(METRICS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["model"]] = row
    return data


# ---------------------------------------------------------------------------
# Graph 1 — Model Performance Comparison
# ---------------------------------------------------------------------------
def graph1_model_performance(metrics: dict, save_path: str):
    """Grouped bar chart comparing Accuracy, Precision, Recall, F1 for all models."""
    metric_keys = ["accuracy", "precision", "recall", "f1"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1-score"]
    x = np.arange(len(metric_labels))
    bar_width = 0.22
    offsets = [-bar_width, 0, bar_width]

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, model in enumerate(MODEL_ORDER):
        values = [float(metrics[model][k]) for k in metric_keys]
        bars = ax.bar(x + offsets[i], values, bar_width,
                      label=model, color=COLORS[model], alpha=0.88,
                      edgecolor="white", linewidth=0.5)
        # Annotate bars
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.005,
                    f"{v:.3f}", ha="center", va="bottom", fontsize=7.5,
                    fontweight="bold")

    ax.set_xlabel("Metric", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Performance Comparison — CNN vs SVM vs CNN+SVM\n"
                 "(UNSW-NB15 Dataset, Binary Intrusion Detection)",
                 fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=11)
    ax.set_ylim(0.0, 1.10)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.35)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    log.info("Graph 1 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Graph 2 — Confusion Matrices (combined into one figure)
# ---------------------------------------------------------------------------
def graph2_confusion_matrices(save_path: str):
    """Load per-model confusion matrices from CSV and plot side-by-side."""
    import ast
    metrics = load_metrics()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    for ax, model in zip(axes, MODEL_ORDER):
        # confusion_matrix is stored as a Python list repr in the CSV
        cm = np.array(ast.literal_eval(metrics[model]["confusion_matrix"]))

        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
            ax=ax, cbar=False,
            annot_kws={"size": 13, "weight": "bold"},
        )
        ax.set_xlabel("Predicted", fontsize=10)
        ax.set_ylabel("Actual", fontsize=10)
        acc = float(metrics[model]["accuracy"])
        ax.set_title(f"{model}\n(Accuracy = {acc:.4f})", fontsize=11, fontweight="bold")

    fig.suptitle(
        "Confusion Matrices — CNN, SVM, CNN+SVM\n"
        "UNSW-NB15 Binary Intrusion Detection (Normal=0, Attack=1)",
        fontsize=12, fontweight="bold", y=1.02,
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Graph 2 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Graph 3 — Efficiency Comparison (Training + Inference Time)
# ---------------------------------------------------------------------------
def graph3_efficiency(metrics: dict, save_path: str):
    """Side-by-side bar chart for training time and inference time."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    models = MODEL_ORDER
    train_times = [float(metrics[m]["training_time_s"]) for m in models]
    infer_times = [float(metrics[m]["inference_time_s"]) for m in models]
    colors = [COLORS[m] for m in models]

    # Training time
    bars1 = ax1.bar(models, train_times, color=colors, alpha=0.88,
                    edgecolor="white", linewidth=0.8, width=0.5)
    for bar, v in zip(bars1, train_times):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(train_times) * 0.01,
                 f"{v:.1f}s", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.set_title("Training Time (seconds)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Time (seconds)", fontsize=10)
    ax1.set_ylim(0, max(train_times) * 1.25)
    ax1.grid(axis="y", alpha=0.35)
    ax1.spines[["top", "right"]].set_visible(False)

    # Inference time
    bars2 = ax2.bar(models, infer_times, color=colors, alpha=0.88,
                    edgecolor="white", linewidth=0.8, width=0.5)
    for bar, v in zip(bars2, infer_times):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(infer_times) * 0.01,
                 f"{v:.3f}s", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax2.set_title("Inference Time on Test Set (seconds)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Time (seconds)", fontsize=10)
    ax2.set_ylim(0, max(infer_times) * 1.25)
    ax2.grid(axis="y", alpha=0.35)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle(
        "Computational Efficiency Comparison\n"
        "CNN vs SVM vs CNN+SVM (UNSW-NB15)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    log.info("Graph 3 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Graph 4 — Feature Reduction vs. Performance
# ---------------------------------------------------------------------------
def graph4_feature_reduction(save_path: str):
    """Line graph: accuracy and F1 vs. number of selected features."""
    if not os.path.isfile(FEATURE_SWEEP_PATH):
        log.warning("Feature sweep file not found: %s — skipping Graph 4",
                    FEATURE_SWEEP_PATH)
        return

    sweep = load_json(FEATURE_SWEEP_PATH)
    ks       = sorted([int(k) for k in sweep.keys()])
    accuracy = [sweep[str(k)]["accuracy"] for k in ks]
    f1       = [sweep[str(k)]["f1"] for k in ks]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ks, accuracy, "o-", color="#1565C0", linewidth=2, markersize=8,
            label="Accuracy")
    ax.plot(ks, f1, "s-", color="#2E7D32", linewidth=2, markersize=8,
            label="F1-score")

    # Highlight the selected k
    from utils import SELECTED_K
    sel_acc = sweep[str(SELECTED_K)]["accuracy"]
    sel_f1  = sweep[str(SELECTED_K)]["f1"]
    ax.axvline(x=SELECTED_K, color="gray", linestyle="--", alpha=0.6)
    ax.text(SELECTED_K + 0.3, min(accuracy) + 0.005,
            f"Working k={SELECTED_K}", color="gray", fontsize=9)

    for k, a, f in zip(ks, accuracy, f1):
        ax.annotate(f"{a:.3f}", (k, a), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8, color="#1565C0")
        ax.annotate(f"{f:.3f}", (k, f), textcoords="offset points",
                    xytext=(0, -14), ha="center", fontsize=8, color="#2E7D32")

    ax.set_xlabel("Number of Selected Features (k)", fontsize=11)
    ax.set_ylabel("Score", fontsize=11)
    ax.set_title(
        "Feature Reduction vs. Classification Performance\n"
        "(LinearSVC sweep on UNSW-NB15, original features = 49)",
        fontsize=11, fontweight="bold",
    )
    ax.set_xticks(ks)
    ax.set_ylim(
        min(min(accuracy), min(f1)) - 0.02,
        max(max(accuracy), max(f1)) + 0.04,
    )
    ax.legend(fontsize=10)
    ax.grid(alpha=0.35)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    log.info("Graph 4 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Graph 5 — CNN Training History
# ---------------------------------------------------------------------------
def graph5_cnn_history(save_path: str):
    """Loss curve across training iterations for the CNN (MLP)."""
    if not os.path.isfile(CNN_HISTORY_PATH):
        log.warning("CNN history file not found: %s — skipping Graph 5",
                    CNN_HISTORY_PATH)
        return

    history = load_json(CNN_HISTORY_PATH)
    loss_curve = history.get("loss_curve", [])
    if not loss_curve:
        log.warning("No loss_curve in history — skipping Graph 5")
        return

    iters = list(range(1, len(loss_curve) + 1))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(iters, loss_curve, "o-", color="#1565C0", linewidth=2,
            markersize=4, label="Training Loss")
    ax.set_xlabel("Iteration", fontsize=11)
    ax.set_ylabel("Loss", fontsize=11)
    ax.set_title("CNN (MLP) Training Loss Curve", fontsize=11, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.35)
    ax.spines[["top", "right"]].set_visible(False)

    train_time = history.get("training_time_sec", 0)
    n_epochs   = history.get("epochs_run", "?")
    best_val   = history.get("best_val_score", 0)
    fig.suptitle(
        f"CNN (MLP) Training History  "
        f"({n_epochs} epochs, time {train_time:.1f}s, best val score {best_val:.4f})",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    log.info("Graph 5 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run_generate_graphs():
    ensure_dirs()
    metrics = load_metrics()

    graph1_model_performance(
        metrics,
        os.path.join(GRAPHS_DIR, "model_performance_comparison.png"),
    )
    graph2_confusion_matrices(
        os.path.join(GRAPHS_DIR, "confusion_matrices.png"),
    )
    graph3_efficiency(
        metrics,
        os.path.join(GRAPHS_DIR, "efficiency_comparison.png"),
    )
    graph4_feature_reduction(
        os.path.join(GRAPHS_DIR, "feature_reduction.png"),
    )
    graph5_cnn_history(
        os.path.join(GRAPHS_DIR, "cnn_training_history.png"),
    )
    log.info("All graphs generated in: %s", GRAPHS_DIR)


if __name__ == "__main__":
    run_generate_graphs()
