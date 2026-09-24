"""
build_simple_ieee_report.py
Generates a simple, elegant IEEE-style lab report PDF.
Maximum 6 pages. Covers all 6 required sections from the instructor's instructions:
1. Title of the experiment/study/exercise
2. Aim
3. Objectives
4. Methodology
5. Simulation results/observations along with scenario diagram
6. Discussion on the results/observation
"""

import os, sys, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
GRAPHS_DIR   = os.path.join(BASE_DIR, "graphs")
PDF_PATH     = os.path.join(BASE_DIR, "Data_Networks_Lab_Report.pdf")

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = A4
        self.setFont("Times-Roman", 8)
        self.setFillColor(colors.HexColor("#333333"))

        # Running header on pages 2..N
        if self._pageNumber > 1:
            self.drawString(2.0*cm, h - 1.2*cm, "Data Networks Course Project — Mid-Lab Technical Report")
            self.drawRightString(w - 2.0*cm, h - 1.2*cm, "Dept. of ECE, NIT Warangal")
            self.setStrokeColor(colors.HexColor("#999999"))
            self.setLineWidth(0.4)
            self.line(2.0*cm, h - 1.35*cm, w - 2.0*cm, h - 1.35*cm)

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#999999"))
        self.setLineWidth(0.4)
        self.line(2.0*cm, 1.5*cm, w - 2.0*cm, 1.5*cm)

        self.drawString(2.0*cm, 1.1*cm, "UNSW-NB15 IoT Intrusion Detection Study")
        self.drawRightString(w - 2.0*cm, 1.1*cm, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def get_styles():
    s = {}
    # IEEE Document Title
    s["title"] = ParagraphStyle("ieee_title",
        fontName="Times-Bold", fontSize=15, leading=19,
        alignment=TA_CENTER, textColor=colors.black, spaceAfter=6)

    # Authors & Affiliation
    s["author"] = ParagraphStyle("ieee_author",
        fontName="Times-Roman", fontSize=9.5, leading=13,
        alignment=TA_CENTER, textColor=colors.black, spaceAfter=2)

    s["affil"] = ParagraphStyle("ieee_affil",
        fontName="Times-Italic", fontSize=9, leading=12,
        alignment=TA_CENTER, textColor=colors.HexColor("#222222"), spaceAfter=10)

    # Section Headings (Numbered strictly matching instructor's 6 points)
    s["sec"] = ParagraphStyle("ieee_sec",
        fontName="Times-Bold", fontSize=10.5, leading=14,
        alignment=TA_LEFT, textColor=colors.black, spaceBefore=8, spaceAfter=3)

    # Subsections
    s["subsec"] = ParagraphStyle("ieee_subsec",
        fontName="Times-BoldItalic", fontSize=9.5, leading=13,
        alignment=TA_LEFT, textColor=colors.black, spaceBefore=5, spaceAfter=2)

    # Body text
    s["body"] = ParagraphStyle("ieee_body",
        fontName="Times-Roman", fontSize=8.5, leading=11.5,
        alignment=TA_JUSTIFY, textColor=colors.black, spaceAfter=4)

    # Bullet points
    s["bullet"] = ParagraphStyle("ieee_bullet",
        fontName="Times-Roman", fontSize=8.5, leading=11.5,
        alignment=TA_JUSTIFY, textColor=colors.black, leftIndent=12, firstLineIndent=-8, spaceAfter=2)

    # Captions
    s["fig_cap"] = ParagraphStyle("ieee_fig_cap",
        fontName="Times-Italic", fontSize=7.8, leading=10.5,
        alignment=TA_CENTER, textColor=colors.HexColor("#222222"), spaceBefore=2, spaceAfter=6)

    s["tbl_cap"] = ParagraphStyle("ieee_tbl_cap",
        fontName="Times-Bold", fontSize=8, leading=11,
        alignment=TA_CENTER, textColor=colors.black, spaceBefore=4, spaceAfter=3)

    # Table text
    s["th"] = ParagraphStyle("ieee_th",
        fontName="Times-Bold", fontSize=7.5, leading=9.5,
        alignment=TA_CENTER, textColor=colors.black)

    s["td"] = ParagraphStyle("ieee_td",
        fontName="Times-Roman", fontSize=7.5, leading=9.5,
        alignment=TA_CENTER, textColor=colors.black)

    s["td_left"] = ParagraphStyle("ieee_td_left",
        fontName="Times-Roman", fontSize=7.5, leading=9.5,
        alignment=TA_LEFT, textColor=colors.black)

    s["ref"] = ParagraphStyle("ieee_ref",
        fontName="Times-Roman", fontSize=7.8, leading=10.5,
        alignment=TA_JUSTIFY, textColor=colors.black, leftIndent=14, firstLineIndent=-14, spaceAfter=2)

    return s


def make_simple_table(headers, rows, widths, styles, alignments=None):
    """Simple clean IEEE-style table with classic horizontal rules and no heavy colors."""
    th_style = styles["th"]
    td_style = styles["td"]
    td_l_style = styles["td_left"]

    table_data = [[Paragraph(h, th_style) for h in headers]]
    for r in rows:
        row_cells = []
        for idx, val in enumerate(r):
            # First column or text column can be left-aligned
            is_left = (idx == 0 and alignments is None) or (alignments and alignments[idx] == "L")
            st = td_l_style if is_left else td_style
            row_cells.append(Paragraph(str(val), st))
        table_data.append(row_cells)

    ts = TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),    # Top rule
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),    # Header underline
        ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),  # Bottom rule
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    # Add subtle horizontal line between rows
    for i in range(1, len(rows)):
        ts.add('LINEBELOW', (0, i), (-1, i), 0.25, colors.HexColor("#D0D0D0"))

    return Table(table_data, colWidths=[w*cm for w in widths], style=ts)


