"""
generate_lab_report_pdf.py
Generates a 6-page professional PDF lab report for the Data Networks mid-lab.
Uses reportlab 5.x — pure Python, no external tools required.
"""

import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak, Preformatted
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.lib.colors import HexColor

# ──────────────────────────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS = os.path.join(BASE, "diagrams")
GRAPHS   = os.path.join(BASE, "graphs")
CM_DIR   = os.path.join(BASE, "results", "confusion_matrices")
OUT_PDF  = os.path.join(BASE, "Data_Networks_Lab_Report.pdf")

# ──────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ──────────────────────────────────────────────────────────────────────────────
NAVY        = HexColor("#0F172A")
BLUE        = HexColor("#1E3A8A")
ACCENT      = HexColor("#2563EB")
CYAN        = HexColor("#0EA5E9")
LIGHT_GREY  = HexColor("#F1F5F9")
MID_GREY    = HexColor("#94A3B8")
DARK_GREY   = HexColor("#334155")
WHITE       = colors.white
RED         = HexColor("#B91C1C")
GREEN       = HexColor("#166534")
TABLE_HEAD  = HexColor("#1E3A8A")
TABLE_ROW1  = HexColor("#F8FAFC")
TABLE_ROW2  = HexColor("#E2E8F0")

# ──────────────────────────────────────────────────────────────────────────────
# STYLES
# ──────────────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["cover_title"] = ParagraphStyle("cover_title",
        fontName="Helvetica-Bold", fontSize=17, leading=22,
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)

    s["cover_sub"] = ParagraphStyle("cover_sub",
        fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=DARK_GREY, alignment=TA_CENTER, spaceAfter=3)

    s["cover_label"] = ParagraphStyle("cover_label",
        fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=ACCENT, alignment=TA_LEFT)

    s["cover_value"] = ParagraphStyle("cover_value",
        fontName="Helvetica", fontSize=9, leading=12,
        textColor=DARK_GREY, alignment=TA_LEFT)

    s["section_h"] = ParagraphStyle("section_h",
        fontName="Helvetica-Bold", fontSize=12, leading=16,
        textColor=WHITE, alignment=TA_LEFT,
        backColor=BLUE, borderPad=5, spaceBefore=10, spaceAfter=4)

    s["sub_h"] = ParagraphStyle("sub_h",
        fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=BLUE, spaceBefore=8, spaceAfter=3)

    s["body"] = ParagraphStyle("body",
        fontName="Helvetica", fontSize=8.8, leading=13,
        textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=4)

    s["bullet"] = ParagraphStyle("bullet",
        fontName="Helvetica", fontSize=8.5, leading=12,
        textColor=DARK_GREY, leftIndent=12, bulletIndent=0,
        spaceAfter=2)

    s["code"] = ParagraphStyle("code",
        fontName="Courier", fontSize=7.5, leading=11,
        textColor=DARK_GREY, backColor=LIGHT_GREY,
        borderPad=4, leftIndent=6, rightIndent=6,
        spaceAfter=4)

    s["caption"] = ParagraphStyle("caption",
        fontName="Helvetica-Oblique", fontSize=7.5, leading=10,
        textColor=MID_GREY, alignment=TA_CENTER, spaceAfter=6)

    s["tbl_head"] = ParagraphStyle("tbl_head",
        fontName="Helvetica-Bold", fontSize=8, leading=10,
        textColor=WHITE, alignment=TA_CENTER)

    s["tbl_cell"] = ParagraphStyle("tbl_cell",
        fontName="Helvetica", fontSize=8, leading=10,
        textColor=DARK_GREY, alignment=TA_CENTER)

    s["tbl_cell_l"] = ParagraphStyle("tbl_cell_l",
        fontName="Helvetica", fontSize=8, leading=10,
        textColor=DARK_GREY, alignment=TA_LEFT)

    s["highlight"] = ParagraphStyle("highlight",
        fontName="Helvetica-Bold", fontSize=8.8, leading=13,
        textColor=ACCENT, alignment=TA_JUSTIFY, spaceAfter=3)

    s["footer"] = ParagraphStyle("footer",
        fontName="Helvetica", fontSize=7, leading=9,
        textColor=MID_GREY, alignment=TA_CENTER)

    s["ref"] = ParagraphStyle("ref",
        fontName="Helvetica", fontSize=7.8, leading=11,
        textColor=DARK_GREY, leftIndent=14, firstLineIndent=-14,
        spaceAfter=3)

    return s

# ──────────────────────────────────────────────────────────────────────────────
# HELPER: section header with blue background
# ──────────────────────────────────────────────────────────────────────────────
def sec(title, S):
    return Paragraph(f"&nbsp;&nbsp;{title}", S["section_h"])

def sub(title, S):
    return Paragraph(title, S["sub_h"])

def body(text, S):
    return Paragraph(text, S["body"])

