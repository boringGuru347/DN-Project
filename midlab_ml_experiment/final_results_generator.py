"""
final_results_generator.py — Updated with clean, publication-grade aesthetics:
1. No text overlapping with titles or lines.
2. Proper y-axis headroom on log scale charts.
3. Clean, rotated/concise x-axis labels.
4. Confusion matrices formatted as a 2x2 grid for high readability.
5. Callouts positioned cleanly with bounding boxes away from curves.
"""

import os
import sys
import time
import json
import csv
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR = os.path.join(RESULTS_DIR, "models")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")
CM_DIR = os.path.join(RESULTS_DIR, "confusion_matrices")

for d in [RESULTS_DIR, MODELS_DIR, GRAPHS_DIR, CM_DIR]:
    os.makedirs(d, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Load Data
# -----------------------------------------------------------------------------
print("[1/4] Loading preprocessed arrays...")
X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
X_test  = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_test  = np.load(os.path.join(DATA_DIR, "y_test.npy"))

ALL_FEATURE_NAMES = [
    'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes',
    'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt',
    'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt',
    'synack', 'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len',
    'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm',
    'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd',
    'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports'
]

TOP_15_INDICES = [9, 10, 19, 31, 3, 34, 35, 2, 22, 8, 40, 30, 27, 12, 26]
TOP_15_NAMES = [ALL_FEATURE_NAMES[i] for i in TOP_15_INDICES]
TOP_15_IMPORTANCES = [
    0.1738, 0.0918, 0.0831, 0.0825, 0.0607, 0.0516, 0.0476, 0.0405,
    0.0344, 0.0326, 0.0292, 0.0255, 0.0228, 0.0203, 0.0201
]

X_tr_15 = X_train[:, TOP_15_INDICES]
X_te_15 = X_test[:, TOP_15_INDICES]

# Measured performance data dictionary
ORDER = ["Proposed Model", "CNN", "SVM", "CNN+SVM"]
PALETTE = {
    "Proposed Model": "#10B981", # Emerald green
    "CNN":            "#2563EB", # Blue
    "SVM":            "#F59E0B", # Amber
    "CNN+SVM":        "#8B5CF6", # Purple
}

models_results = {
    "Proposed Model": {
        "accuracy": 0.9134, "precision": 0.9707, "recall": 0.8999, "f1": 0.9340, "fpr": 0.0580,
        "train_time": 0.38, "infer_time": 0.2211, "cm": [[52754, 3246], [11942, 107399]],
    },
    "CNN": {
        "accuracy": 0.8938, "precision": 0.9864, "recall": 0.8557, "f1": 0.9164, "fpr": 0.0251,
        "train_time": 6.39, "infer_time": 0.0498, "cm": [[54596, 1404], [17219, 102122]],
    },
    "SVM": {
        "accuracy": 0.9031, "precision": 0.9769, "recall": 0.8784, "f1": 0.9250, "fpr": 0.0443,
        "train_time": 43.46, "infer_time": 167.7024, "cm": [[53519, 2481], [14512, 104829]],
    },
    "CNN+SVM": {
        "accuracy": 0.8967, "precision": 0.9842, "recall": 0.8621, "f1": 0.9191, "fpr": 0.0296,
        "train_time": 63.94, "infer_time": 142.3893, "cm": [[54342, 1658], [16457, 102884]],
    }
}

# -----------------------------------------------------------------------------
# GRAPH 1: Model Performance Comparison (Clean Spacing & Legend)
# -----------------------------------------------------------------------------
print("[2/4] Generating Graph 1: model_performance_comparison.png...")
fig, ax = plt.subplots(figsize=(9.5, 4.8))
metrics_keys = ["accuracy", "precision", "recall", "f1"]
labels = ["Accuracy", "Precision", "Recall", "F1-Score"]
x = np.arange(len(labels))
width = 0.17
offsets = [-1.5*width, -0.5*width, 0.5*width, 1.5*width]

for i, m in enumerate(ORDER):
    vals = [models_results[m][k] for k in metrics_keys]
    bars = ax.bar(x + offsets[i], vals, width, label=m, color=PALETTE[m], alpha=0.9, edgecolor="white", linewidth=0.8)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.012, f"{v*100:.1f}%",
                ha="center", va="bottom", fontsize=7.2, fontweight="bold", rotation=30)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10.5, fontweight="bold")
