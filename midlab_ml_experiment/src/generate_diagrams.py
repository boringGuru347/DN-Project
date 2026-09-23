"""
generate_diagrams.py — Generate technical flow diagrams using matplotlib.

Diagram 1 — Overall experimental pipeline
Diagram 2 — CNN architecture flow
Diagram 3 — SVM flow
Diagram 4 — CNN+SVM flow

All diagrams are generated programmatically using matplotlib patches and arrows
so they match the actual implemented architecture exactly.
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import DIAGRAMS_DIR, get_logger, ensure_dirs

log = get_logger("generate_diagrams")

# ---------------------------------------------------------------------------
# Helper — draw a labelled box
# ---------------------------------------------------------------------------
def draw_box(ax, x, y, width, height, label, color="#E3F2FD",
             fontsize=9, bold=False, border_color="#1565C0", linewidth=1.5):
    """Draw a rounded rectangle with centred label."""
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.03",
        facecolor=color, edgecolor=border_color, linewidth=linewidth,
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x, y, label, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, color="#0D1117")


def draw_arrow(ax, x, y_start, y_end, color="#555555"):
    """Draw a downward arrow between two y coordinates at x."""
    ax.annotate(
        "", xy=(x, y_end), xytext=(x, y_start),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5),
    )


def draw_branching_arrows(ax, x_src, y_src, targets_xy, color="#555555"):
    """Draw arrows from one point to multiple targets (for parallel branches)."""
    # Horizontal line
    xs = [t[0] for t in targets_xy]
    ax.plot([min(xs), max(xs)], [y_src, y_src],
            color=color, lw=1.2, solid_capstyle="round")
    for tx, ty in targets_xy:
        ax.annotate(
            "", xy=(tx, ty), xytext=(tx, y_src),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5),
        )


def draw_merging_arrows(ax, sources_xy, x_dst, y_dst, color="#555555"):
    """Draw arrows from multiple sources to a single destination."""
    ys = y_dst + 0.06
    xs = [s[0] for s in sources_xy]
    ax.plot([min(xs), max(xs)], [ys, ys],
            color=color, lw=1.2, solid_capstyle="round")
    for sx, sy in sources_xy:
        ax.annotate(
            "", xy=(sx, ys), xytext=(sx, sy),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5),
        )
    ax.annotate(
        "", xy=(x_dst, y_dst), xytext=(x_dst, ys),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5),
    )


# ---------------------------------------------------------------------------
# Diagram 1 — Overall Experimental Pipeline
# ---------------------------------------------------------------------------
def diagram1_overall_pipeline(save_path: str):
    fig, ax = plt.subplots(figsize=(8, 13))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    cx = 0.50   # centre x

    # Sequential boxes
    steps = [
        (0.95, "IoT Network Traffic Data\n(UNSW-NB15 Dataset)",  "#E8EAF6", True),
        (0.86, "Data Loading\n(Training + Testing CSVs)",         "#E3F2FD", False),
        (0.77, "Data Cleaning\n(Remove irrelevant columns,\nhandle NaN/Inf)",  "#E3F2FD", False),
        (0.68, "Categorical Encoding + Feature Scaling\n(fitted on training only)", "#E3F2FD", False),
        (0.59, "Feature Selection\n(SelectKBest, ANOVA F-score, k=20 of 49)", "#FFF3E0", False),
        (0.50, "Train / Test Split\n(pre-defined UNSW-NB15 partition)",        "#E8F5E9", False),
    ]
    for y, label, color, bold in steps:
        draw_box(ax, cx, y, 0.60, 0.07, label, color=color, bold=bold, fontsize=8)
        if y < 0.95:
            draw_arrow(ax, cx, y + 0.07 / 2 + 0.01, y + 0.07 / 2 + 0.005)  # stub; re-calc below

    # Re-draw arrows (cleaner)
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for y, label, color, bold in steps:
        draw_box(ax, cx, y, 0.62, 0.068, label, color=color, bold=bold, fontsize=8)

    prev_y = None
    for y, label, color, bold in steps:
        if prev_y is not None:
            draw_arrow(ax, cx, prev_y - 0.034, y + 0.034)
        prev_y = y

    # Parallel branches
    branch_y_start = 0.46
    branch_y_top   = 0.40
    branch_ys      = [0.30, 0.30, 0.30]
    branch_xs      = [0.18, 0.50, 0.82]
    branch_labels  = ["CNN", "SVM", "CNN+SVM"]
    branch_colors  = ["#BBDEFB", "#FFE0B2", "#C8E6C9"]

    # Draw split arrow horizontal line
    ax.plot([branch_xs[0], branch_xs[2]], [branch_y_top, branch_y_top],
            color="#555", lw=1.2)
    draw_arrow(ax, cx, 0.50 - 0.034, branch_y_top + 0.005)
    for bx, bl, bc in zip(branch_xs, branch_labels, branch_colors):
        draw_arrow(ax, bx, branch_y_top, 0.34)
        draw_box(ax, bx, 0.30, 0.28, 0.08, bl, color=bc, bold=True, fontsize=10,
                 border_color="#333333", linewidth=2)

    # Merge back
    merge_y = 0.22
    ax.plot([branch_xs[0], branch_xs[2]], [merge_y + 0.035, merge_y + 0.035],
            color="#555", lw=1.2)
    for bx in branch_xs:
        draw_arrow(ax, bx, 0.30 - 0.04, merge_y + 0.035 + 0.005)
    draw_arrow(ax, cx, merge_y + 0.035, merge_y + 0.005)

    draw_box(ax, cx, 0.18, 0.62, 0.068,
             "Performance Evaluation\n(Accuracy, Precision, Recall, F1, FPR, Time)",
             color="#F3E5F5", bold=False, fontsize=8)
    draw_arrow(ax, cx, 0.18 - 0.034, 0.10 + 0.034)
    draw_box(ax, cx, 0.10, 0.62, 0.068,
             "Results Comparison & Graphs",
             color="#FCE4EC", bold=True, fontsize=9)

    fig.suptitle("Overall Experimental Pipeline\nDN Mid-Lab Preliminary Experiment — UNSW-NB15",
                 fontsize=11, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Diagram 1 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Diagram 2 — CNN Architecture Flow
# ---------------------------------------------------------------------------
def diagram2_cnn_flow(save_path: str):
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    cx = 0.50

    layers = [
        (0.93, "Input: Traffic Features\n(20 selected, scaled)",    "#E8EAF6", True),
        (0.82, "Reshape → (20, 1)\n1-D Sequence for Conv1D",         "#F3E5F5", False),
        (0.71, "Conv1D — 32 filters, kernel=3\nActivation: ReLU",   "#E3F2FD", False),
        (0.60, "MaxPooling1D — pool size=2",                          "#E3F2FD", False),
        (0.49, "Conv1D — 64 filters, kernel=3\nActivation: ReLU",   "#E3F2FD", False),
        (0.38, "GlobalAveragePooling1D\n→ 64-D feature vector\n[Feature extractor output for CNN+SVM]", "#FFF9C4", True),
        (0.27, "Dense (64 units, ReLU)\nDropout 0.3",                "#E8F5E9", False),
        (0.16, "Dense (1 unit, Sigmoid)\n→ Normal / Attack",         "#FCE4EC", True),
    ]

    for y, label, color, bold in layers:
        draw_box(ax, cx, y, 0.70, 0.075, label, color=color, bold=bold, fontsize=8.5)

    prev_y = None
    for y, _, _, _ in layers:
        if prev_y is not None:
            draw_arrow(ax, cx, prev_y - 0.075 / 2 - 0.005, y + 0.075 / 2 + 0.005)
        prev_y = y

    # Annotate feature size at each step
    annotations = [
        (0.93, "(20,)"),
        (0.82, "(20, 1)"),
        (0.71, "(20, 32)"),
        (0.60, "(10, 32)"),
        (0.49, "(10, 64)"),
        (0.38, "(64,)"),
        (0.27, "(64,)"),
        (0.16, "(1,)"),
    ]
    for y, note in annotations:
        ax.text(0.85, y, note, ha="left", va="center", fontsize=7.5,
                color="#616161", fontstyle="italic")

    ax.text(0.50, 0.06, f"~12,000–15,000 trainable parameters",
            ha="center", fontsize=8.5, color="#424242",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F5F5F5",
                      edgecolor="#BDBDBD"))

    fig.suptitle("CNN Architecture — IoT Intrusion Detection\n"
                 "(1-D Conv on network-flow feature vector)",
                 fontsize=11, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Diagram 2 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Diagram 3 — SVM Flow
# ---------------------------------------------------------------------------
def diagram3_svm_flow(save_path: str):
    fig, ax = plt.subplots(figsize=(6, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    cx = 0.50

    steps = [
        (0.88, "Input: Traffic Features\n(20 selected features)", "#E8EAF6", True),
        (0.72, "Feature Scaling\n(StandardScaler, fitted on training only)",  "#E3F2FD", False),
        (0.56, "SVM — RBF Kernel\nC = 1.0,  gamma = 'scale'\n"
               "(finds optimal hyperplane in kernel space)",      "#FFE0B2", True),
        (0.34, "Support Vectors\n(data points closest to decision boundary)",  "#FFF9C4", False),
        (0.18, "Classification Output\nNormal  /  Attack",        "#E8F5E9", True),
    ]

    for y, label, color, bold in steps:
        draw_box(ax, cx, y, 0.70, 0.11, label, color=color, bold=bold, fontsize=9)

    prev_y = None
    for y, _, _, _ in steps:
        if prev_y is not None:
            draw_arrow(ax, cx, prev_y - 0.11 / 2 - 0.005, y + 0.11 / 2 + 0.005)
        prev_y = y

    fig.suptitle("SVM Pipeline — IoT Intrusion Detection\n"
                 "(RBF kernel on 20 ANOVA-selected features)",
                 fontsize=11, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Diagram 3 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Diagram 4 — CNN+SVM Flow
# ---------------------------------------------------------------------------
def diagram4_cnn_svm_flow(save_path: str):
    fig, ax = plt.subplots(figsize=(6, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    cx = 0.50

    steps = [
        (0.93, "Input: Traffic Features\n(20 selected, scaled)", "#E8EAF6", True),
        (0.80, "CNN — Conv1D Blocks\n(2 × Conv1D + Pooling)",    "#E3F2FD", False),
        (0.67, "GlobalAveragePooling1D\n→ 64-D Learned Representation\n"
               "(CNN acts as non-linear feature transformer)", "#FFF9C4", True),
        (0.52, "SVM — RBF Kernel\nC = 1.0,  gamma = 'scale'\n"
               "(classifies in CNN-learned feature space)",      "#FFE0B2", True),
        (0.37, "Classification Output\nNormal  /  Attack",       "#E8F5E9", True),
    ]

    for y, label, color, bold in steps:
        draw_box(ax, cx, y, 0.72, 0.10, label, color=color, bold=bold, fontsize=8.5)

    prev_y = None
    for y, _, _, _ in steps:
        if prev_y is not None:
            draw_arrow(ax, cx, prev_y - 0.10 / 2 - 0.005, y + 0.10 / 2 + 0.005)
        prev_y = y

    # Annotation box explaining the distinction
    ax.text(0.50, 0.20,
            "CNN transforms raw features into a compact learned\n"
            "representation. SVM then performs the final decision.\n"
            "Unlike standalone SVM (20-D raw features), SVM here\n"
            "operates on 64-D CNN-extracted nonlinear features.",
            ha="center", va="center", fontsize=8,
            color="#333333",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F0F4FF",
                      edgecolor="#9FA8DA", linewidth=1.2))

    fig.suptitle("CNN+SVM Hybrid Pipeline — IoT Intrusion Detection\n"
                 "(CNN as feature extractor + SVM as classifier)",
                 fontsize=11, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Diagram 4 saved: %s", save_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run_generate_diagrams():
    ensure_dirs()

    diagram1_overall_pipeline(os.path.join(DIAGRAMS_DIR, "overall_pipeline.png"))
    diagram2_cnn_flow(os.path.join(DIAGRAMS_DIR, "cnn_flow.png"))
    diagram3_svm_flow(os.path.join(DIAGRAMS_DIR, "svm_flow.png"))
    diagram4_cnn_svm_flow(os.path.join(DIAGRAMS_DIR, "cnn_svm_flow.png"))

    log.info("All diagrams generated in: %s", DIAGRAMS_DIR)


if __name__ == "__main__":
    run_generate_diagrams()