def build_pdf():
    styles = get_styles()
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=1.8*cm,
        rightMargin=1.8*cm,
        topMargin=1.8*cm,
        bottomMargin=1.8*cm,
        title="Data Networks Mid-Lab Technical Report",
        author="Chhatrapal Bhuarya, Dasari Sai Kishan, Saarth Yawale, Sudhanshu Bhagat"
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, AUTHORS, 1. TITLE, 2. AIM, 3. OBJECTIVES, 4. METHODOLOGY (PART 1)
    # =========================================================================
    story.append(Paragraph("Lightweight Edge-Based Intrusion Detection for IoT Networks Using Deep Feature Extraction and Classical Machine Learning", styles["title"]))

    story.append(Paragraph(
        "<b>Chhatrapal Bhuarya</b> (24ECB0B14) &nbsp;|&nbsp; "
        "<b>Dasari Sai Kishan</b> (24ECB0B15) &nbsp;|&nbsp; "
        "<b>Saarth Yawale</b> (24ECB0B49) &nbsp;|&nbsp; "
        "<b>Sudhanshu Bhagat</b> (24ECB0B57)", styles["author"]))

    story.append(Paragraph(
        "Department of Electronics and Communication Engineering, National Institute of Technology Warangal<br/>"
        "Course: Data Networks (ECE) &nbsp;|&nbsp; GitHub Repository: <i>https://github.com/boringGuru347/DN-Project</i>", styles["affil"]))

    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceAfter=5))

    # 1. Title of the experiment/study/exercise
    story.append(Paragraph("1. Title of the Experiment / Study / Exercise", styles["sec"]))
    story.append(Paragraph(
        "<b>Lightweight Edge-Based Intrusion Detection for IoT Networks Using Deep Feature Extraction and Classical Machine Learning: A Comparative Study of CNN, SVM, and CNN+SVM Architectures on the UNSW-NB15 Benchmark.</b>", styles["body"]))

    # 2. Aim
    story.append(Paragraph("2. Aim", styles["sec"]))
    story.append(Paragraph(
        "To develop, benchmark, and critically evaluate a lightweight machine-learning pipeline for network intrusion detection in resource-constrained Internet of Things (IoT) environments. The study aims to replace heavy recurrent deep learning architectures (such as CNN-LSTM-Attention) with compact feature extraction and efficient classifiers, reducing feature dimensionality from 42 attributes to 20 while sustaining high detection accuracy (>87%), low false positive rates (<4%), and microsecond-level edge inference latency.", styles["body"]))

    # 3. Objectives
    story.append(Paragraph("3. Objectives", styles["sec"]))
    story.append(Paragraph("• <b>O1 — Data Preparation & Zero-Leakage Preprocessing:</b> Ingest the full UNSW-NB15 benchmark dataset (82,332 training flows and 175,341 testing flows); handle missing and infinite values; encode categorical features (protocol, service, state); and apply standard z-score normalization fit exclusively on the training partition.", styles["bullet"]))
    story.append(Paragraph("• <b>O2 — Statistical Feature Reduction:</b> Formulate an ANOVA F-score feature selection sweep across <i>k</i> ∈ {10, 15, 20, 25, 30, 35} to achieve over 50% feature compression while retaining maximal inter-class variance.", styles["bullet"]))
    story.append(Paragraph("• <b>O3 — Deep Feature Extractor Formulation:</b> Construct a lightweight neural network (MLP feature extractor with 3,457 parameters) that transforms raw scaled traffic into a compact 64-dimensional latent representation.", styles["bullet"]))
    story.append(Paragraph("• <b>O4 — Standalone & Hybrid Model Implementation:</b> Train and evaluate three distinct classifiers: (a) Standalone CNN/MLP, (b) Standalone Support Vector Machine with Radial Basis Function kernel (RBF-SVM), and (c) a Hybrid CNN+SVM pipeline utilizing extracted latent deep features.", styles["bullet"]))
    story.append(Paragraph("• <b>O5 — Empirical Performance & Edge Profiling:</b> Quantify classification accuracy, precision, recall, F1-score, false alarm rate (FPR), model size, training time, and per-flow inference latency across 175,341 unseen test flows.", styles["bullet"]))
    story.append(Paragraph("• <b>O6 — Methodological Literature Benchmarking:</b> Contrast the empirical footprint and classification trade-offs against complex deep architectures from published IEEE literature.", styles["bullet"]))

    # 4. Methodology (Intro + Dataset)
    story.append(Paragraph("4. Methodology", styles["sec"]))
    story.append(Paragraph("<b>4.1 Dataset Selection and Class Distribution</b>", styles["subsec"]))
    story.append(Paragraph(
        "The UNSW-NB15 dataset (created by the Australian Cyber Security Centre) was selected as the evaluation testbed due to its realistic synthesis of modern network normal transactions and nine contemporary attack vectors (DoS, Exploits, Fuzzers, Generic, Reconnaissance, Backdoor, Analysis, Shellcode, Worms). For binary intrusion detection, all malicious records are classified as class 1 (Attack) while benign traffic is designated as class 0 (Normal). The standard benchmark partitioning was maintained.", styles["body"]))

    story.append(Paragraph("TABLE I: UNSW-NB15 TRAIN AND TEST PARTITIONING", styles["tbl_cap"]))
    t1_data = [
        ["Training Set", "82,332", "37,000 (44.94%)", "45,332 (55.06%)", "42 (after dropping id, attack_cat)"],
        ["Testing Set", "175,341", "56,000 (31.94%)", "119,341 (68.06%)", "42 (transformed using train stats)"],
    ]
    story.append(make_simple_table(
        ["Dataset Split", "Total Flows", "Normal Flows (0)", "Attack Flows (1)", "Feature Dimension"],
        t1_data, [3.2, 2.5, 3.2, 3.2, 5.3], styles))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: 4. METHODOLOGY (CONTINUED)
    # =========================================================================
    story.append(Paragraph("4. Methodology (Continued)", styles["sec"]))

    story.append(Paragraph("<b>4.2 Preprocessing and Data Leakage Prevention Pipeline</b>", styles["subsec"]))
    story.append(Paragraph(
        "In operational network intrusion detection, model parameters must never observe future test traffic during training. To guarantee zero data leakage, our preprocessing pipeline executes strictly as follows: (1) Identifier columns (<i>id</i>) and multi-class categories (<i>attack_cat</i>) are eliminated; (2) Infinite values are mapped to NaN, and missing values are imputed using column-wise medians computed <i>strictly</i> from the 82,332 training flows; (3) Nominal categorical attributes (<i>proto</i>: 132 unique tokens, <i>service</i>: 14 tokens, <i>state</i>: 8 tokens) are encoded using LabelEncoders fitted solely on training values with out-of-vocabulary test items mapped to an unknown bin; (4) Standard scaling is executed using parameters fit exclusively on training data: <i>z = (x - μ_train) / σ_train</i>. Test data is normalized using the frozen <i>μ_train</i> and <i>σ_train</i> vectors.", styles["body"]))

    story.append(Paragraph("<b>4.3 ANOVA F-Score Feature Selection</b>", styles["subsec"]))
    story.append(Paragraph(
        "To minimize processing overhead and memory usage on edge IoT gateways, we deploy Analysis of Variance (ANOVA) F-score ranking (SelectKBest). The F-statistic tests whether the class-conditional means differ significantly relative to within-class dispersion:", styles["body"]))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>F<sub>j</sub> = [ Σ<sub>c</sub> n<sub>c</sub> (x̄<sub>j,c</sub> - x̄<sub>j</sub>)<sup>2</sup> / (C - 1) ] / [ Σ<sub>c</sub> Σ<sub>i</sub> (x<sub>i,j,c</sub> - x̄<sub>j,c</sub>)<sup>2</sup> / (N - C) ]</b>", styles["body"]))
    story.append(Paragraph(
        "where <i>C = 2</i> (binary classes), <i>N = 82,332</i>, and <i>n_c</i> is the sample count for class <i>c</i>. The top 20 features were chosen from the original 42 (a 52.4% dimensionality reduction). The selected subset includes: <i>sbytes, sttl, dttl, sload, dload, sinpkt, dinpkt, sjit, djit, swin, stcpb, dtcpb, tcprtt, synack, ackdat, smean, dmean, ct_state_ttl, ct_dst_sport_ltm, ct_srv_dst</i>. These capture critical packet sizes, inter-arrival dynamics, TCP handshake latencies, and active connection density.", styles["body"]))

    story.append(Paragraph("<b>4.4 Architectural Design of Evaluated Models</b>", styles["subsec"]))
    story.append(Paragraph(
        "• <b>Standalone CNN/MLP:</b> Configured with an input layer of 20 units, followed by Hidden Layer 1 (64 units, ReLU activation, batch size 512), Hidden Layer 2 (32 units, ReLU activation), and a logistic output unit. The network is trained with the Adam optimizer (learning rate = 10<sup>-3</sup>, weight decay α = 10<sup>-4</sup>) using early stopping with a patience of 5 iterations based on a 10% validation split. Total trainable parameters: <b>3,457</b> (occupying just 47.6 KB).<br/>"
        "• <b>Standalone Support Vector Machine (SVM):</b> Implemented with a non-linear Radial Basis Function (RBF) kernel: <i>K(x_i, x_j) = exp(-γ ||x_i - x_j||<sup>2</sup>)</i> with regularization penalty <i>C = 1.0</i> and kernel coefficient <i>γ = 1 / (20 × Var(X))</i>. A 1,000 MB kernel cache is allocated for high-throughput dual optimization.<br/>"
        "• <b>Hybrid CNN+SVM Pipeline:</b> The trained CNN feature extractor is frozen, and the 64-dimensional activations from Hidden Layer 1 (<i>h_1 = max(0, W_1<sup>T</sup> x + b_1)</i>) are extracted as learned non-linear descriptors. An RBF-SVM classifier is then trained on this 64-dimensional latent manifold, creating a maximum-margin decision boundary over learned deep features.", styles["body"]))

    story.append(Paragraph("TABLE II: ARCHITECTURAL CHARACTERISTICS OF EVALUATED MODELS", styles["tbl_cap"]))
    t2_data = [
        ["Standalone CNN", "20 (Scaled)", "Dense(64, ReLU) → Dense(32, ReLU)", "Dense(1, Sigmoid)", "3,457 weights & biases", "Adam (lr=1e-3, L2=1e-4)"],
        ["Standalone SVM", "20 (Scaled)", "Implicit RBF Kernel Space", "Hyperplane Sign", "13,665 Support Vectors", "Dual Quadratic Programming"],
        ["CNN+SVM Hybrid", "20 (Scaled)", "CNN Hidden 1 (64-D Latent Embeddings)", "RBF-SVM Hyperplane", "3,457 CNN + 13,665 SVs", "Two-Stage Feature & Margin Learning"],
    ]
    story.append(make_simple_table(
        ["Model Architecture", "Input Dimension", "Feature Mapping / Hidden Layers", "Decision Function", "Model Parameters", "Optimization Method"],
        t2_data, [2.8, 2.0, 4.4, 2.8, 2.8, 2.6], styles))

    story.append(Paragraph("<b>4.5 Quantitative Performance Metrics</b>", styles["subsec"]))
    story.append(Paragraph(
        "Performance is evaluated using five primary statistical metrics along with execution profiling: "
        "<b>Accuracy</b> = (TP+TN)/(TP+TN+FP+FN); "
        "<b>Precision</b> = TP/(TP+FP); "
        "<b>Recall (Detection Rate)</b> = TP/(TP+FN); "
        "<b>F1-Score</b> = 2 × (Precision × Recall)/(Precision + Recall); "
        "<b>False Positive Rate (FPR)</b> = FP/(TN+FP). "
        "Training wall-clock duration and end-to-end inference latency across 175,341 flows are benchmarked in identical runtime conditions.", styles["body"]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: 5. SIMULATION RESULTS & SCENARIO DIAGRAMS (PIPELINE & FLOWCHART)
    # =========================================================================
    story.append(Paragraph("5. Simulation Results / Observations Along with Scenario Diagram", styles["sec"]))
    story.append(Paragraph(
        "This section presents the empirical findings obtained from the complete experimental execution on the UNSW-NB15 test suite. All experiments were conducted using Python 3.10 with deterministic seeds (seed=42). The full end-to-end pipeline required 9.3 minutes of execution time.", styles["body"]))

    story.append(Paragraph("<b>5.1 System Architecture and Scenario Flow Diagrams</b>", styles["subsec"]))
    story.append(Paragraph(
        "Fig. 1 depicts the complete scenario diagram of the edge-based intrusion detection pipeline, showing the transition of network packet captures from raw flow aggregation, data preprocessing, ANOVA feature filtering, model inference, and alert notification. Fig. 2 illustrates the detailed architectural flowchart of the proposed CNN+SVM hybrid model.", styles["body"]))

    # Add Scenario Diagram and Architecture Flowchart side-by-side
    p1 = os.path.join(DIAGRAMS_DIR, "overall_pipeline.png")
    p2 = os.path.join(DIAGRAMS_DIR, "cnn_svm_flow.png")

    img_w = 7.8 * cm
    img_h = 10.5 * cm
    diag_cells = []
    if os.path.exists(p1) and os.path.exists(p2):
        row_images = [Image(p1, width=img_w, height=img_h), Image(p2, width=img_w, height=img_h)]
        row_caps = [
            Paragraph("<b>Fig. 1:</b> Scenario diagram of end-to-end IoT IDS pipeline.", styles["fig_cap"]),
            Paragraph("<b>Fig. 2:</b> Deep feature extraction & SVM classification flowchart.", styles["fig_cap"])
        ]
        diag_tbl = Table([row_images, row_caps], colWidths=[8.5*cm, 8.5*cm],
                         style=TableStyle([
                             ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                             ('VALIGN', (0,0), (-1,-1), 'TOP'),
                             ('TOPPADDING', (0,0), (-1,-1), 1),
                             ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                         ]))
        story.append(diag_tbl)

    story.append(Paragraph(
        "<b>Scenario Execution Walkthrough:</b> Incoming network traffic at an IoT gateway is parsed into bidirectional flow records. The lightweight preprocessing module cleans attributes and applies scaling parameters computed during training. The ANOVA module extracts the 20 pre-selected features. In the standalone CNN configuration, flows are scored in batches of 512 in under 0.06 seconds. In the hybrid mode, intermediate representations are passed to the SVM kernel decision block to verify suspicious anomalous behaviors.", styles["body"]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: 5. SIMULATION RESULTS (FEATURE SWEEP, CONVERGENCE, AND GRAPHS)
    # =========================================================================
    story.append(Paragraph("5. Simulation Results / Observations (Continued)", styles["sec"]))

    story.append(Paragraph("<b>5.2 Feature Reduction Sweep Analysis</b>", styles["subsec"]))
    story.append(Paragraph(
        "To justify the selection of <i>k = 20</i> features, an automated sensitivity sweep was evaluated across <i>k</i> ∈ {10, 15, 20, 25, 30, 35}. Table III and Fig. 3 illustrate the performance trajectory across varying feature dimensions.", styles["body"]))

    # Table III & Table IV
    t3_data = [
        ["k = 10", "82.91%", "86.88%", "76.19% Reduction", "Underfitting; lacks essential TCP handshake timing metrics"],
        ["k = 15", "82.04%", "86.02%", "64.29% Reduction", "Suboptimal separation in connection-state attributes"],
        ["k = 20 (Selected)", "85.55%", "88.67%", "52.38% Reduction", "Optimal elbow point; high precision with low memory usage"],
        ["k = 25", "88.30%", "90.95%", "40.48% Reduction", "Diminishing returns begin; marginal gain (+2.75% acc)"],
        ["k = 30", "88.45%", "91.06%", "28.57% Reduction", "Peak accuracy with linear classifier, but +50% memory cost"],
        ["k = 35", "88.29%", "90.92%", "16.67% Reduction", "Slight performance degradation due to noise in weak features"],
    ]
    story.append(Paragraph("TABLE III: ANOVA F-SCORE FEATURE SWEEP ON UNSW-NB15 TEST SET", styles["tbl_cap"]))
    story.append(make_simple_table(
        ["Feature Count", "Accuracy", "F1-Score", "Dimensionality Reduction", "Analytical Observation"],
        t3_data, [2.5, 2.0, 2.0, 3.8, 7.1], styles))

    story.append(Paragraph("<b>5.3 CNN Convergence and Loss Profile</b>", styles["subsec"]))
    story.append(Paragraph(
        "The deep feature extractor was trained over 53 epochs before triggering early stopping. The training cross-entropy loss converged smoothly from 0.4090 to 0.1144, with the validation score reaching a peak of <b>95.14%</b> at iteration 47. Wall-clock training required only <b>11.01 seconds</b>.", styles["body"]))

    # Embed Feature Reduction graph and CNN Loss Curve side by side
    g4 = os.path.join(GRAPHS_DIR, "feature_reduction.png")
    g5 = os.path.join(GRAPHS_DIR, "cnn_training_history.png")
    if os.path.exists(g4) and os.path.exists(g5):
        row_g = [Image(g4, width=8.2*cm, height=5.2*cm), Image(g5, width=8.2*cm, height=5.2*cm)]
        row_g_caps = [
            Paragraph("<b>Fig. 3:</b> Accuracy and F1-Score vs. Number of Features (k).", styles["fig_cap"]),
            Paragraph("<b>Fig. 4:</b> CNN training loss curve across 53 iterations.", styles["fig_cap"])
        ]
        g_tbl = Table([row_g, row_g_caps], colWidths=[8.7*cm, 8.7*cm],
                      style=TableStyle([
                          ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                          ('VALIGN', (0,0), (-1,-1), 'TOP'),
                          ('TOPPADDING', (0,0), (-1,-1), 1),
                          ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                      ]))
        story.append(g_tbl)

    t4_data = [
        ["Iteration 1", "0.4090", "0.8580", "Initial forward pass, rapid gradient adjustment"],
        ["Iteration 10", "0.1487", "0.9362", "Major convergence phase; learns dominant attack patterns"],
        ["Iteration 30", "0.1247", "0.9440", "Steady refinement of non-linear decision surface"],
        ["Iteration 47 (Best)", "0.1162", "0.9514", "Optimal validation checkpoint; model weights preserved"],
        ["Iteration 53 (Stop)", "0.1144", "0.9501", "Early stopping triggered (n_iter_no_change = 5)"],
    ]
    story.append(Paragraph("TABLE IV: TRAINING CONVERGENCE HISTORY OF THE CNN FEATURE EXTRACTOR", styles["tbl_cap"]))
    story.append(make_simple_table(
        ["Iteration", "Training Loss", "Validation Score", "Optimization Status"],
        t4_data, [3.0, 2.5, 3.0, 8.9], styles))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: 5. SIMULATION RESULTS (MODEL COMPARISON, CONFUSION MATRICES, EFFICIENCY)
    # =========================================================================
    story.append(Paragraph("5. Simulation Results / Observations (Continued)", styles["sec"]))

    story.append(Paragraph("<b>5.4 Comprehensive Performance Comparison on Unseen Test Set</b>", styles["subsec"]))
    story.append(Paragraph(
        "Table V reports the complete set of measured classification metrics across the three models on the 175,341 testing flows. All metrics are computed strictly on the held-out test split.", styles["body"]))

    t5_data = [
        ["Accuracy (%)", "87.60%", "88.21%", "88.16%", "SVM achieves highest accuracy; CNN within 0.61%"],
        ["Precision (%)", "98.40%", "97.51%", "97.99%", "CNN achieves lowest false alarms on benign flows"],
        ["Recall / DR (%)", "83.14%", "84.84%", "84.34%", "SVM detects 2,035 more attack flows than CNN"],
        ["F1-Score (%)", "90.13%", "90.73%", "90.65%", "All three models exceed 90% harmonic balance"],
        ["False Positive Rate", "2.88%", "4.62%", "3.69%", "CNN FPR is 37.6% lower than SVM (1,615 vs 2,590 FP)"],
        ["Training Duration (s)", "11.01 s", "66.55 s", "61.36 s", "CNN trains 6.0× faster than standalone SVM"],
        ["Inference Time (175k flows)", "0.0596 s", "163.14 s", "151.73 s", "CNN achieves 2,737× faster inference speed"],
        ["Per-Flow Latency", "0.34 μs", "930 μs", "867 μs", "CNN supports wire-speed real-time IoT processing"],
        ["Model Footprint (KB)", "47.6 KB", "3,077 KB", "7,149 KB", "CNN model is 64× smaller than SVM on disk"],
    ]
    story.append(Paragraph("TABLE V: BENCHMARK PERFORMANCE COMPARISON ON 175,341 UNSW-NB15 TEST FLOWS", styles["tbl_cap"]))
    story.append(make_simple_table(
        ["Evaluation Metric", "Standalone CNN", "Standalone SVM", "Hybrid CNN+SVM", "Comparative Analysis"],
        t5_data, [3.5, 2.5, 2.5, 2.5, 6.4], styles))

    story.append(Paragraph("<b>5.5 Confusion Matrix Breakdown</b>", styles["subsec"]))
    t6_data = [
        ["Standalone CNN", "54,385", "1,615", "20,123", "99,218", "2.88%", "83.14%", "Very low false alarms (1,615 FP)"],
        ["Standalone SVM", "53,410", "2,590", "18,088", "101,253", "4.62%", "84.84%", "Higher attack capture (+2,035 TP)"],
        ["Hybrid CNN+SVM", "53,936", "2,064", "18,690", "100,651", "3.69%", "84.34%", "Effective middle ground in FPR & Recall"],
    ]
    story.append(Paragraph("TABLE VI: CONFUSION MATRIX QUANTIFICATION (TOTAL TEST FLOWS = 175,341)", styles["tbl_cap"]))
    story.append(make_simple_table(
        ["Model", "True Neg (TN)", "False Pos (FP)", "False Neg (FN)", "True Pos (TP)", "FPR (%)", "Recall (%)", "Operational Impact"],
        t6_data, [2.5, 2.0, 1.8, 2.0, 2.0, 1.5, 1.7, 3.9], styles))

    # Add Graphs (Performance Comparison, Efficiency, Confusion Matrix)
    g1 = os.path.join(GRAPHS_DIR, "model_performance_comparison.png")
    g3 = os.path.join(GRAPHS_DIR, "efficiency_comparison.png")
    if os.path.exists(g1) and os.path.exists(g3):
        row_eval = [Image(g1, width=8.2*cm, height=4.8*cm), Image(g3, width=8.2*cm, height=4.8*cm)]
        row_eval_caps = [
            Paragraph("<b>Fig. 5:</b> Classification metrics across evaluated models.", styles["fig_cap"]),
            Paragraph("<b>Fig. 6:</b> Training and inference runtime comparison.", styles["fig_cap"])
        ]
        tbl_eval = Table([row_eval, row_eval_caps], colWidths=[8.7*cm, 8.7*cm],
                         style=TableStyle([
                             ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                             ('VALIGN', (0,0), (-1,-1), 'TOP'),
                             ('TOPPADDING', (0,0), (-1,-1), 1),
                             ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                         ]))
        story.append(tbl_eval)

    g2 = os.path.join(GRAPHS_DIR, "confusion_matrices.png")
    if os.path.exists(g2):
        story.append(Image(g2, width=15.5*cm, height=3.6*cm))
        story.append(Paragraph("<b>Fig. 7:</b> Comparative normalized confusion matrices for CNN, SVM, and CNN+SVM models.", styles["fig_cap"]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 6. DISCUSSION ON THE RESULTS/OBSERVATION & REFERENCES
    # =========================================================================
    story.append(Paragraph("6. Discussion on the Results / Observation", styles["sec"]))

    story.append(Paragraph("<b>6.1 Classification Accuracy vs. Resource Footprint</b>", styles["subsec"]))
    story.append(Paragraph(
        "All three architectures achieve remarkably consistent classification performance, spanning an accuracy interval of <b>87.60% to 88.21%</b> and F1-scores between <b>90.13% and 90.73%</b>. The standalone SVM achieves the highest raw accuracy (88.21%) and recall (84.84%), demonstrating the effectiveness of the RBF kernel in projecting tabular flow features into high-dimensional space. However, this marginal 0.61% accuracy gain over the CNN comes at an exorbitant computational price: SVM inference is <b>2,737× slower</b> than the CNN (163.14 seconds vs. 0.0596 seconds for 175k flows). This confirms that a lightweight feedforward neural model provides vastly superior edge practicality.", styles["body"]))

    story.append(Paragraph("<b>6.2 False Positive Rate and Alert Fatigue in IoT Gateways</b>", styles["subsec"]))
    story.append(Paragraph(
        "In industrial and municipal IoT networks, false alarms are often more damaging than minor drop-offs in detection rate, as false alerts trigger bandwidth throttling, automated port isolations, and personnel fatigue. The standalone CNN achieves the lowest FPR (<b>2.88%</b>) and the highest precision (<b>98.40%</b>), misclassifying only 1,615 normal packets out of 56,000. In contrast, the standalone SVM produces 2,590 false alarms (FPR = 4.62%) — a <b>60.4% increase</b> in false positives. The hybrid CNN+SVM balances this trade-off with an FPR of 3.69% and recall of 84.34%, proving that learned deep representations provide cleaner geometric clustering than raw scaled inputs.", styles["body"]))

    story.append(Paragraph("<b>6.3 Edge Deployment Feasibility and Memory Profiling</b>", styles["subsec"]))
    story.append(Paragraph(
        "With a model size of just <b>47.6 KB</b> and 3,457 parameters, the CNN can comfortably reside within the SRAM of embedded microcontrollers (e.g., STM32, ESP32, ARM Cortex-M4/M7) without requiring off-chip DRAM. Its per-sample inference latency of <b>0.34 microseconds</b> permits real-time wire-speed line monitoring up to hundreds of thousands of flows per second. Conversely, the SVM stores 13,665 support vectors (3,077 KB), requiring <i>O(N_sv × d)</i> floating-point operations per flow, rendering it unsuitable for high-speed edge gating.", styles["body"]))

    story.append(Paragraph("<b>6.4 Methodological Comparison with Reference Literature</b>", styles["subsec"]))
    story.append(Paragraph(
        "• <b>Phalaagae et al. (IEEE Access, 2025):</b> Proposed a complex CNN-LSTM model with Attention mechanisms. While recurrent temporal units capture multi-step flow transitions, they introduce <i>O(T × H<sup>2</sup>)</i> sequential operations and quadratic attention memory complexity that overwhelm low-power IoT gateways. Our study establishes an empirical baseline showing that non-recurrent deep feature extraction delivers >87.6% accuracy while eliminating recurrent loop latency entirely.<br/>"
        "• <b>Edge-AI Hybrid Framework (IEEE ICERECT, 2025):</b> Emphasized botnet mitigation directly at the edge. Our empirical findings substantiate their core hypothesis, demonstrating that feature reduction from 42 to 20 variables coupled with lightweight deep inference reduces processing latency to the sub-microsecond regime while preserving effective perimeter defense.", styles["body"]))

    story.append(Paragraph("<b>6.5 Acknowledged Limitations and Next Steps</b>", styles["subsec"]))
    story.append(Paragraph(
        "<b>Limitations:</b> (1) The dataset was evaluated as a binary classification task; individual attack categories (e.g., Worms, Shellcode) have not yet been evaluated separately; (2) Hyperparameters were selected via sensible baselines rather than exhaustive Bayesian optimization; (3) Benchmarks were executed on an x86 workstation rather than physical ARM/RISC-V edge hardware.<br/>"
        "<b>Next Steps:</b> (1) Extend the pipeline to 10-class multi-attack classification; (2) Implement 8-bit post-training integer quantization (INT8) to reduce model size below 15 KB; (3) Deploy and profile the quantized model on an embedded Raspberry Pi 4 / ESP32 edge device with hardware timers.", styles["body"]))

    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.black, spaceAfter=4))

    # References
    story.append(Paragraph("References", styles["sec"]))
    refs = [
        "[1] N. Moustafa and J. Slay, \"UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set),\" in <i>Proc. IEEE Military Communications and Information Systems Conference (MilCIS)</i>, Canberra, Australia, 2015, pp. 1–6.",
        "[2] P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni, and S. Rajalakshmi, \"A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks,\" <i>IEEE Access</i>, vol. 13, pp. 15420–15435, 2025.",
        "[3] \"Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems,\" in <i>Proc. IEEE International Conference on Emerging Research in Electronics, Computer Science and Technology (ICERECT)</i>, 2025.",
        "[4] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825–2830, 2011.",
        "[5] V. N. Vapnik, <i>The Nature of Statistical Learning Theory</i>, Springer-Verlag New York, 1995.",
    ]
    for r in refs:
        story.append(Paragraph(r, styles["ref"]))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report built successfully at: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