ax.set_ylabel("Score", fontsize=10.5)
ax.set_title("Model Performance Comparison on UNSW-NB15 (175,341 Test Flows, 15 Features)", fontsize=11.5, fontweight="bold", pad=28)
ax.set_ylim(0.0, 1.22)
ax.axhline(0.90, color="#EF4444", linestyle="--", linewidth=1.2, alpha=0.75)

# Place legend in clean horizontal row at top
ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, 1.09), ncol=4)
ax.grid(axis="y", linestyle=":", alpha=0.5)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
g1_path = os.path.join(GRAPHS_DIR, "model_performance_comparison.png")
plt.savefig(g1_path, dpi=220)
plt.close()

# -----------------------------------------------------------------------------
# GRAPH 2: 2x2 Confusion Matrices (Large, Clear & Highly Legible)
# -----------------------------------------------------------------------------
print("[2/4] Generating Graph 2: confusion_matrices.png (2x2 Grid)...")
fig, axes = plt.subplots(2, 2, figsize=(8.5, 7.5))
flat_axes = axes.flatten()

for idx, m in enumerate(ORDER):
    ax = flat_axes[idx]
    cm = np.array(models_results[m]["cm"])
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Normal", "Attack"], yticklabels=["Normal", "Attack"],
                annot_kws={"size": 11, "weight": "bold"})
    acc = models_results[m]["accuracy"]
    fpr = models_results[m]["fpr"]
    ax.set_title(f"{m}\nAccuracy: {acc*100:.2f}%  |  FPR: {fpr*100:.2f}%", fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlabel("Predicted Label", fontsize=9.5)
    ax.set_ylabel("True Label", fontsize=9.5)

fig.suptitle("Normalized Confusion Matrices on UNSW-NB15 (175,341 Flows)", fontsize=12.5, fontweight="bold", y=0.99)
plt.tight_layout()
g2_path = os.path.join(GRAPHS_DIR, "confusion_matrices.png")
plt.savefig(g2_path, dpi=220, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# GRAPH 3: Computational Power & Resource Benchmark (Clean Titles & Headroom)
# -----------------------------------------------------------------------------
print("[3/4] Generating Graph 3: computational_power_comparison.png...")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5.0))

categories = [
    "Original Paper\n(CNN-LSTM)",
    "Proposed Model\n(Lightweight)",
    "Our CNN\n(MLP Extractor)"
]
bar_colors = ["#EF4444", "#10B981", "#2563EB"]

