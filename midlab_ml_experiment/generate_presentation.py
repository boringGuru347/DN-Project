"""
generate_presentation.py — Generates a 5-slide PowerPoint presentation (.pptx)
for the Data Networks Mid-Lab Review at NIT Warangal.
Evaluation Scheme: 40 Marks (Title + 4 slides @ 10 marks each).
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette (NIT Warangal Academic & Modern Tech Theme)
# -----------------------------------------------------------------------------
DARK_NAVY    = RGBColor(15, 23, 42)     # #0F172A - Dominant dark
PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1E3A8A - Header primary
ACCENT_BLUE  = RGBColor(37, 99, 235)    # #2563EB - Highlights & badges
CYAN_ACCENT  = RGBColor(14, 165, 233)   # #0EA5E9 - Subtle tech accent
LIGHT_BG     = RGBColor(248, 250, 252)  # #F8FAFC - Slide background
CARD_BG      = RGBColor(255, 255, 255)  # #FFFFFF - Container cards
CARD_BORDER  = RGBColor(226, 232, 240)  # #E2E8F0 - Subtle border
TEXT_MAIN    = RGBColor(30, 41, 59)     # #1E293B - Primary dark text
TEXT_MUTED   = RGBColor(100, 116, 139)  # #64748B - Secondary subtitle text
SUCCESS_GREEN= RGBColor(22, 101, 52)    # #166534 - Metric positive
HEADER_TEXT  = RGBColor(255, 255, 255)  # White text

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

def set_slide_background(slide, prs, color):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background() # No border
    return bg_shape

def add_header(slide, title_text, section_tag=""):
    """Adds a consistent, professional banner across slides 2-5."""
    # Top banner card
    header_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1)
    )
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = PRIMARY_BLUE
    header_box.line.fill.background()

    # Accent stripe
    stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333), Inches(0.06)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = CYAN_ACCENT
    stripe.line.fill.background()

    # Text container
    tx_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.12), Inches(12.133), Inches(0.85))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = HEADER_TEXT

    if section_tag:
        p2 = tf.add_paragraph()
        p2.text = section_tag
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(191, 219, 254)

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Draws a clean modern container card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)
    return card

def create_presentation(output_path, project_root):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    diagrams_dir = os.path.join(project_root, "diagrams")
    graphs_dir = os.path.join(project_root, "graphs")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, prs, DARK_NAVY)

    # Decorative header glow
    glow = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CYAN_ACCENT
    glow.line.fill.background()

    # Category Pill Badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.65), Inches(5.8), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(30, 41, 59)
    badge.line.color.rgb = ACCENT_BLUE
    badge.line.width = Pt(1)
    b_tf = badge.text_frame
    b_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bp = b_tf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = "DATA NETWORKS COURSE PROJECT  |  MID-LAB REVIEW"
    bp.font.name = FONT_BODY
    bp.font.size = Pt(10)
    bp.font.bold = True
    bp.font.color.rgb = CYAN_ACCENT

    # Main Project Title
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(2.0))
    t_tf = title_box.text_frame
    t_tf.word_wrap = True
    tp = t_tf.paragraphs[0]
    tp.text = "Lightweight Edge-Based Intrusion Detection for IoT Networks"
    tp.font.name = FONT_TITLE
    tp.font.size = Pt(30)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(255, 255, 255)

    tp_sub = t_tf.add_paragraph()
    tp_sub.text = "Using Deep Feature Extraction and Classical Machine Learning"
    tp_sub.font.name = FONT_TITLE
    tp_sub.font.size = Pt(24)
    tp_sub.font.bold = True
    tp_sub.font.color.rgb = CYAN_ACCENT

    # Subtitle / Department Info
    info_box = slide1.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.7), Inches(0.6))
    i_tf = info_box.text_frame
    ip = i_tf.paragraphs[0]
    ip.text = "Department of Electronics and Communication Engineering  •  National Institute of Technology Warangal"
    ip.font.name = FONT_BODY
    ip.font.size = Pt(13)
    ip.font.color.rgb = RGBColor(148, 163, 184)

    # 4 Student Cards Grid
    students = [
        ("Chhatrapal Bhuarya", "24ECB0B14", "Network / Data Preprocessing"),
        ("Dasari Sai Kishan", "24ECB0B15", "Reference Paper Reproduction"),
        ("Saarth Yawale", "24ECB0B49", "Proposed Model & Architecture"),
        ("Sudhanshu Bhagat", "24ECB0B57", "Benchmarking & Evaluation"),
    ]

    card_w = Inches(2.78)
    card_h = Inches(2.5)
    start_x = Inches(0.8)
    card_y = Inches(4.0)
    gap = Inches(0.2)

    for idx, (name, roll, role) in enumerate(students):
        cx = start_x + idx * (card_w + gap)
        scard = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        scard.fill.solid()
        scard.fill.fore_color.rgb = RGBColor(30, 41, 59)
        scard.line.color.rgb = RGBColor(51, 65, 85)
        scard.line.width = Pt(1.2)

        # Avatar circle / number tag
        tag = slide1.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.2), card_y + Inches(0.25), Inches(0.55), Inches(0.55))
        tag.fill.solid()
        tag.fill.fore_color.rgb = ACCENT_BLUE
        tag.line.fill.background()
        tag_tf = tag.text_frame
        tag_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tag_p = tag_tf.paragraphs[0]
        tag_p.alignment = PP_ALIGN.CENTER
        tag_p.text = f"S{idx+1}"
        tag_p.font.name = FONT_BODY
        tag_p.font.size = Pt(12)
        tag_p.font.bold = True
        tag_p.font.color.rgb = RGBColor(255, 255, 255)

        st_box = slide1.shapes.add_textbox(cx + Inches(0.2), card_y + Inches(0.9), card_w - Inches(0.4), Inches(1.4))
        st_tf = st_box.text_frame
        st_tf.word_wrap = True

        p_name = st_tf.paragraphs[0]
        p_name.text = name
        p_name.font.name = FONT_TITLE
        p_name.font.size = Pt(14)
        p_name.font.bold = True
        p_name.font.color.rgb = RGBColor(241, 245, 249)

        p_roll = st_tf.add_paragraph()
        p_roll.text = roll
        p_roll.font.name = FONT_BODY
        p_roll.font.size = Pt(12)
        p_roll.font.bold = True
        p_roll.font.color.rgb = CYAN_ACCENT

        p_role = st_tf.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_BODY
        p_role.font.size = Pt(10.5)
        p_role.font.color.rgb = RGBColor(148, 163, 184)

    # Footer Evaluation Note
    footer = slide1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    f_tf = footer.text_frame
    fp = f_tf.paragraphs[0]
    fp.text = "Mid-Lab Presentation: 8–10 Minutes  |  Total Evaluation: 40 Marks (10 Marks / Section)"
    fp.font.name = FONT_BODY
    fp.font.size = Pt(10)
    fp.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # SLIDE 2: MAIN REFERENCE PAPERS & TARGETED RESULTS (10 MARKS)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, prs, LIGHT_BG)
    add_header(slide2, "1. Main Reference Papers & Targeted Results", "Evaluation Section 1 — [10 Marks]")

    # Left Container: Main Reference Papers (Width: 6.8")
    add_card(slide2, Inches(0.6), Inches(1.35), Inches(6.4), Inches(5.8))

    ref_header = slide2.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(6.0), Inches(0.4))
    rf_tf = ref_header.text_frame
    rf_p = rf_tf.paragraphs[0]
    rf_p.text = "Identified Main IEEE Reference Papers"
    rf_p.font.name = FONT_TITLE
    rf_p.font.size = Pt(15)
    rf_p.font.bold = True
    rf_p.font.color.rgb = PRIMARY_BLUE

    # Paper 1 Box
    p1_card = add_card(slide2, Inches(0.8), Inches(1.95), Inches(6.0), Inches(2.35),
                       bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))
    p1_tf = slide2.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.8), Inches(2.25)).text_frame
    p1_tf.word_wrap = True

    p = p1_tf.paragraphs[0]
    p.text = "Reference Paper 1 (IEEE Access, 2025):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = p1_tf.add_paragraph()
    p.text = "P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni and S. Rajalakshmi, \"A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks.\""
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MAIN

    p = p1_tf.add_paragraph()
    p.text = "• Core Contribution: Employs CNN for spatial feature learning, LSTM for temporal correlation, and an Attention module to prioritize attack vectors."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    p = p1_tf.add_paragraph()
    p.text = "• Inherent Drawback: Extreme architectural complexity, high memory footprint, and recurrent sequential latency unsuitable for low-power edge IoT microcontrollers."
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(185, 28, 28)

    # Paper 2 Box
    p2_card = add_card(slide2, Inches(0.8), Inches(4.45), Inches(6.0), Inches(2.45),
                       bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))
    p2_tf = slide2.shapes.add_textbox(Inches(0.9), Inches(4.5), Inches(5.8), Inches(2.35)).text_frame
    p2_tf.word_wrap = True

    p = p2_tf.paragraphs[0]
    p.text = "Reference Paper 2 (IEEE ICERECT, 2025):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = p2_tf.add_paragraph()
    p.text = "\"Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems.\""
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MAIN

    p = p2_tf.add_paragraph()
    p.text = "• Core Contribution: Proposes edge-based deep learning pipelines to detect malicious botnet propagation and DDoS surges locally."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    p = p2_tf.add_paragraph()
    p.text = "• Inherent Drawback: Relies on deep end-to-end multi-layer neural classifiers requiring full GPU inference acceleration, limiting decentralization."
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(185, 28, 28)

    # Right Container: Targeted Results & Project Objectives (Width: 5.4")
    add_card(slide2, Inches(7.3), Inches(1.35), Inches(5.4), Inches(5.8))

    tgt_header = slide2.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5.0), Inches(0.4))
    tg_tf = tgt_header.text_frame
    tg_p = tg_tf.paragraphs[0]
    tg_p.text = "Targeted Results & Proposed Direction"
    tg_p.font.name = FONT_TITLE
    tg_p.font.size = Pt(15)
    tg_p.font.bold = True
    tg_p.font.color.rgb = PRIMARY_BLUE

    tg_body = slide2.shapes.add_textbox(Inches(7.5), Inches(1.95), Inches(5.0), Inches(4.9))
    tb_tf = tg_body.text_frame
    tb_tf.word_wrap = True

    objectives = [
        ("Feature Dimension Reduction",
         "Reduce raw traffic features by >50% (from 42 down to 20 flow attributes) via statistical ANOVA F-Score selection, slashing memory buffer and transmission overhead."),
        ("Lightweight Hybrid Pipeline",
         "Decouple representation learning from decision boundary: Use a compact CNN (or MLP) solely for feature transformation, paired with SVM for maximum-margin classification."),
        ("Preserve High Detection Performance",
         "Retain high attack detection accuracy (>88%) and strong precision (>97%), with false alarm rate (FPR) constrained below 4% on standard benchmark network traffic."),
        ("Drastic Computational Savings",
         "Eliminate recurrent LSTM loops and multi-head attention overhead, minimizing parameter count (<3,500 parameters) and enabling microsecond inference on constrained edge gateways."),
        ("Preliminary Milestone Objective",
         "Demonstrate concrete empirical feasibility of CNN vs. SVM vs. CNN+SVM on UNSW-NB15 dataset as the verified foundation for subsequent hardware-in-the-loop edge refinement.")
    ]

    for title, desc in objectives:
        p_t = tb_tf.add_paragraph() if tb_tf.paragraphs[0].text else tb_tf.paragraphs[0]
        p_t.text = f"✔ {title}"
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_BLUE

        p_d = tb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 3: GAPS BEING ADDRESSED & TASK DISTRIBUTION (10 MARKS)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, prs, LIGHT_BG)
    add_header(slide3, "2. Research Gaps & Group Member Task Distribution", "Evaluation Section 2 — [10 Marks]")

    # Left Container: 5 Gaps (Width: 5.7")
    add_card(slide3, Inches(0.6), Inches(1.35), Inches(5.7), Inches(5.8))

    gap_header = slide3.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.3), Inches(0.4))
    g_tf = gap_header.text_frame
    gp = g_tf.paragraphs[0]
    gp.text = "Identified Research Gaps in Literature"
    gp.font.name = FONT_TITLE
    gp.font.size = Pt(15)
    gp.font.bold = True
    gp.font.color.rgb = PRIMARY_BLUE

    gaps = [
        ("Gap 1: High Computational Complexity",
         "Existing models (CNN-LSTM, Transformers) demand immense FLOPs and memory, rendering them impractical for resource-constrained IoT/edge nodes."),
        ("Gap 2: Excessive Feature Dimensionality",
         "Standard datasets supply 40–80 features. Many are redundant or noisy, elevating memory storage, energy burn, and processing latency on gateways."),
        ("Gap 3: Accuracy vs. Inference Latency Trade-off",
         "Literature heavily optimizes for 99%+ accuracy at the cost of deep sequential models, disregarding real-time per-packet deadline constraints at the edge."),
        ("Gap 4: Underutilized Lightweight Hybrid Classifiers",
         "Scope exists to deploy deep learning strictly as a lightweight feature transformer, delegating classification to classical convex optimizers (SVM)."),
        ("Gap 5: Practical Edge Deployment Readiness",
         "Most IDS frameworks remain server-bound. Lowering memory footprint (<100 KB) and execution time is essential for proximity to IoT sensors.")
    ]

    gap_body = slide3.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.3), Inches(4.9))
    gb_tf = gap_body.text_frame
    gb_tf.word_wrap = True

    for title, desc in gaps:
        p_t = gb_tf.add_paragraph() if gb_tf.paragraphs[0].text else gb_tf.paragraphs[0]
        p_t.text = f"⚠ {title}"
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = RGBColor(194, 65, 12)

        p_d = gb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.2)
        p_d.font.color.rgb = TEXT_MAIN

    # Right Container: 4 Group Members Task Distribution (Width: 6.3")
    add_card(slide3, Inches(6.5), Inches(1.35), Inches(6.2), Inches(5.8))

    task_header = slide3.shapes.add_textbox(Inches(6.7), Inches(1.5), Inches(5.8), Inches(0.4))
    t_tf = task_header.text_frame
    tp = t_tf.paragraphs[0]
    tp.text = "Task Distribution Among Group Members"
    tp.font.name = FONT_TITLE
    tp.font.size = Pt(15)
    tp.font.bold = True
    tp.font.color.rgb = PRIMARY_BLUE

    members = [
        ("Student 1: Chhatrapal Bhuarya (24ECB0B14)", "Network & Data Preprocessing Pipeline",
         "• Researched IoT traffic characteristics and cyber-attack taxonomy.\n• Managed UNSW-NB15 benchmark dataset ingestion (82K train / 175K test flows).\n• Engineered data cleaning: median imputation, categorical encoding (proto, state, service), and zero-leakage standard feature scaling."),
        ("Student 2: Dasari Sai Kishan (24ECB0B15)", "Reference Paper Reproduction & Baseline",
         "• Analyzed architectures from Phalaagae et al. (IEEE Access 2025) and ICERECT 2025.\n• Evaluated baseline CNN-LSTM and attention complexities against edge requirements.\n• Defined baseline experimental protocols and metric benchmarking standards."),
        ("Student 3: Saarth Yawale (24ECB0B49)", "Proposed Lightweight Architecture & Models",
         "• Implemented statistical ANOVA F-Score feature selection (SelectKBest, k=20).\n• Built and tuned the standalone Lightweight Deep Feature Extractor (CNN/MLP).\n• Formulated and implemented the CNN+SVM hybrid classification pipeline (64-D learned feature extraction coupled to RBF-kernel SVM decision boundary)."),
        ("Student 4: Sudhanshu Bhagat (24ECB0B57)", "Evaluation, Latency Profiling & Benchmarking",
         "• Scripted the evaluation suite measuring Accuracy, Precision, Recall, F1, and FPR.\n• Measured training runtime and per-sample inference latency across all 3 models.\n• Generated confusion matrix visualisations, feature-sweep curves, and benchmarked empirical metrics against reference paper findings.")
    ]

    task_body = slide3.shapes.add_textbox(Inches(6.7), Inches(1.95), Inches(5.8), Inches(4.9))
    tb_tf = task_body.text_frame
    tb_tf.word_wrap = True

    for name, role, details in members:
        p_n = tb_tf.add_paragraph() if tb_tf.paragraphs[0].text else tb_tf.paragraphs[0]
        p_n.text = name
        p_n.font.name = FONT_TITLE
        p_n.font.size = Pt(10.5)
        p_n.font.bold = True
        p_n.font.color.rgb = ACCENT_BLUE

        p_r = tb_tf.add_paragraph()
        p_r.text = f"Role: {role}"
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(9.5)
        p_r.font.bold = True
        p_r.font.color.rgb = DARK_NAVY

        p_det = tb_tf.add_paragraph()
        p_det.text = details
        p_det.font.name = FONT_BODY
        p_det.font.size = Pt(8.8)
        p_det.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: PROGRESS MADE (10 MARKS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, prs, LIGHT_BG)
    add_header(slide4, "3. Progress Made — Implementation & Technical Architecture", "Evaluation Section 3 — [10 Marks]")

    # Left Container: Technical Progress Highlights (Width: 6.0")
    add_card(slide4, Inches(0.6), Inches(1.35), Inches(6.0), Inches(5.8))

    prog_header = slide4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(0.4))
    pr_tf = prog_header.text_frame
    pr_p = pr_tf.paragraphs[0]
    pr_p.text = "Completed Engineering & Experimental Milestones"
    pr_p.font.name = FONT_TITLE
    pr_p.font.size = Pt(14)
    pr_p.font.bold = True
    pr_p.font.color.rgb = PRIMARY_BLUE

    milestones = [
        ("✓ Rigorous Dataset Preprocessing Pipeline",
         "Loaded UNSW-NB15 benchmark (82,332 train / 175,341 test rows). Addressed class distributions (45K attack / 37K normal train). Encoded 132 protocols, 14 services, and 8 states. Handled missing/inf values with training medians and applied zero-leakage standard scaling."),
        ("✓ ANOVA F-Score Feature Selection (42 → 20)",
         "Implemented SelectKBest to isolate top 20 discriminative flow attributes (e.g. sbytes, sttl, smean, ct_state_ttl), achieving a 52.4% feature dimensionality reduction without losing critical attack signatures."),
        ("✓ Lightweight CNN / Feature Extractor Implemented",
         "Constructed a lightweight 2-stage neural architecture (~3,450 parameters). Incorporates 64-unit nonlinear hidden representations and adaptive pooling, achieving rapid convergence with early-stopping patience."),
        ("✓ Standalone SVM Classifier Formulated",
         "Implemented RBF-kernel SVM (C=1.0, gamma='scale') directly on the 20 ANOVA-selected features, establishing convex maximum-margin benchmark."),
        ("✓ CNN + SVM Hybrid Architecture Formed",
         "Coupled the trained neural extractor to SVM: extracts 64-D dense nonlinear latent vectors and passes them directly to the RBF SVM decision boundary, verifying the hybrid concept."),
        ("✓ Fully Automated, Reproducible Scripting Suite",
         "All steps integrated into modular Python pipelines (`run_all.py`), generating reproducible weights, metric logs (`metrics.csv`), and academic plots.")
    ]

    prog_body = slide4.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.6), Inches(5.0))
    pb_tf = prog_body.text_frame
    pb_tf.word_wrap = True

    for title, desc in milestones:
        p_t = pb_tf.add_paragraph() if pb_tf.paragraphs[0].text else pb_tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SUCCESS_GREEN

        p_d = pb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(8.6)
        p_d.font.color.rgb = TEXT_MAIN

    # Right Container: Architecture & Flow Diagrams (Width: 6.0")
    add_card(slide4, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.8))

    diag_header = slide4.shapes.add_textbox(Inches(7.0), Inches(1.45), Inches(5.5), Inches(0.35))
    dg_tf = diag_header.text_frame
    dg_p = dg_tf.paragraphs[0]
    dg_p.text = "Implemented System Flow & Hybrid Architecture"
    dg_p.font.name = FONT_TITLE
    dg_p.font.size = Pt(14)
    dg_p.font.bold = True
    dg_p.font.color.rgb = PRIMARY_BLUE

    # Place Diagram 1 (overall_pipeline) and Diagram 4 (cnn_svm_flow)
    pipe_img = os.path.join(diagrams_dir, "overall_pipeline.png")
    hybrid_img = os.path.join(diagrams_dir, "cnn_svm_flow.png")

    if os.path.exists(pipe_img) and os.path.exists(hybrid_img):
        # Place both side by side or neatly sized
        slide4.shapes.add_picture(pipe_img, Inches(7.0), Inches(1.85), width=Inches(2.75))
        slide4.shapes.add_picture(hybrid_img, Inches(9.85), Inches(1.85), width=Inches(2.75))
    elif os.path.exists(pipe_img):
        slide4.shapes.add_picture(pipe_img, Inches(7.5), Inches(1.85), height=Inches(5.0))

    # Caption box
    cap_box = slide4.shapes.add_textbox(Inches(7.0), Inches(6.55), Inches(5.5), Inches(0.4))
    cp_tf = cap_box.text_frame
    cp_p = cp_tf.paragraphs[0]
    cp_p.alignment = PP_ALIGN.CENTER
    cp_p.text = "Fig 1: End-to-End Experimental Pipeline (Left)  |  Fig 2: Implemented CNN+SVM Hybrid (Right)"
    cp_p.font.name = FONT_BODY
    cp_p.font.size = Pt(8.5)
    cp_p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: PRELIMINARY RESULTS & BENCHMARKING (10 MARKS)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, prs, LIGHT_BG)
    add_header(slide5, "4. Preliminary Results Obtained & Reference Paper Benchmarking", "Evaluation Section 4 — [10 Marks]")

    # Top-Left: Empirical Results Table (Width: 6.8", Height: 2.5")
    add_card(slide5, Inches(0.6), Inches(1.35), Inches(6.5), Inches(2.7))

    t_head = slide5.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(6.0), Inches(0.35))
    th_p = t_head.text_frame.paragraphs[0]
    th_p.text = "Actual Measured Experimental Results (UNSW-NB15 Test Set: 175,341 flows)"
    th_p.font.name = FONT_TITLE
    th_p.font.size = Pt(12)
    th_p.font.bold = True
    th_p.font.color.rgb = PRIMARY_BLUE

    # Draw Formatted Metrics Table
    rows = 4
    cols = 7
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.85), Inches(6.1), Inches(1.6))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(1.1)  # Model
    table.columns[1].width = Inches(0.8)  # Acc
    table.columns[2].width = Inches(0.8)  # Prec
    table.columns[3].width = Inches(0.8)  # Recall
    table.columns[4].width = Inches(0.8)  # F1
    table.columns[5].width = Inches(0.9)  # Train (s)
    table.columns[6].width = Inches(0.9)  # Infer (s)

    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "Train Time", "Infer Time"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_TITLE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ["CNN",     "87.60%", "98.40%", "83.14%", "90.13%", "11.01 s",  "0.0596 s"],
        ["SVM",     "88.21%", "97.51%", "84.84%", "90.73%", "66.55 s",  "163.14 s"],
        ["CNN+SVM", "88.16%", "97.99%", "84.34%", "90.65%", "61.36 s",  "151.73 s"],
    ]

    for row_idx, row_vals in enumerate(data):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 0 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_BODY
            p.font.size = Pt(9.2)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = DARK_NAVY
            elif col_idx in [1, 4]:
                p.font.bold = True
                p.font.color.rgb = ACCENT_BLUE

    # Bottom-Left: Benchmarking with Reference Papers (Width: 6.5", Height: 2.85")
    add_card(slide5, Inches(0.6), Inches(4.2), Inches(6.5), Inches(3.0))

    b_head = slide5.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(6.0), Inches(0.35))
    bh_p = b_head.text_frame.paragraphs[0]
    bh_p.text = "Benchmarking & Comparative Analysis with Reference Literature"
    bh_p.font.name = FONT_TITLE
    bh_p.font.size = Pt(12)
    bh_p.font.bold = True
    bh_p.font.color.rgb = PRIMARY_BLUE

    bench_box = slide5.shapes.add_textbox(Inches(0.8), Inches(4.65), Inches(6.1), Inches(2.4))
    b_tf = bench_box.text_frame
    b_tf.word_wrap = True

    bench_points = [
        ("Methodological Comparison with Phalaagae et al. (IEEE Access 2025):",
         "The reference paper leverages CNN-LSTM + Attention, obtaining >95-98% accuracy but requiring recurrent unrolling over long temporal sequences. Our preliminary pipeline establishes that a lightweight CNN feature extractor + SVM retains ~88.2% accuracy and 90.7% F1 on only 20 features, slashing complex matrix multiplications."),
        ("Edge-AI Alignment with ICERECT 2025 Botnet Framework:",
         "While ICERECT 2025 utilizes deep learning for edge botnet detection, our preliminary neural model achieves an ultra-low inference time of 0.0596 seconds for 175,341 flows (~0.34 μs/sample), validating instant wire-speed throughput required for edge deployment."),
        ("False Positive Rate (FPR) Performance:",
         "CNN achieved a 2.88% FPR, and CNN+SVM achieved 3.69% FPR. High precision (>98%) ensures minimal false alarms, preventing operational alert fatigue in IoT networks."),
        ("Preliminary Stage Scope:",
         "As our project is in the initial refining stage, these genuine baseline metrics demonstrate proof-of-concept without artificial data manipulation. Subsequent phases will explore multi-class classification, quantisation, and edge microcontroller deployment.")
    ]

    for title, desc in bench_points:
        p_t = b_tf.add_paragraph() if b_tf.paragraphs[0].text else b_tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(9.3)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_BLUE

        p_d = b_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(8.2)
        p_d.font.color.rgb = TEXT_MAIN

    # Right Container: Empirical Result Graphs (Width: 5.4")
    add_card(slide5, Inches(7.3), Inches(1.35), Inches(5.4), Inches(5.85))

    g_head = slide5.shapes.add_textbox(Inches(7.5), Inches(1.45), Inches(5.0), Inches(0.35))
    gh_p = g_head.text_frame.paragraphs[0]
    gh_p.text = "Generated Experimental Visualisations"
    gh_p.font.name = FONT_TITLE
    gh_p.font.size = Pt(13)
    gh_p.font.bold = True
    gh_p.font.color.rgb = PRIMARY_BLUE

    # Add Graph 1 (model_performance_comparison) and Graph 4 (feature_reduction)
    g1_path = os.path.join(graphs_dir, "model_performance_comparison.png")
    g4_path = os.path.join(graphs_dir, "feature_reduction.png")

    if os.path.exists(g1_path) and os.path.exists(g4_path):
        slide5.shapes.add_picture(g1_path, Inches(7.5), Inches(1.85), width=Inches(5.0))
        slide5.shapes.add_picture(g4_path, Inches(7.6), Inches(4.45), width=Inches(4.8))
    elif os.path.exists(g1_path):
        slide5.shapes.add_picture(g1_path, Inches(7.5), Inches(2.0), width=Inches(5.0))

    # Save Presentation
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = current_dir
    if not os.path.exists(os.path.join(project_root, "graphs")):
        project_root = os.path.join(current_dir, "midlab_ml_experiment")

    output_file = os.path.join(project_root, "Data_Networks_MidLab_Presentation.pptx")
    create_presentation(output_file, project_root)