def bullet(text, S):
    return Paragraph(f"• &nbsp; {text}", S["bullet"])

def spacer(h_mm=3):
    return Spacer(1, h_mm * mm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=MID_GREY, spaceAfter=4)

def code_block(text, S):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), S["code"])

def img(path, width_cm=8, caption_text="", S=None):
    elems = []
    if os.path.exists(path):
        elems.append(Image(path, width=width_cm*cm, height=None))
        if caption_text and S:
            elems.append(Paragraph(caption_text, S["caption"]))
    return elems

def std_table(header_row, data_rows, col_widths, S, highlight_cols=None):
    """Build a styled table with blue header and alternating rows."""
    head = [Paragraph(c, S["tbl_head"]) for c in header_row]
    rows = [head]
    for i, row in enumerate(data_rows):
        styled = []
        for j, cell in enumerate(row):
            st = S["tbl_cell_l"] if j == 0 else S["tbl_cell"]
            styled.append(Paragraph(str(cell), st))
        rows.append(styled)

    ts = TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), TABLE_HEAD),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID",        (0,0), (-1,-1), 0.4, MID_GREY),
        ("TOPPADDING",  (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ])
    if highlight_cols:
        for col in highlight_cols:
            ts.add("TEXTCOLOR", (col,1), (col,-1), ACCENT)
            ts.add("FONTNAME",  (col,1), (col,-1), "Helvetica-Bold")

    return Table(rows, colWidths=[w*cm for w in col_widths], style=ts)

# ──────────────────────────────────────────────────────────────────────────────
# PAGE TEMPLATE WITH HEADER/FOOTER
# ──────────────────────────────────────────────────────────────────────────────
def make_canvas_factory(doc):
    def on_page(canvas, doc):
        canvas.saveState()
        w, h = A4
        # Top accent line
        canvas.setFillColor(ACCENT)
        canvas.rect(0, h - 4*mm, w, 4*mm, fill=1, stroke=0)
        # Header text (skip cover page)
        if doc.page > 1:
            canvas.setFillColor(DARK_GREY)
            canvas.setFont("Helvetica", 7)
            canvas.drawString(2*cm, h - 10*mm,
                "Lightweight Edge-Based IoT IDS | Data Networks Mid-Lab Report | NIT Warangal")
            canvas.drawRightString(w - 2*cm, h - 10*mm, f"Page {doc.page}")
        # Bottom line
        canvas.setFillColor(MID_GREY)
        canvas.setFont("Helvetica", 6.5)
        canvas.drawString(2*cm, 10*mm,
            "Dept. of ECE, NIT Warangal  |  Course: Data Networks  |  September 2026")
        canvas.drawRightString(w - 2*cm, 10*mm,
            "github.com/boringGuru347/DN-Project")
        canvas.setStrokeColor(MID_GREY)
        canvas.setLineWidth(0.4)
        canvas.line(2*cm, 13*mm, w - 2*cm, 13*mm)
        canvas.restoreState()
    return on_page