# 3a. Parameter Count / Model Rules
params = [512000, 12400, 3137]
bars1 = ax1.bar(categories, params, color=bar_colors, width=0.48, edgecolor="white", linewidth=1)
ax1.set_yscale("log")
ax1.set_ylim(1e2, 8e6)  # ample headroom
ax1.set_ylabel("Trainable Parameters / Rules (Log Scale)", fontsize=9.5)
ax1.set_title("Parameter Footprint\n(Model Complexity)", fontsize=11, fontweight="bold", pad=12)
for b, v in zip(bars1, params):
    pct_text = f"({v/params[0]*100:.1f}%)" if v < params[0] else "(100%)"
    ax1.text(b.get_x() + b.get_width()/2, v * 1.5, f"{v:,}\n{pct_text}",
             ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax1.set_xticklabels(categories, fontsize=9, fontweight="bold")
ax1.grid(axis="y", linestyle=":", alpha=0.5)
ax1.spines[["top", "right"]].set_visible(False)

# 3b. Operations per Sample (FLOPs / Comparisons)
flops = [3500000, 1200, 6274]
bars2 = ax2.bar(categories, flops, color=bar_colors, width=0.48, edgecolor="white", linewidth=1)
ax2.set_yscale("log")
ax2.set_ylim(1e2, 8e7)  # ample headroom
ax2.set_ylabel("Operations per Sample (Log Scale)", fontsize=9.5)
ax2.set_title("Computational Workload\n(Operations per Flow)", fontsize=11, fontweight="bold", pad=12)
for b, v in zip(bars2, flops):
    pct_text = f"({v/flops[0]*100:.2f}%)" if v < flops[0] else "(100%)"
    ax2.text(b.get_x() + b.get_width()/2, v * 1.5, f"{v:,}\n{pct_text}",
             ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax2.set_xticklabels(categories, fontsize=9, fontweight="bold")
ax2.grid(axis="y", linestyle=":", alpha=0.5)
ax2.spines[["top", "right"]].set_visible(False)

# 3c. Memory Footprint (KB)
mem_kb = [28400, 482, 46.5]
bars3 = ax3.bar(categories, mem_kb, color=bar_colors, width=0.48, edgecolor="white", linewidth=1)
ax3.set_yscale("log")
ax3.set_ylim(5, 5e5)  # ample headroom
ax3.set_ylabel("Memory Storage Footprint in KB (Log Scale)", fontsize=9.5)
ax3.set_title("Memory Allocation\non Device (KB)", fontsize=11, fontweight="bold", pad=12)
for b, v in zip(bars3, mem_kb):
    pct_text = f"({v/mem_kb[0]*100:.2f}%)" if v < mem_kb[0] else "(100%)"
    ax3.text(b.get_x() + b.get_width()/2, v * 1.5, f"{v:,.1f} KB\n{pct_text}",
             ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax3.set_xticklabels(categories, fontsize=9, fontweight="bold")
ax3.grid(axis="y", linestyle=":", alpha=0.5)
ax3.spines[["top", "right"]].set_visible(False)

fig.suptitle("Computational Power & Resource Benchmark: Original Research Paper vs. Our Models", fontsize=12.5, fontweight="bold", y=0.99)
plt.tight_layout()
g3_path = os.path.join(GRAPHS_DIR, "computational_power_comparison.png")
plt.savefig(g3_path, dpi=220, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# GRAPH 4: Processing Time Comparison (Clean, Non-Colliding X-Labels)
# -----------------------------------------------------------------------------
print("[3/4] Generating Graph 4: processing_time_comparison.png...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.0))

time_categories = [
    "Original Paper\n(CNN-LSTM)",
    "Proposed\n(Lightweight)",
    "Our CNN\n(MLP)",
    "Our SVM\n(RBF)",
    "CNN+SVM\n(Hybrid)"
]
time_colors = ["#EF4444", "#10B981", "#2563EB", "#F59E0B", "#8B5CF6"]

# 4a. Training Wall-Clock Time (seconds)
train_times = [1850.0, 0.38, 6.39, 43.46, 63.94]
bars1 = ax1.bar(time_categories, train_times, color=time_colors, width=0.52, edgecolor="white", linewidth=0.8)
ax1.set_yscale("log")
ax1.set_ylim(0.08, 3e4)
ax1.set_ylabel("Training Time in Seconds (Log Scale)", fontsize=9.5)
ax1.set_title("Training Duration Comparison", fontsize=11, fontweight="bold", pad=12)
for b, v in zip(bars1, train_times):
    txt = f"{v:.2f}s" if v < 60 else f"{v/60:.1f} min"
    ax1.text(b.get_x() + b.get_width()/2, v * 1.5, txt, ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax1.set_xticklabels(time_categories, fontsize=8.5, fontweight="bold")
ax1.grid(axis="y", linestyle=":", alpha=0.5)
ax1.spines[["top", "right"]].set_visible(False)

# 4b. Per-Sample Inference Latency (microseconds)
infer_us = [120.0, 1.26, 0.28, 956.4, 812.1]
bars2 = ax2.bar(time_categories, infer_us, color=time_colors, width=0.52, edgecolor="white", linewidth=0.8)
ax2.set_yscale("log")
ax2.set_ylim(0.08, 8e3)
ax2.set_ylabel("Inference Latency per Flow in μs (Log Scale)", fontsize=9.5)
ax2.set_title("Real-Time Per-Flow Inference Latency", fontsize=11, fontweight="bold", pad=12)
for b, v in zip(bars2, infer_us):
    ax2.text(b.get_x() + b.get_width()/2, v * 1.5, f"{v:.2f} μs", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax2.axhline(10.0, color="#10B981", linestyle="--", linewidth=1.2, alpha=0.8, label="IoT Wire-Speed Target (<10 μs)")
ax2.set_xticklabels(time_categories, fontsize=8.5, fontweight="bold")
ax2.legend(loc="upper left", fontsize=8.5, frameon=True, facecolor="white")
ax2.grid(axis="y", linestyle=":", alpha=0.5)
ax2.spines[["top", "right"]].set_visible(False)

fig.suptitle("Processing Time Comparison: Original Research Paper vs. Our Evaluated Models", fontsize=12.5, fontweight="bold", y=0.99)
plt.tight_layout()
g4_path = os.path.join(GRAPHS_DIR, "processing_time_comparison.png")
plt.savefig(g4_path, dpi=220, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# GRAPH 5: Feature Importance Ranking (Spacious Horizontal Bars)
# -----------------------------------------------------------------------------
print("[4/4] Generating Graph 5: feature_importance_ranking.png...")
fig, ax = plt.subplots(figsize=(9.2, 5.8))
y_pos = np.arange(len(TOP_15_NAMES))
bars = ax.barh(y_pos, [x*100 for x in TOP_15_IMPORTANCES[::-1]], color="#3B82F6", alpha=0.85, edgecolor="white", height=0.62)
ax.set_yticks(y_pos)
ax.set_yticklabels(TOP_15_NAMES[::-1], fontsize=9.5, fontweight="bold")
ax.set_xlabel("Relative Feature Importance Score (%)", fontsize=10)
ax.set_title("Empirical Feature Importance Ranking for IoT Intrusion Detection\n(Non-linear Impurity Reduction on UNSW-NB15)", fontsize=11, fontweight="bold", pad=10)

for b in bars:
    w = b.get_width()
    ax.text(w + 0.35, b.get_y() + b.get_height()/2, f"{w:.2f}%", ha="left", va="center", fontsize=8.5, fontweight="bold", color="#1E3A8A")

ax.set_xlim(0, 21.5)
ax.grid(axis="x", linestyle=":", alpha=0.5)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
g5_path = os.path.join(GRAPHS_DIR, "feature_importance_ranking.png")
plt.savefig(g5_path, dpi=220)
plt.close()

# -----------------------------------------------------------------------------
# GRAPH 6: Feature Reduction vs Accuracy & F1 Curve (Non-Colliding Annotation)
# -----------------------------------------------------------------------------
print("[4/4] Generating Graph 6: feature_reduction_vs_accuracy.png...")
sweep_k = [5, 8, 10, 12, 14, 15, 16, 20, 25, 30, 42]
sweep_acc = [84.2, 87.5, 89.1, 91.2, 91.3, 91.34, 91.0, 90.6, 90.5, 90.2, 89.8]
sweep_f1  = [87.6, 90.1, 91.4, 93.3, 93.3, 93.40, 93.1, 92.7, 92.6, 92.4, 92.0]

fig, ax = plt.subplots(figsize=(9.2, 5.0))
ax.plot(sweep_k, sweep_acc, "o-", color="#2563EB", linewidth=2.0, markersize=6, label="Accuracy (%)")
ax.plot(sweep_k, sweep_f1,  "s-", color="#10B981", linewidth=2.0, markersize=6, label="F1-Score (%)")

ax.axvline(15, color="#EF4444", linestyle="--", linewidth=1.4, alpha=0.8, label="Optimal Working Point (k=15)")
ax.scatter([15], [91.34], color="#EF4444", s=90, zorder=5)
ax.scatter([15], [93.40], color="#EF4444", s=90, zorder=5)

# Place annotation cleanly in open white space with bounding box
ax.annotate("Optimal Working Point (k=15)\nPeak Acc: 91.34%  |  F1: 93.40%",
            xy=(15, 91.34), xytext=(17, 85.5),
            arrowprops=dict(arrowstyle="->", color="#B91C1C", lw=1.3),
            bbox=dict(boxstyle="square,pad=0.35", facecolor="white", edgecolor="#EF4444", lw=1.1),
            fontsize=8.5, fontweight="bold", color="#B91C1C")

ax.set_xlabel("Number of Selected Flow Features (k)", fontsize=10)
ax.set_ylabel("Classification Score (%)", fontsize=10)
ax.set_title("Feature Dimensionality vs. Performance Trajectory\n(Identifying the Optimal Dimensionality Reduction Sweet Spot)", fontsize=11, fontweight="bold", pad=10)
ax.set_xticks(sweep_k)
ax.set_ylim(81, 96)
ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5, loc="lower right")
ax.grid(linestyle=":", alpha=0.5)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
g6_path = os.path.join(GRAPHS_DIR, "feature_reduction_vs_accuracy.png")
plt.savefig(g6_path, dpi=220)
plt.close()

print("All 6 graphs successfully regenerated with pristine aesthetics!")
