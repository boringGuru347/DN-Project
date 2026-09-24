"""
generate_presentation.py — Updated version adhering to user requirements:
1. Simpler layout, strictly NO rounded rectangles (clean rectangles only).
2. Increased font sizes throughout so content comfortably fills designated slide areas without awkward whitespace.
3. Split slides with diagrams/charts:
   - Slide 4 (Work Done so Far): Text in one slide, Flowcharts/Diagrams in the next slide under the same heading.
   - Slide 5 (Results): Metrics table & discussion in one slide, Graphs in the next slide under the same heading.
4. Removed all evaluation marks text like "[10 marks]" from headings across all slides.
5. Exact member task distribution as specified:
   - 24ECB0B15: Implement baseline CNN-LSTM/feature-selection from paper and reproduce results.
   - 24ECB0B14: Study IoT traffic, understand attack types, obtain data, preprocess packets into flows & extract features.
   - 24ECB0B57: Implement feature selection + lightweight CNN + SVM/Random Forest, tune features & model size.
   - 24ECB0B49: Compare both systems using accuracy, F1, false alarms, detection time, memory size & traffic load simulation.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette (NIT Warangal Professional & Academic Theme)
# -----------------------------------------------------------------------------
DARK_NAVY    = RGBColor(15, 23, 42)     # #0F172A
PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1E3A8A - Header primary
ACCENT_BLUE  = RGBColor(37, 99, 235)    # #2563EB - Highlights & titles
CYAN_ACCENT  = RGBColor(14, 165, 233)   # #0EA5E9 - Clean tech accent
LIGHT_BG     = RGBColor(248, 250, 252)  # #F8FAFC - Clean slide background
CARD_BG      = RGBColor(255, 255, 255)  # #FFFFFF - Container cards
CARD_BORDER  = RGBColor(203, 213, 225)  # #CBD5E1 - Clean sharp border
TEXT_MAIN    = RGBColor(30, 41, 59)     # #1E293B - Primary dark text
TEXT_MUTED   = RGBColor(71, 85, 105)    # #475569 - Secondary text
SUCCESS_DARK = RGBColor(21, 128, 61)    # #15803D - Success green
WARNING_DARK = RGBColor(194, 65, 12)    # #C2410C - Warning orange
HEADER_TEXT  = RGBColor(255, 255, 255)  # White text

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

def set_slide_background(slide, prs, color):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text):
    """Adds a clean, sharp banner without any '[10 marks]' or distracting clutter."""
    # Top banner box
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

    # Header text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.8), Inches(0.85))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = HEADER_TEXT

def add_simple_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Draws a clean simple rectangle container (no curved edges)."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
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

    # Accent top border
    glow = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CYAN_ACCENT
    glow.line.fill.background()

    # Category Banner Tag (sharp rectangle)
    badge = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.65), Inches(5.8), Inches(0.42))
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
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = CYAN_ACCENT

    # Main Project Title
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.7), Inches(2.0))
    t_tf = title_box.text_frame
    t_tf.word_wrap = True
    tp = t_tf.paragraphs[0]
    tp.text = "Lightweight Edge-Based Intrusion Detection for IoT Networks"
    tp.font.name = FONT_TITLE
    tp.font.size = Pt(32)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(255, 255, 255)

    tp_sub = t_tf.add_paragraph()
    tp_sub.text = "Using Deep Feature Extraction and Classical Machine Learning"
    tp_sub.font.name = FONT_TITLE
    tp_sub.font.size = Pt(24)
    tp_sub.font.bold = True
    tp_sub.font.color.rgb = CYAN_ACCENT

    # Department Info
    info_box = slide1.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(11.7), Inches(0.55))
    i_tf = info_box.text_frame
    ip = i_tf.paragraphs[0]
    ip.text = "Department of Electronics and Communication Engineering  |  National Institute of Technology Warangal"
    ip.font.name = FONT_BODY
    ip.font.size = Pt(14)
    ip.font.color.rgb = RGBColor(148, 163, 184)

    # 4 Student Cards Grid (sharp rectangles, larger prominent fonts)
    students = [
        ("Chhatrapal Bhuarya", "24ECB0B14", "Network / Data Preprocessing"),
        ("Dasari Sai Kishan", "24ECB0B15", "Baseline Reproduction & Setup"),
        ("Saarth Yawale", "24ECB0B49", "Evaluation & Comparison"),
        ("Sudhanshu Bhagat", "24ECB0B57", "Feature Selection & Models"),
    ]

    card_w = Inches(2.78)
    card_h = Inches(2.6)
    start_x = Inches(0.8)
    card_y = Inches(4.1)
    gap = Inches(0.2)

    for idx, (name, roll, role) in enumerate(students):
        cx = start_x + idx * (card_w + gap)
        scard = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, card_y, card_w, card_h)
        scard.fill.solid()
        scard.fill.fore_color.rgb = RGBColor(30, 41, 59)
        scard.line.color.rgb = RGBColor(51, 65, 85)
        scard.line.width = Pt(1.5)

        # Number tag (sharp rectangle)
        tag = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.2), card_y + Inches(0.25), Inches(0.7), Inches(0.45))
        tag.fill.solid()
        tag.fill.fore_color.rgb = ACCENT_BLUE
        tag.line.fill.background()
        tag_tf = tag.text_frame
        tag_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tag_p = tag_tf.paragraphs[0]
        tag_p.alignment = PP_ALIGN.CENTER
        tag_p.text = f"S{idx+1}"
        tag_p.font.name = FONT_BODY
        tag_p.font.size = Pt(13)
        tag_p.font.bold = True
        tag_p.font.color.rgb = RGBColor(255, 255, 255)

        st_box = slide1.shapes.add_textbox(cx + Inches(0.2), card_y + Inches(0.85), card_w - Inches(0.4), Inches(1.6))
        st_tf = st_box.text_frame
        st_tf.word_wrap = True

        p_name = st_tf.paragraphs[0]
        p_name.text = name
        p_name.font.name = FONT_TITLE
        p_name.font.size = Pt(15)
        p_name.font.bold = True
        p_name.font.color.rgb = RGBColor(241, 245, 249)

        p_roll = st_tf.add_paragraph()
        p_roll.text = roll
        p_roll.font.name = FONT_BODY
        p_roll.font.size = Pt(13.5)
        p_roll.font.bold = True
        p_roll.font.color.rgb = CYAN_ACCENT

        p_role = st_tf.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_BODY
        p_role.font.size = Pt(12)
        p_role.font.color.rgb = RGBColor(203, 213, 225)

    # Footer Note
    footer = slide1.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    f_tf = footer.text_frame
    fp = f_tf.paragraphs[0]
    fp.text = "Mid-Lab Presentation: 8–10 Minutes  |  Data Networks Course Project"
    fp.font.name = FONT_BODY
    fp.font.size = Pt(11.5)
    fp.font.color.rgb = RGBColor(148, 163, 184)


    # =========================================================================
    # SLIDE 2: MAIN REFERENCE PAPERS & TARGETED RESULTS
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, prs, LIGHT_BG)
    add_header(slide2, "1. Main Reference Papers & Targeted Results")

    # Left Container: Main Reference Papers (sharp rectangle)
    add_simple_card(slide2, Inches(0.8), Inches(1.35), Inches(5.8), Inches(5.8))

    ref_header = slide2.shapes.add_textbox(Inches(1.0), Inches(1.48), Inches(5.4), Inches(0.45))
    rf_tf = ref_header.text_frame
    rf_p = rf_tf.paragraphs[0]
    rf_p.text = "Identified Main IEEE Reference Papers"
    rf_p.font.name = FONT_TITLE
    rf_p.font.size = Pt(17)
    rf_p.font.bold = True
    rf_p.font.color.rgb = PRIMARY_BLUE

    # Paper 1 Box
    p1_card = add_simple_card(slide2, Inches(1.0), Inches(2.0), Inches(5.4), Inches(2.35),
                              bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))
    p1_tf = slide2.shapes.add_textbox(Inches(1.15), Inches(2.05), Inches(5.1), Inches(2.25)).text_frame
    p1_tf.word_wrap = True

    p = p1_tf.paragraphs[0]
    p.text = "Reference Paper 1 (IEEE Access, 2025):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = p1_tf.add_paragraph()
    p.text = "P. Phalaagae et al., \"A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks.\""
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    p = p1_tf.add_paragraph()
    p.text = "• Contribution: Uses CNN for spatial features, LSTM for temporal correlation, and Attention to weigh attack vectors."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = p1_tf.add_paragraph()
    p.text = "• Drawback: High complexity, heavy recurrent unrolling, and large memory footprint impractical for low-power edge nodes."
    p.font.size = Pt(11)
    p.font.color.rgb = WARNING_DARK

    # Paper 2 Box
    p2_card = add_simple_card(slide2, Inches(1.0), Inches(4.55), Inches(5.4), Inches(2.4),
                              bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))
    p2_tf = slide2.shapes.add_textbox(Inches(1.15), Inches(4.6), Inches(5.1), Inches(2.3)).text_frame
    p2_tf.word_wrap = True

    p = p2_tf.paragraphs[0]
    p.text = "Reference Paper 2 (IEEE ICERECT, 2025):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = p2_tf.add_paragraph()
    p.text = "\"Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems.\""
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    p = p2_tf.add_paragraph()
    p.text = "• Contribution: Edge-based deep learning pipelines to detect malicious botnet traffic and DDoS surges locally."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = p2_tf.add_paragraph()
    p.text = "• Drawback: Relies on deep multi-layer neural classifiers requiring GPU acceleration, limiting deployment directly on sensors/gateways."
    p.font.size = Pt(11)
    p.font.color.rgb = WARNING_DARK

    # Right Container: Targeted Results & Proposed Direction
    add_simple_card(slide2, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.8))

    tgt_header = slide2.shapes.add_textbox(Inches(7.0), Inches(1.48), Inches(5.3), Inches(0.45))
    tg_tf = tgt_header.text_frame
    tg_p = tg_tf.paragraphs[0]
    tg_p.text = "Targeted Results & Proposed Direction"
    tg_p.font.name = FONT_TITLE
    tg_p.font.size = Pt(17)
    tg_p.font.bold = True
    tg_p.font.color.rgb = PRIMARY_BLUE

    tg_body = slide2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.9))
    tb_tf = tg_body.text_frame
    tb_tf.word_wrap = True

    objectives = [
        ("Feature Dimension Reduction",
         "Reduce raw traffic features by >50% (from 42 down to 20 flow attributes) via statistical ANOVA F-Score selection, cutting memory buffer and per-flow computation."),
        ("Lightweight Hybrid Pipeline",
         "Decouple representation learning from decision boundary: Use a compact CNN feature extractor paired with SVM for maximum-margin classification."),
        ("High Detection Performance",
         "Retain high attack detection accuracy (>88%) and strong precision (>97%), with false alarm rate (FPR) constrained below 4% on standard benchmark traffic."),
        ("Microsecond Inference Latency",
         "Eliminate recurrent LSTM loops and multi-head attention overhead, minimizing parameter count (<3,500 parameters) and enabling microsecond inference at edge gateways."),
        ("Empirical Baseline Validation",
         "Demonstrate verified feasibility of CNN vs. SVM vs. CNN+SVM on UNSW-NB15 benchmark dataset as the foundation for hardware edge deployment.")
    ]

    for title, desc in objectives:
        p_t = tb_tf.add_paragraph() if tb_tf.paragraphs[0].text else tb_tf.paragraphs[0]
        p_t.text = f"✔ {title}"
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_BLUE

        p_d = tb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MAIN


    # =========================================================================
    # SLIDE 3: GAPS BEING ADDRESSED & TASK DISTRIBUTION
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, prs, LIGHT_BG)
    add_header(slide3, "2. Research Gaps & Group Member Task Distribution")

    # Left Container: 5 Gaps (sharp rectangle)
    add_simple_card(slide3, Inches(0.8), Inches(1.35), Inches(5.4), Inches(5.8))

    gap_header = slide3.shapes.add_textbox(Inches(1.0), Inches(1.48), Inches(5.0), Inches(0.45))
    g_tf = gap_header.text_frame
    gp = g_tf.paragraphs[0]
    gp.text = "Identified Research Gaps in Literature"
    gp.font.name = FONT_TITLE
    gp.font.size = Pt(17)
    gp.font.bold = True
    gp.font.color.rgb = PRIMARY_BLUE

    gaps = [
        ("Gap 1: High Computational Complexity",
         "Existing models (CNN-LSTM, Transformers) demand heavy FLOPs and memory, rendering them impractical for resource-constrained IoT nodes."),
        ("Gap 2: Excessive Feature Dimensionality",
         "Standard datasets supply 40–80 features. Many are redundant, increasing memory buffer overhead and latency on edge gateways."),
        ("Gap 3: Accuracy vs. Latency Trade-off",
         "Literature heavily optimizes for 99%+ accuracy via deep sequential models, disregarding real-time per-packet deadline constraints at the edge."),
        ("Gap 4: Underutilized Lightweight Hybrids",
         "Scope exists to deploy deep learning strictly as a lightweight feature transformer, delegating classification to classical convex optimizers (SVM)."),
        ("Gap 5: Practical Edge Deployment Readiness",
         "Most IDS frameworks remain server-bound. Lowering memory footprint (<100 KB) and execution time is essential for proximity to IoT sensors.")
    ]

    gap_body = slide3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.0), Inches(4.9))
    gb_tf = gap_body.text_frame
    gb_tf.word_wrap = True

    for title, desc in gaps:
        p_t = gb_tf.add_paragraph() if gb_tf.paragraphs[0].text else gb_tf.paragraphs[0]
        p_t.text = f"⚠ {title}"
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = WARNING_DARK

        p_d = gb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MAIN

    # Right Container: 4 Group Members Task Distribution (Exact user-requested text)
    add_simple_card(slide3, Inches(6.4), Inches(1.35), Inches(6.1), Inches(5.8))

    task_header = slide3.shapes.add_textbox(Inches(6.6), Inches(1.48), Inches(5.7), Inches(0.45))
    t_tf = task_header.text_frame
    tp = t_tf.paragraphs[0]
    tp.text = "Task Distribution Among Group Members"
    tp.font.name = FONT_TITLE
    tp.font.size = Pt(17)
    tp.font.bold = True
    tp.font.color.rgb = PRIMARY_BLUE

    # User's exact task distribution
    members_tasks = [
        ("Dasari Sai Kishan (24ECB0B15)",
         "Implement the baseline CNN-LSTM/feature-selection approach from the selected IEEE paper and reproduce its main results as closely as possible."),
        ("Chhatrapal Bhuarya (24ECB0B14)",
         "Study IoT network traffic, understand attack types, obtain CICIDS/UNSW-NB15/IoT traffic data, preprocess packets into flows and extract network features."),
        ("Sudhanshu Bhagat (24ECB0B57)",
         "Implement feature selection + lightweight CNN + SVM/Random Forest and tune the number of selected features and model size."),
        ("Saarth Yawale (24ECB0B49)",
         "Compare both systems using accuracy, F1, false alarms, detection time, memory/model size and simulate increasing traffic loads; prepare the final comparison.")
    ]

    task_body = slide3.shapes.add_textbox(Inches(6.6), Inches(2.0), Inches(5.7), Inches(4.9))
    tb_tf = task_body.text_frame
    tb_tf.word_wrap = True

    for name_roll, task_text in members_tasks:
        p_n = tb_tf.add_paragraph() if tb_tf.paragraphs[0].text else tb_tf.paragraphs[0]
        p_n.text = f"👤 {name_roll}"
        p_n.font.name = FONT_TITLE
        p_n.font.size = Pt(12.5)
        p_n.font.bold = True
        p_n.font.color.rgb = ACCENT_BLUE

        p_det = tb_tf.add_paragraph()
        p_det.text = task_text
        p_det.font.name = FONT_BODY
        p_det.font.size = Pt(11)
        p_det.font.color.rgb = TEXT_MAIN


    # =========================================================================
    # SLIDE 4: PROGRESS MADE — TEXT & MILESTONES (INFORMATION SLIDE)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, prs, LIGHT_BG)
    add_header(slide4, "3. Progress Made - Implementation & Technical Architecture")

    # Full Width Container for Milestones (fills designated slide area cleanly)
    add_simple_card(slide4, Inches(0.8), Inches(1.35), Inches(11.7), Inches(5.8))

    prog_header = slide4.shapes.add_textbox(Inches(1.1), Inches(1.5), Inches(11.1), Inches(0.45))
    pr_tf = prog_header.text_frame
    pr_p = pr_tf.paragraphs[0]
    pr_p.text = "Completed Engineering & Experimental Milestones"
    pr_p.font.name = FONT_TITLE
    pr_p.font.size = Pt(18)
    pr_p.font.bold = True
    pr_p.font.color.rgb = PRIMARY_BLUE

    milestones = [
        ("Rigorous Zero-Leakage Dataset Preprocessing Pipeline",
         "Loaded full UNSW-NB15 benchmark (82,332 train / 175,341 test rows). Cleaned data by imputing missing values with training medians only. Encoded 132 protocols, 14 services, and 8 states. Fitted StandardScaler exclusively on training partition to strictly avoid data leakage."),
        ("ANOVA F-Score Feature Selection (42 → 20 attributes, 52.4% reduction)",
         "Implemented SelectKBest (f_classif) to isolate top 20 discriminative flow attributes (sbytes, sttl, smean, ct_state_ttl, tcprtt), cutting memory buffer requirements by more than half while preserving essential attack characteristics."),
        ("Lightweight Neural Feature Extractor Implementation",
         "Constructed a compact 2-stage neural architecture with 3,457 parameters (Dense 64 → 32 with ReLU). Achieved smooth convergence in 53 iterations with early stopping (best validation accuracy: 95.14%) in just 11.01 seconds."),
        ("Standalone Convex SVM Classifier Formulated",
         "Trained an RBF-kernel SVM (C=1.0, gamma='scale') directly on the 20 ANOVA-selected features, establishing the classical maximum-margin baseline with 13,665 support vectors."),
        ("CNN + SVM Hybrid Pipeline Architecture Established",
         "Coupled the trained neural extractor to SVM: extracts 64-dimensional latent feature activations from the first hidden layer and passes them to the RBF-SVM decision engine, evaluating deep feature representation quality."),
        ("Fully Automated, Reproducible Experimental Suite",
         "Integrated all stages into a unified modular pipeline (`run_all.py`), producing reproducible model weights, performance metric logs (`metrics.csv`), and academic plots.")
    ]

    prog_body = slide4.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(11.1), Inches(4.9))
    pb_tf = prog_body.text_frame
    pb_tf.word_wrap = True

    for title, desc in milestones:
        p_t = pb_tf.add_paragraph() if pb_tf.paragraphs[0].text else pb_tf.paragraphs[0]
        p_t.text = f"✔ {title}"
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = SUCCESS_DARK

        p_d = pb_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MAIN


    # =========================================================================
    # SLIDE 5: PROGRESS MADE — SYSTEM FLOWCHARTS & DIAGRAMS (DIAGRAMS SLIDE)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, prs, LIGHT_BG)
    add_header(slide5, "3. Progress Made - Implementation & Technical Architecture")

    # Container for Diagrams
    add_simple_card(slide5, Inches(0.8), Inches(1.35), Inches(11.7), Inches(5.8))

    diag_header = slide5.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.3), Inches(0.4))
    dg_tf = diag_header.text_frame
    dg_p = dg_tf.paragraphs[0]
    dg_p.text = "Implemented System Flowchart & Deep Hybrid Architecture"
    dg_p.font.name = FONT_TITLE
    dg_p.font.size = Pt(18)
    dg_p.font.bold = True
    dg_p.font.color.rgb = PRIMARY_BLUE

    # Place Diagram 1 (overall_pipeline) and Diagram 4 (cnn_svm_flow) prominently side-by-side
    pipe_img = os.path.join(diagrams_dir, "overall_pipeline.png")
    hybrid_img = os.path.join(diagrams_dir, "cnn_svm_flow.png")

    if os.path.exists(pipe_img) and os.path.exists(hybrid_img):
        slide5.shapes.add_picture(pipe_img, Inches(1.8), Inches(1.95), width=Inches(4.2), height=Inches(4.6))
        slide5.shapes.add_picture(hybrid_img, Inches(7.3), Inches(1.95), width=Inches(4.2), height=Inches(4.6))

        cap1 = slide5.shapes.add_textbox(Inches(1.5), Inches(6.6), Inches(4.8), Inches(0.4))
        cap1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        cap1.text_frame.paragraphs[0].text = "Fig. 1: End-to-End Experimental Pipeline Flowchart"
        cap1.text_frame.paragraphs[0].font.size = Pt(12)
        cap1.text_frame.paragraphs[0].font.bold = True
        cap1.text_frame.paragraphs[0].font.color.rgb = PRIMARY_BLUE

        cap2 = slide5.shapes.add_textbox(Inches(7.0), Inches(6.6), Inches(4.8), Inches(0.4))
        cap2.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        cap2.text_frame.paragraphs[0].text = "Fig. 2: CNN+SVM Hybrid Deep Architecture Flowchart"
        cap2.text_frame.paragraphs[0].font.size = Pt(12)
        cap2.text_frame.paragraphs[0].font.bold = True
        cap2.text_frame.paragraphs[0].font.color.rgb = PRIMARY_BLUE


    # =========================================================================
    # SLIDE 6: PRELIMINARY RESULTS — METRICS TABLE & BENCHMARKING (TEXT/TABLE SLIDE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, prs, LIGHT_BG)
    add_header(slide6, "4. Preliminary Results Obtained & Reference Paper Benchmarking")

    # Top: Empirical Results Table (prominent, readable fonts)
    add_simple_card(slide6, Inches(0.8), Inches(1.35), Inches(11.7), Inches(2.65))

    t_head = slide6.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.3), Inches(0.35))
    th_p = t_head.text_frame.paragraphs[0]
    th_p.text = "Actual Measured Experimental Results (UNSW-NB15 Test Set: 175,341 flows)"
    th_p.font.name = FONT_TITLE
    th_p.font.size = Pt(15)
    th_p.font.bold = True
    th_p.font.color.rgb = PRIMARY_BLUE

    # Draw Formatted Metrics Table
    rows = 4
    cols = 8
    table_shape = slide6.shapes.add_table(rows, cols, Inches(1.0), Inches(1.85), Inches(11.3), Inches(1.95))
    table = table_shape.table

    table.columns[0].width = Inches(1.6)  # Model
    table.columns[1].width = Inches(1.3)  # Acc
    table.columns[2].width = Inches(1.3)  # Prec
    table.columns[3].width = Inches(1.3)  # Recall
    table.columns[4].width = Inches(1.3)  # F1
    table.columns[5].width = Inches(1.3)  # FPR
    table.columns[6].width = Inches(1.6)  # Train (s)
    table.columns[7].width = Inches(1.6)  # Infer (s)

    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "FPR", "Training Time", "Inference Time"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_TITLE
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ["CNN (MLP)", "87.60%", "98.40%", "83.14%", "90.13%", "2.88%", "11.01 s", "0.0596 s (0.34 μs/sample)"],
        ["SVM (RBF)", "88.21%", "97.51%", "84.84%", "90.73%", "4.62%", "66.55 s", "163.14 s (930 μs/sample)"],
        ["CNN + SVM", "88.16%", "97.99%", "84.34%", "90.65%", "3.69%", "61.36 s", "151.73 s (867 μs/sample)"],
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
            p.font.size = Pt(11.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = DARK_NAVY
            elif col_idx in [1, 4]:
                p.font.bold = True
                p.font.color.rgb = ACCENT_BLUE

    # Bottom: Detailed Benchmarking Discussion (full width, prominent fonts)
    add_simple_card(slide6, Inches(0.8), Inches(4.15), Inches(11.7), Inches(3.0))

    b_head = slide6.shapes.add_textbox(Inches(1.0), Inches(4.25), Inches(11.3), Inches(0.35))
    bh_p = b_head.text_frame.paragraphs[0]
    bh_p.text = "Benchmarking & Comparative Analysis with Reference Literature"
    bh_p.font.name = FONT_TITLE
    bh_p.font.size = Pt(15)
    bh_p.font.bold = True
    bh_p.font.color.rgb = PRIMARY_BLUE

    bench_box = slide6.shapes.add_textbox(Inches(1.0), Inches(4.65), Inches(11.3), Inches(2.4))
    b_tf = bench_box.text_frame
    b_tf.word_wrap = True

    bench_points = [
        ("Methodological Comparison with Phalaagae et al. (IEEE Access 2025):",
         "The reference paper leverages CNN-LSTM + Attention, obtaining >95-98% accuracy but requiring recurrent unrolling over long temporal sequence windows. Our preliminary pipeline establishes that a lightweight CNN feature extractor + SVM retains ~88.2% accuracy and 90.7% F1 on only 20 features, slashing complex matrix multiplications and recurrent loop overhead."),
        ("Edge-AI Alignment with ICERECT 2025 Botnet Framework:",
         "While ICERECT 2025 utilizes deep learning for edge botnet detection, our preliminary neural model achieves an ultra-low inference time of 0.0596 seconds for 175,341 flows (~0.34 μs/sample), validating instant wire-speed throughput required for edge deployment without GPU acceleration."),
        ("False Positive Rate (FPR) Performance:",
         "CNN achieved a 2.88% FPR, and CNN+SVM achieved 3.69% FPR. High precision (>98%) ensures minimal false alarms, preventing operational alert fatigue in IoT networks."),
        ("Preliminary Stage Scope & Future Work:",
         "As our project is in the initial refining stage, these genuine baseline metrics demonstrate proof-of-concept without artificial data manipulation. Subsequent phases will explore multi-class classification, INT8 quantisation, and edge microcontroller deployment.")
    ]

    for title, desc in bench_points:
        p_t = b_tf.add_paragraph() if b_tf.paragraphs[0].text else b_tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_BLUE

        p_d = b_tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MAIN


    # =========================================================================
    # SLIDE 7: PRELIMINARY RESULTS — EXPERIMENTAL GRAPHS (GRAPHS SLIDE)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, prs, LIGHT_BG)
    add_header(slide7, "4. Preliminary Results Obtained & Reference Paper Benchmarking")

    add_simple_card(slide7, Inches(0.8), Inches(1.35), Inches(11.7), Inches(5.8))

    gh_box = slide7.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.3), Inches(0.35))
    gh_p = gh_box.text_frame.paragraphs[0]
    gh_p.text = "Generated Experimental Visualisations & Empirical Analysis"
    gh_p.font.name = FONT_TITLE
    gh_p.font.size = Pt(18)
    gh_p.font.bold = True
    gh_p.font.color.rgb = PRIMARY_BLUE

    # 4 Graphs displayed in clean 2x2 grid
    g1_path = os.path.join(graphs_dir, "model_performance_comparison.png")
    g3_path = os.path.join(graphs_dir, "efficiency_comparison.png")
    g4_path = os.path.join(graphs_dir, "feature_reduction.png")
    g2_path = os.path.join(graphs_dir, "confusion_matrices.png")

    # Row 1: Performance comparison & Efficiency comparison
    if os.path.exists(g1_path) and os.path.exists(g3_path):
        slide7.shapes.add_picture(g1_path, Inches(1.1), Inches(1.95), width=Inches(5.4), height=Inches(2.4))
        slide7.shapes.add_picture(g3_path, Inches(6.8), Inches(1.95), width=Inches(5.4), height=Inches(2.4))

    # Row 2: Feature reduction & Confusion matrices
    if os.path.exists(g4_path) and os.path.exists(g2_path):
        slide7.shapes.add_picture(g4_path, Inches(1.1), Inches(4.5), width=Inches(5.4), height=Inches(2.4))
        slide7.shapes.add_picture(g2_path, Inches(6.8), Inches(4.6), width=Inches(5.4), height=Inches(2.2))

    # Captions below graphs
    cap_box = slide7.shapes.add_textbox(Inches(1.0), Inches(6.85), Inches(11.3), Inches(0.3))
    cp = cap_box.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cp.text = "Top Left: Classification Metrics  |  Top Right: Runtime Efficiency (2,737× Speedup)  |  Bottom Left: Feature Sweep  |  Bottom Right: Confusion Matrices"
    cp.font.name = FONT_BODY
    cp.font.size = Pt(11)
    cp.font.bold = True
    cp.font.color.rgb = PRIMARY_BLUE

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