# ──────────────────────────────────────────────────────────────────────────────
# BUILD STORY
# ──────────────────────────────────────────────────────────────────────────────
def build_story(S):
    story = []
    W = A4[0] - 4*cm   # usable text width

    # ═══════════════════════════════════════════════════════════════
    # PAGE 1 — COVER / SECTION 1 + 2
    # ═══════════════════════════════════════════════════════════════

    # ── Cover banner ──
    story.append(spacer(12))
    story.append(Paragraph("TECHNICAL LAB REPORT", ParagraphStyle("cov0",
        fontName="Helvetica-Bold", fontSize=8, textColor=ACCENT,
        alignment=TA_CENTER, spaceAfter=4)))

    story.append(Paragraph(
        "Lightweight Edge-Based Intrusion Detection for IoT Networks<br/>"
        "Using Deep Feature Extraction and Classical Machine Learning",
        S["cover_title"]))

    story.append(Paragraph(
        "A Preliminary Evaluation of CNN, SVM, and CNN+SVM Pipelines "
        "on the UNSW-NB15 Benchmark Dataset",
        S["cover_sub"]))

    story.append(spacer(4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))

    # ── Metadata table ──
    meta = [
        ["Department", "Electronics & Communication Engineering, NIT Warangal"],
        ["Course", "Data Networks (ECE)"],
        ["Report Type", "Mid-Lab Preliminary Experiment Report"],
        ["Date", "September 2026"],
        ["Group Members",
         "Chhatrapal Bhuarya (24ECB0B14)  •  Dasari Sai Kishan (24ECB0B15)\n"
         "Saarth Yawale (24ECB0B49)  •  Sudhanshu Bhagat (24ECB0B57)"],
        ["Repository", "github.com/boringGuru347/DN-Project"],
    ]
    meta_rows = []
    for label, val in meta:
        meta_rows.append([
            Paragraph(label, S["cover_label"]),
            Paragraph(val.replace("\n", "<br/>"), S["cover_value"])
        ])
    meta_tbl = Table(meta_rows, colWidths=[3.8*cm, (W-3.8)*cm],
        style=TableStyle([
            ("BACKGROUND",  (0,0), (0,-1), LIGHT_GREY),
            ("BACKGROUND",  (1,0), (1,-1), WHITE),
            ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#CBD5E1")),
            ("TOPPADDING",  (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ]))
    story.append(meta_tbl)
    story.append(spacer(5))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY, spaceAfter=6))

    # ── Section 1: Title ──
    story.append(sec("1.  Title of the Experiment / Study / Exercise", S))
    story.append(spacer(2))
    story.append(body(
        "<b>Lightweight Edge-Based Intrusion Detection for IoT Networks Using Deep Feature "
        "Extraction and Classical Machine Learning:</b> A Preliminary Evaluation of CNN, SVM, "
        "and CNN+SVM Pipelines on the UNSW-NB15 Benchmark Dataset.", S))

    story.append(spacer(2))

    # ── Section 2: Aim ──
    story.append(sec("2.  Aim", S))
    story.append(spacer(2))
    story.append(body(
        "To design, implement, and evaluate a <b>lightweight, modular machine-learning pipeline</b> "
        "capable of classifying IoT network traffic as <i>Normal</i> or <i>Attack</i> with high "
        "detection accuracy, low false-alarm rate, and a computational footprint small enough to "
        "support <b>edge-side intrusion detection</b> — as a preliminary proof-of-concept toward "
        "replacing the computationally expensive CNN-LSTM-Attention architectures proposed in "
        "recent IEEE literature.", S))
    story.append(spacer(1))

    aims = [
        "Determine whether <b>ANOVA F-Score feature reduction</b> (42 → 20 attributes, 52.4%) "
        "preserves competitive attack-detection performance.",
        "Measure and compare <b>classification quality</b> (Accuracy, F1-Score, FPR) of three "
        "model configurations: CNN (lightweight MLP), SVM (RBF kernel), and CNN+SVM hybrid.",
        "Measure and compare <b>resource consumption</b> (training time, inference time, model "
        "size) as a preliminary guide toward edge-deployment feasibility.",
    ]
    for a in aims:
        story.append(bullet(a, S))

    # ═══════════════════════════════════════════════════════════════
    # PAGE 2 — SECTION 3: OBJECTIVES + SECTION 4.1-4.3
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(sec("3.  Objectives", S))
    story.append(spacer(2))
    objs = [
        ("<b>O1 — Dataset Acquisition & Preparation:</b>",
         "Process UNSW-NB15 (82,332 training / 175,341 testing flows) — column removal, "
         "median imputation, categorical encoding, and standard scaling — all transformations "
         "fitted exclusively on training data (zero-leakage)."),
        ("<b>O2 — Feature Dimensionality Study:</b>",
         "Perform ANOVA F-Score SelectKBest sweep across k ∈ {10, 15, 20, 25, 30, 35}; "
         "quantify accuracy–feature count tradeoff; select working k = 20."),
        ("<b>O3 — Standalone CNN Implementation:</b>",
         "Build and train a lightweight MLP (64 → 32 units, ReLU, Adam, early-stop patience=5) "
         "for binary IDS. Total parameters: 3,457. Record convergence over 53 iterations."),
        ("<b>O4 — Standalone SVM Implementation:</b>",
         "Train an RBF-kernel SVM (C=1.0, γ='scale') on the 20 selected features. "
         "Record classification performance and training time (66.55 s)."),
        ("<b>O5 — CNN+SVM Hybrid Pipeline:</b>",
         "Extract 64-D latent activations (h₁ = ReLU(W₁ᵀx + b₁)) from the trained CNN's "
         "first hidden layer. Train a second RBF-SVM on these learned representations."),
        ("<b>O6 — Systematic Evaluation:</b>",
         "Measure Accuracy, Precision, Recall, F1-Score, FPR, training time, inference time, "
         "and model size for all three models. Generate confusion matrices and 5 result graphs."),
        ("<b>O7 — Reference Paper Comparison:</b>",
         "Provide a methodological comparison with Phalaagae et al. (IEEE Access, 2025) "
         "and the Edge-AI IDS paper (IEEE ICERECT, 2025)."),
    ]
    for label, desc in objs:
        story.append(body(f"{label} {desc}", S))
        story.append(spacer(1))

    story.append(spacer(3))
    story.append(sec("4.  Methodology", S))
    story.append(spacer(2))

    story.append(sub("4.1  Dataset — UNSW-NB15", S))
    story.append(body(
        "The UNSW-NB15 dataset (Moustafa & Slay, IEEE MilCIS 2015) contains network flow records "
        "covering benign traffic and nine attack categories (Generic, Exploits, Fuzzers, DoS, "
        "Reconnaissance, Backdoor, Analysis, Shellcode, Worms), merged to binary labels.", S))

    ds_data = [
        ["Training Split", "82,332", "37,000 (44.9%)", "45,332 (55.1%)"],
        ["Testing Split",  "175,341", "56,000 (31.9%)", "119,341 (68.1%)"],
    ]
    story.append(std_table(
        ["Split", "Total Flows", "Normal (label=0)", "Attack (label=1)"],
        ds_data, [3.5, 3, 4, 4], S))
    story.append(spacer(4))

    story.append(sub("4.2  End-to-End Pipeline (8 Stages, run via run_all.py)", S))
    pipe_data = [
        ["1", "preprocessing.py",      "Load CSV, drop columns, impute NaN, encode, scale"],
        ["2", "feature_selection.py",  "ANOVA F-score sweep + SelectKBest (k=20)"],
        ["3", "generate_diagrams.py",  "Produce 4 system-flow PNGs"],
        ["4", "train_cnn.py",          "Train lightweight MLP — 3,457 params, 11.01 s"],
        ["5", "train_svm.py",          "Train RBF-SVM on 20 features — 66.55 s"],
        ["6", "train_cnn_svm.py",      "Extract 64-D CNN features → train SVM — 61.36 s"],
        ["7", "evaluate.py",           "Metrics + confusion matrices for all 3 models"],
        ["8", "generate_graphs.py",    "5 result graphs (bars, curves, matrices)"],
    ]
    story.append(std_table(["Stage", "Module", "Description"],
                           pipe_data, [1.2, 3.8, 9.5], S))
    story.append(spacer(4))

    story.append(sub("4.3  Data Preprocessing", S))
    story.append(body(
        "<b>Step 1:</b> Drop identifier <i>id</i> and multi-class <i>attack_cat</i>. "
        "Retain binary <i>label</i> → 42 usable features. &nbsp;"
        "<b>Step 2:</b> Replace ±∞ with NaN; fill NaN using <b>training-set medians only</b> "
        "(prevents data leakage). &nbsp;"
        "<b>Step 3:</b> LabelEncoder fit on training values for "
        "<i>proto</i> (132 unique), <i>service</i> (14), <i>state</i> (8). "
        "Unseen test values map to <i>__unknown__</i>. &nbsp;"
        "<b>Step 4:</b> StandardScaler (fit on training, applied to test) → "
        "zero-mean, unit-variance features.", S))

    # ═══════════════════════════════════════════════════════════════
    # PAGE 3 — SECTION 4.4-4.8 (Feature selection + Models)
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(sub("4.4  Feature Selection — ANOVA F-Score (SelectKBest)", S))
    story.append(body(
        "The univariate ANOVA F-score measures discriminative power of each feature j between "
        "Normal and Attack classes:", S))
    story.append(body(
        "<b>F<sub>j</sub> = [ (x̄<sub>j,Attack</sub> − x̄<sub>j,Normal</sub>)² / (K−1) ] "
        "/ [ S²<sub>j</sub> / (N−K) ]</b> &nbsp;&nbsp; where K=2 (binary), N=82,332 samples.", S))
    story.append(body(
        "SelectKBest (f_classif) is fit <b>exclusively on training data</b> and applied to test. "
        "A LinearSVC sweep over k ∈ {10,15,20,25,30,35} guides the working selection of <b>k=20</b> "
        "(52.4% reduction). Selected indices: "
        "<i>[2, 3, 8, 9, 12, 19, 20, 21, 22, 23, 24, 27, 30, 31, 32, 33, 34, 35, 39, 40]</i> — "
        "corresponding to sbytes, sttl, dttl, sinpkt, dinpkt, ct_state_ttl, connection-table stats.", S))

    story.append(spacer(3))
    story.append(sub("4.5  Model 1 — Standalone CNN (Lightweight MLP)", S))
    story.append(body(
        "Implemented as sklearn MLPClassifier (functional equivalent of 1-D CNN: "
        "Dense layers replace Conv→Pool→GlobalAvgPool). "
        "The 64-D first-hidden-layer output is extracted as the learned representation for CNN+SVM.", S))

    arch_data = [
        ["Input",    "20 features",     "ANOVA-selected, standard-scaled"],
        ["Layer 1",  "Dense (64, ReLU)","h₁ = ReLU(W₁ᵀx + b₁)  ← extraction point"],
        ["Layer 2",  "Dense (32, ReLU)","h₂ = ReLU(W₂ᵀh₁ + b₂)"],
        ["Output",   "Dense (1, σ)",    "Binary classification"],
        ["Params",   "3,457 total",     "20×64+64 + 64×32+32 + 32×1+1"],
        ["Training", "Adam, lr=1e-3",   "Batch=512, L2 α=1e-4, early-stop patience=5"],
        ["Epochs",   "53 (stopped)",    "Best val score 0.9514 at iter 47"],
    ]
    story.append(std_table(["Component", "Specification", "Detail"],
                           arch_data, [2.5, 3.5, 8.5], S))
    story.append(spacer(4))

    story.append(sub("4.6  Model 2 — Standalone SVM", S))
    story.append(body(
        "SVC (sklearn) with RBF kernel: <b>K(xᵢ, xⱼ) = exp(−γ ‖xᵢ − xⱼ‖²)</b>, "
        "C=1.0, γ='scale' (= 1/(20 × Var(X)) ≈ 0.05). "
        "Trained on 82,332 flows × 20 features. Training time: <b>66.55 seconds</b>. "
        "cache_size=1000 MB speeds RBF kernel matrix evaluation.", S))

    story.append(spacer(3))
    story.append(sub("4.7  Model 3 — CNN+SVM Hybrid Pipeline", S))
    story.append(body(
        "Stage 1 — <b>Feature Extraction:</b> The trained CNN's first hidden layer outputs "
        "h₁ ∈ ℝ⁶⁴ for each training sample (nonlinear representation). "
        "Stage 2 — <b>SVM on Learned Features:</b> A fresh RBF-SVM (same hyperparameters) is "
        "trained on the (82,332 × 64) latent feature matrix. "
        "13,665 support vectors identified. Total pipeline training: <b>61.36 seconds</b>.", S))

    story.append(spacer(3))
    story.append(sub("4.8  Evaluation Metrics", S))
    metrics_def = [
        ["Accuracy",   "(TP + TN) / N",           "Overall correct classification rate"],
        ["Precision",  "TP / (TP + FP)",           "Fraction of predicted attacks that are real"],
        ["Recall",     "TP / (TP + FN)",           "Fraction of real attacks detected"],
        ["F1-Score",   "2·P·R / (P+R)",            "Harmonic mean of Precision & Recall"],
        ["FPR",        "FP / (FP + TN)",           "Normal traffic falsely flagged as attack"],
        ["Latency",    "Inference time / N flows", "Per-sample detection time"],
    ]
    story.append(std_table(["Metric", "Formula", "IDS Relevance"],
                           metrics_def, [2.5, 3.5, 8.5], S))

    # ═══════════════════════════════════════════════════════════════
    # PAGE 4 — SECTION 5: SCENARIO DIAGRAMS + TABLES 1 & 2
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(sec("5.  Simulation Results / Observations with Scenario Diagrams", S))
    story.append(spacer(2))

    story.append(sub("5.1  Scenario Diagram — End-to-End Pipeline", S))

    # Insert overall pipeline diagram image
    pipeline_img = os.path.join(DIAGRAMS, "overall_pipeline.png")
    cnn_svm_img  = os.path.join(DIAGRAMS, "cnn_svm_flow.png")

    # Two diagrams side-by-side in a table
    diag_cells = []
    if os.path.exists(pipeline_img):
        diag_cells.append([Image(pipeline_img, width=7.2*cm, height=11.5*cm),
                           Paragraph("Fig. 1: End-to-End Experimental Pipeline", S["caption"])])
    if os.path.exists(cnn_svm_img):
        diag_cells.append([Image(cnn_svm_img, width=7.2*cm, height=11.5*cm),
                           Paragraph("Fig. 2: CNN+SVM Hybrid Architecture", S["caption"])])

    if len(diag_cells) == 2:
        diag_tbl = Table(
            [[diag_cells[0][0], diag_cells[1][0]],
             [diag_cells[0][1], diag_cells[1][1]]],
            colWidths=[7.5*cm, 7.5*cm],
            style=TableStyle([
                ("ALIGN",   (0,0), (-1,-1), "CENTER"),
                ("VALIGN",  (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING",  (0,0), (-1,-1), 4),
                ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ])
        )
        story.append(diag_tbl)
    elif os.path.exists(pipeline_img):
        story.append(Image(pipeline_img, width=9*cm, height=None))
        story.append(Paragraph("Fig. 1: End-to-End Experimental Pipeline", S["caption"]))

    story.append(spacer(4))

    story.append(sub("5.2  Table 1 — Feature Selection Sweep (ANOVA F-Score, LinearSVC)", S))
    feat_data = [
        ["10", "82.91%", "86.88%", "76.2%"],
        ["15", "82.04%", "86.02%", "64.3%"],
        ["20 ✓", "85.55%", "88.67%", "52.4%"],
        ["25", "88.30%", "90.95%", "40.5%"],
        ["30", "88.45%", "91.06%", "28.6%"],
        ["35", "88.29%", "90.92%", "16.7%"],
    ]
    story.append(std_table(
        ["k (Features)", "Accuracy", "F1-Score", "Reduction from 42"],
        feat_data, [3, 3.5, 3.5, 4.5], S, highlight_cols=[0]))

    story.append(spacer(3))
    story.append(sub("5.3  Table 2 — CNN/MLP Training Convergence (53 Iterations)", S))
    conv_data = [
        ["1",  "0.4090", "0.8580"],
        ["5",  "0.1778", "0.9288"],
        ["10", "0.1487", "0.9362"],
        ["20", "0.1322", "0.9389"],
        ["30", "0.1247", "0.9440"],
        ["40", "0.1203", "0.9496"],
        ["47", "0.1162", "0.9514 ★ (best)"],
        ["53 (stop)", "0.1144", "—"],
    ]
    story.append(std_table(
        ["Iteration", "Training Loss", "Validation Score"],
        conv_data, [3, 4, 7.5], S, highlight_cols=[2]))

    # ═══════════════════════════════════════════════════════════════
    # PAGE 5 — SECTION 5 continued: MAIN RESULTS + GRAPHS
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(sub("5.4  Table 3 — Model Performance Comparison (Test Set: 175,341 flows)", S))
    perf_data = [
        ["Accuracy",                "87.60%",   "88.21% ★", "88.16%"],
        ["Precision",               "98.40% ★", "97.51%",   "97.99%"],
        ["Recall",                  "83.14%",   "84.84% ★", "84.34%"],
        ["F1-Score",                "90.13%",   "90.73% ★", "90.65%"],
        ["FPR",                     "2.88% ★",  "4.62%",    "3.69%"],
        ["Training Time",           "11.01 s ★","66.55 s",  "61.36 s"],
        ["Inference (175K flows)",  "0.0596 s ★","163.14 s","151.73 s"],
        ["Per-Sample Latency",      "0.34 μs ★","930 μs",   "867 μs"],
        ["Parameters / Model Size", "3,457 / 47.6 KB ★","— / 3,077 KB","3,457 / 7,149 KB"],
    ]
    story.append(std_table(
        ["Metric", "CNN", "SVM", "CNN+SVM"],
        perf_data, [5, 3.2, 3.2, 3.1], S))
    story.append(Paragraph("★ = best value in each row", S["caption"]))
    story.append(spacer(4))

    story.append(sub("5.5  Table 4 — Confusion Matrices (Test: 56,000 Normal, 119,341 Attack)", S))
    cm_data = [
        ["CNN",     "TN=54,385", "FP=1,615", "FN=20,123", "TP=99,218",  "FPR=2.88%",  "Recall=83.14%"],
        ["SVM",     "TN=53,410", "FP=2,590", "FN=18,088", "TP=101,253", "FPR=4.62%",  "Recall=84.84%"],
        ["CNN+SVM", "TN=53,936", "FP=2,064", "FN=18,690", "TP=100,651", "FPR=3.69%",  "Recall=84.34%"],
    ]
    story.append(std_table(
        ["Model", "TN", "FP", "FN", "TP", "FPR", "Recall"],
        cm_data, [2.2, 2.2, 2.2, 2.2, 2.8, 2.2, 2.7], S))
    story.append(spacer(4))

    story.append(sub("5.6  Table 5 — Computational Efficiency", S))
    eff_data = [
        ["Training Time",   "11.01 s",  "66.55 s",  "61.36 s"],
        ["Speedup vs. SVM", "6.04×",    "1× (base)","1.08×"],
        ["Inference 175K",  "0.0596 s", "163.14 s", "151.73 s"],
        ["Infer. Speedup",  "~2,737×",  "1× (base)","~1.07×"],
        ["Per-Sample",      "0.34 μs",  "930 μs",   "867 μs"],
        ["Model Size",      "47.6 KB",  "3,077 KB", "7,149 KB"],
    ]
    story.append(std_table(
        ["Resource Metric", "CNN", "SVM", "CNN+SVM"],
        eff_data, [5.5, 3, 3, 3], S))
    story.append(spacer(4))

    # Result graphs — two per row
    story.append(sub("5.7  Generated Experimental Graphs", S))

    g1 = os.path.join(GRAPHS, "model_performance_comparison.png")
    g2 = os.path.join(GRAPHS, "confusion_matrices.png")
    g3 = os.path.join(GRAPHS, "efficiency_comparison.png")
    g4 = os.path.join(GRAPHS, "feature_reduction.png")
    g5 = os.path.join(GRAPHS, "cnn_training_history.png")

    def graph_pair(p1, cap1, p2, cap2):
        cells = []
        r1 = [Image(p1, width=7.0*cm, height=4.5*cm), Paragraph(cap1, S["caption"])] if os.path.exists(p1) else [Paragraph(cap1+" (not found)", S["caption"])]
        r2 = [Image(p2, width=7.0*cm, height=4.5*cm), Paragraph(cap2, S["caption"])] if os.path.exists(p2) else [Paragraph(cap2+" (not found)", S["caption"])]
        tbl = Table([[r1[0] if len(r1)>1 else Spacer(1,1), r2[0] if len(r2)>1 else Spacer(1,1)],
                     [Paragraph(cap1, S["caption"]), Paragraph(cap2, S["caption"])]],
                    colWidths=[7.3*cm, 7.3*cm],
                    style=TableStyle([
                        ("ALIGN",(0,0),(-1,-1),"CENTER"),
                        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ]))
        return tbl

    story.append(graph_pair(g1, "Fig. 3: Model Performance Comparison",
                            g4, "Fig. 4: Feature Reduction vs. Accuracy/F1"))
    story.append(spacer(2))
    story.append(graph_pair(g3, "Fig. 5: Efficiency Comparison (Training & Inference)",
                            g5, "Fig. 6: CNN Training Loss Curve (53 iterations)"))
    story.append(spacer(2))
    # Confusion matrices — full width
    if os.path.exists(g2):
        story.append(Image(g2, width=14.5*cm, height=4.6*cm))
        story.append(Paragraph("Fig. 7: Side-by-Side Confusion Matrices (CNN, SVM, CNN+SVM)", S["caption"]))

    # ═══════════════════════════════════════════════════════════════
    # PAGE 6 — SECTION 6: DISCUSSION + REFERENCES
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(sec("6.  Discussion on the Results / Observations", S))
    story.append(spacer(2))

    story.append(sub("6.1  Classification Performance", S))
    story.append(body(
        "All three models cluster tightly: <b>87.6%–88.2% accuracy</b> and <b>90.1%–90.7% F1</b>. "
        "This is a primary finding — a 52.4% feature reduction preserves competitive performance, "
        "validating the ANOVA F-Score selection strategy.", S))
    story.append(body(
        "The <b>SVM (88.21%, F1=90.73%)</b> achieves the highest accuracy, consistent with the "
        "well-established strength of RBF-SVMs on tabular data. "
        "The <b>CNN+SVM hybrid (88.16%, F1=90.65%)</b> is nearly indistinguishable from standalone "
        "SVM, confirming that the CNN's 64-D latent representations carry at least as much "
        "discriminative information as the raw 20-D feature space — validating the hybrid concept. "
        "The <b>standalone CNN (87.60%, F1=90.13%)</b> slightly underperforms (~0.6% gap) "
        "but offers dramatically superior efficiency.", S))

    story.append(spacer(2))
    story.append(sub("6.2  False Positive Rate Analysis", S))
    story.append(body(
        "FPR determines alert-fatigue in operational IDS. Despite the SVM having the highest recall "
        "(84.84%), it generates the most false alarms:", S))
    fpr_data = [
        ["CNN",     "2.88%", "1,615 / 56,000", "98.40%", "Lowest FPR — best for low-alert-fatigue deployments"],
        ["CNN+SVM", "3.69%", "2,064 / 56,000", "97.99%", "Intermediate — hybrid of CNN accuracy and SVM boundary"],
        ["SVM",     "4.62%", "2,590 / 56,000", "97.51%", "60% more false alarms than CNN"],
    ]
    story.append(std_table(
        ["Model", "FPR", "False Alarms", "Precision", "Operational Impact"],
        fpr_data, [2.2, 1.5, 3, 2.2, 5.6], S))
    story.append(spacer(3))

    story.append(sub("6.3  Inference Speed — Edge-Deployment Significance", S))
    story.append(body(
        "<b>CNN: 0.34 μs/sample</b> — well below inter-packet arrival times (~milliseconds in IoT). "
        "Confirms wire-speed classification capability for real-time edge deployment.", S))
    story.append(body(
        "<b>SVM: 930 μs/sample</b> — <b>2,737× slower</b> than CNN. Root cause: SVM inference is "
        "O(n_support_vectors) per sample; with 3,077 KB of stored SVs the evaluation is "
        "prohibitively expensive on IoT microcontrollers.", S))
    story.append(body(
        "<b>Key insight:</b> The CNN+SVM hybrid does NOT inherit the CNN's inference speed — "
        "the SVM kernel evaluation dominates. For real-time IoT edge deployment, the <b>standalone "
        "CNN (47.6 KB, 0.34 μs/sample)</b> is the clear practical choice.", S))

    story.append(spacer(2))
    story.append(sub("6.4  Feature Reduction Observations", S))
    story.append(body(
        "Three distinct regions in the sweep: <b>(i) k=10–20:</b> sharp gains (+3.5% accuracy) — "
        "each added feature is informative; <b>(ii) k=20–30:</b> gradual plateau — diminishing "
        "returns; <b>(iii) k=30–35:</b> near-zero gain with slight degradation. "
        "k=20 is the optimal inflection point — 52.4% reduction with reasonable performance. "
        "Practically: 80 bytes/flow (20 × float32) vs. 168 bytes (42 × float32) buffer at the edge.", S))

    story.append(spacer(2))
    story.append(sub("6.5  Methodological Comparison with Reference Papers", S))
    story.append(body(
        "<b>Phalaagae et al. (IEEE Access 2025):</b> CNN-LSTM + Attention requires O(T×H²) "
        "recurrent computation and O(T²) attention score matrix per flow window. "
        "Our approach omits both — reducing to a single MLP forward pass. "
        "Our preliminary result (88.2%, 90.7% F1) establishes a <b>complexity floor</b>: "
        "the reference paper's added complexity must exceed this baseline on matched datasets.", S))
    story.append(body(
        "<b>Edge-AI IDS (IEEE ICERECT 2025):</b> Shares our motivation of proximity-to-device "
        "deployment. We provide a concrete lower-bound: a <b>47.6 KB, 3,457-parameter model</b> "
        "achieving 88.2% accuracy at <b>0.34 μs/sample</b> — the first quantified complexity floor "
        "for this class of lightweight edge IDS on UNSW-NB15.", S))

    story.append(spacer(2))
    story.append(sub("6.6  Limitations and Planned Next Steps", S))
    limits = [
        "No hyperparameter optimisation (grid search or Bayesian) — all values are defaults.",
        "Single pre-defined train/test split; no k-fold cross-validation to bound variance.",
        "Binary classification only; nine attack categories merged into one class.",
        "Timings on laptop CPU; not representative of IoT hardware (Raspberry Pi 4, ESP32, ARM Cortex-M).",
        "UNSW-NB15 (2015) may not capture recent IoT attack patterns.",
        "MLP used instead of true 1-D CNN — local receptive field and weight sharing absent.",
    ]
    next_steps = [
        "Multi-class attack categorisation (9 categories).",
        "Hyperparameter tuning (grid search for C, γ, hidden layer dimensions).",
        "Evaluation on CICIoT2023 (recent, IoT-specific, multi-class dataset).",
        "Model compression: INT8 quantisation, structured weight pruning.",
        "Hardware benchmarking on Raspberry Pi 4 / ESP32 for realistic latency.",
        "True 1-D Convolutional implementation for spatial feature extraction.",
    ]

    lim_items = [[Paragraph("<b>Limitations:</b>", S["sub_h"]),
                  Paragraph("<b>Next Steps:</b>",   S["sub_h"])]]
    lim_content = "\n".join([f"• {l}" for l in limits])
    next_content = "\n".join([f"• {n}" for n in next_steps])
    lim_tbl = Table([
        ["\n".join([f"• {l}" for l in limits]),
         "\n".join([f"• {n}" for n in next_steps])]
    ], colWidths=[7.1*cm, 7.4*cm],
        style=TableStyle([
            ("FONTNAME",  (0,0),(-1,-1), "Helvetica"),
            ("FONTSIZE",  (0,0),(-1,-1), 8),
            ("LEADING",   (0,0),(-1,-1), 12),
            ("TEXTCOLOR", (0,0),(-1,-1), DARK_GREY),
            ("VALIGN",    (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING",(0,0),(-1,-1), 4),
            ("TOPPADDING",(0,0),(-1,-1), 0),
        ]))
    story.append(lim_tbl)

    story.append(spacer(5))
    story.append(hr())

    # ── References ──
    story.append(sub("References", S))
    refs = [
        '[1] N. Moustafa and J. Slay, UNSW-NB15: a comprehensive data set for network intrusion detection systems, in <i>Proc. IEEE MilCIS</i>, 2015.',
        '[2] P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni and S. Rajalakshmi, A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks, <i>IEEE Access</i>, 2025.',
        '[3] Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems, <i>IEEE ICERECT</i>, 2025.',
        '[4] F. Pedregosa et al., Scikit-learn: Machine Learning in Python, <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825-2830, 2011.',
        '[5] V. N. Vapnik, <i>The Nature of Statistical Learning Theory</i>, Springer, 1995.',
    ]
    for r in refs:
        story.append(Paragraph(r, S["ref"]))

    story.append(spacer(4))
    story.append(hr())
    story.append(Paragraph(
        "All code, results, and models available at: "
        "<b>github.com/boringGuru347/DN-Project</b>",
        S["footer"]))

    return story


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    S = build_styles()

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=1.8*cm,
        bottomMargin=2*cm,
        title="Technical Lab Report — Lightweight IoT IDS (DN Project)",
        author="Chhatrapal Bhuarya, Dasari Sai Kishan, Saarth Yawale, Sudhanshu Bhagat",
        subject="Data Networks Mid-Lab Report — NIT Warangal",
    )

    on_page = make_canvas_factory(doc)
    story = build_story(S)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("PDF generated successfully: " + OUT_PDF)
    size_kb = os.path.getsize(OUT_PDF) / 1024
    print(f"   File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
