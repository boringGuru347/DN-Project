"""
generate_final_evaluation_ppt.py — Clean, pristine formatting without any overlap:
Slide 1: Original Research Paper Result & 1-Minute Concept Overview (Projector Background with Title, Names, Roll Numbers)
Slide 2: Final Results Obtained (Clean table without overlap, proper column widths, spacious deductions box)
Slide 3: Graphs of Original Research Paper Comparison (Clear non-overlapping axis labels, proper headroom)
Slide 4: Graphs of Final Result (Cleanly spaced 4 quadrants with 2x2 confusion matrix grid)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Color Palette
DARK_NAVY    = RGBColor(15, 23, 42)     # #0F172A
PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1E3A8A
ACCENT_BLUE  = RGBColor(37, 99, 235)    # #2563EB
CYAN_ACCENT  = RGBColor(14, 165, 233)   # #0EA5E9
LIGHT_BG     = RGBColor(248, 250, 252)  # #F8FAFC
CARD_BG      = RGBColor(255, 255, 255)  # #FFFFFF
CARD_BORDER  = RGBColor(203, 213, 225)  # #CBD5E1
TEXT_MAIN    = RGBColor(30, 41, 59)     # #1E293B
TEXT_MUTED   = RGBColor(71, 85, 105)    # #475569
SUCCESS_DARK = RGBColor(21, 128, 61)    # #15803D
WARNING_DARK = RGBColor(194, 65, 12)    # #C2410C
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

def add_header(slide, title_text, sub_title=None):
    """Header banner across slides."""
    header_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.10)
    )
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = PRIMARY_BLUE
    header_box.line.fill.background()

    stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.10), Inches(13.333), Inches(0.05)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = CYAN_ACCENT
    stripe.line.fill.background()

    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.08), Inches(11.8), Inches(0.95))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = HEADER_TEXT

    if sub_title:
        p2 = tf.add_paragraph()
        p2.text = sub_title
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(191, 219, 254)

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.1)
    return card

def build_presentation(output_path, project_root):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    graphs_dir = os.path.join(project_root, "graphs")

    # =========================================================================
    # SLIDE 1: ORIGINAL RESEARCH PAPER RESULT & 1-MINUTE CONCEPT OVERVIEW
    # (Projector Background with Project Title, Student Names, Roll Numbers)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, prs, LIGHT_BG)

    top_banner = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.75)
    )
    top_banner.fill.solid()
    top_banner.fill.fore_color.rgb = DARK_NAVY
    top_banner.line.fill.background()

    t_stripe = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.75), Inches(13.333), Inches(0.05)
    )
    t_stripe.fill.solid()
    t_stripe.fill.fore_color.rgb = CYAN_ACCENT
    t_stripe.line.fill.background()

    tb_box = slide1.shapes.add_textbox(Inches(0.6), Inches(0.08), Inches(12.133), Inches(0.85))
    tf1 = tb_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Lightweight Edge-Based Intrusion Detection for IoT Networks"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Using Deep Feature Extraction and Classical Machine Learning  |  Data Networks Lab Final Evaluation"
    p1_sub.font.name = FONT_TITLE
    p1_sub.font.size = Pt(12.5)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = CYAN_ACCENT

    team_box = slide1.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12.133), Inches(0.7))
    tf_team = team_box.text_frame
    tf_team.word_wrap = True
    p_team = tf_team.paragraphs[0]
    p_team.text = "Chhatrapal Bhuarya (24ECB0B14)   |   Dasari Sai Kishan (24ECB0B15)   |   Saarth Yawale (24ECB0B49)   |   Sudhanshu Bhagat (24ECB0B57)"
    p_team.font.name = FONT_BODY
    p_team.font.size = Pt(11.5)
    p_team.font.bold = True
    p_team.font.color.rgb = RGBColor(241, 245, 249)

    p_dept = tf_team.add_paragraph()
    p_dept.text = "Department of Electronics and Communication Engineering  •  National Institute of Technology Warangal"
    p_dept.font.name = FONT_BODY
    p_dept.font.size = Pt(10.5)
    p_dept.font.color.rgb = RGBColor(148, 163, 184)

    # Left Container: 1-Minute Project Concept
    add_card(slide1, Inches(0.6), Inches(1.95), Inches(5.8), Inches(5.3))
    c_head = slide1.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(5.4), Inches(0.4))
    cp = c_head.text_frame.paragraphs[0]
    cp.text = "1-Minute Project Concept & Motivation"
    cp.font.name = FONT_TITLE
    cp.font.size = Pt(15.5)
    cp.font.bold = True
    cp.font.color.rgb = PRIMARY_BLUE

    c_body = slide1.shapes.add_textbox(Inches(0.8), Inches(2.50), Inches(5.4), Inches(4.6))
    c_tf = c_body.text_frame
    c_tf.word_wrap = True

    concept_points = [
        ("The Problem in Edge IoT:",
         "IoT networks generate massive flow volumes, but individual edge gateways have strict CPU and memory limits. Offloading all traffic to cloud servers causes latency, bandwidth bottlenecks, and security vulnerabilities."),
        ("Drawback of Modern IEEE Solutions:",
         "Recent IEEE works deploy deep sequential models (CNN-LSTM with Attention). While highly accurate, they demand over 500,000 parameters and complex recurrent unrolling, leading to packet drops at line rate."),
        ("Our Core Engineering Hypothesis:",
         "We decouple feature representation from the decision boundary: By reducing redundant features by >60% and deploying a lightweight non-linear model, we can achieve >91% accuracy at microsecond latency on low-cost microcontrollers.")
    ]
    for title, desc in concept_points:
        pt = c_tf.add_paragraph() if c_tf.paragraphs[0].text else c_tf.paragraphs[0]
        pt.text = f"• {title}"
        pt.font.name = FONT_TITLE
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = ACCENT_BLUE

        pd = c_tf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = TEXT_MAIN

    # Right Container: Original Research Paper Benchmark
    add_card(slide1, Inches(6.6), Inches(1.95), Inches(6.1), Inches(5.3))
    r_head = slide1.shapes.add_textbox(Inches(6.8), Inches(2.05), Inches(5.7), Inches(0.4))
    rp = r_head.text_frame.paragraphs[0]
    rp.text = "Original Research Paper Benchmark (Baseline)"
    rp.font.name = FONT_TITLE
    rp.font.size = Pt(15.5)
    rp.font.bold = True
    rp.font.color.rgb = PRIMARY_BLUE

    r_body = slide1.shapes.add_textbox(Inches(6.8), Inches(2.50), Inches(5.7), Inches(1.6))
    r_tf = r_body.text_frame
    r_tf.word_wrap = True

    p = r_tf.paragraphs[0]
    p.text = "Reference Paper: P. Phalaagae et al., IEEE Access (2025)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WARNING_DARK

    p = r_tf.add_paragraph()
    p.text = "\"A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks\""
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    p = r_tf.add_paragraph()
    p.text = "• Architecture: Conv1D (Spatial) + Bidirectional LSTM (Temporal) + Multi-Head Self-Attention"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MAIN

    # Baseline Metric Table
    rows = 6
    cols = 3
    t_shape = slide1.shapes.add_table(rows, cols, Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.7))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.3)
    tbl.columns[1].width = Inches(1.7)
    tbl.columns[2].width = Inches(1.7)

    base_headers = ["Metric / Parameter", "Original IEEE Paper", "Operational Edge Impact"]
    for c_idx, h in enumerate(base_headers):
        cell = tbl.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_TITLE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    base_data = [
        ["Model Complexity", "512,000 weights", "Exceeds SRAM limits"],
        ["Inference Workload", "3.5 MFLOPs / flow", "High GPU dependency"],
        ["Per-Flow Latency", "~120 μs / sample", "Bottleneck for line rate"],
        ["Memory Footprint", "~28.4 MB RAM", "Impractical for microcontrollers"],
        ["Feature Ingestion", "42–49 raw features", "Heavy gateway buffer overhead"],
    ]
    for r_idx, r_vals in enumerate(base_data):
        for c_idx, val in enumerate(r_vals):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 0 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
            elif c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = WARNING_DARK

    # =========================================================================
    # SLIDE 2: FINAL RESULTS OBTAINED BY OUR MODEL (NO OVERLAP, PERFECT ALIGNMENT)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, prs, LIGHT_BG)
    add_header(slide2, "Final Results Obtained - Benchmark on 175,341 UNSW-NB15 Test Flows",
               "15 Selected Features (64.3% Reduction)  |  Tested on Complete Unseen Testing Partition")

    # Card 1: Table Container (Height: 2.70", Top: 1.25")
    add_card(slide2, Inches(0.6), Inches(1.25), Inches(12.133), Inches(2.72))

    t_head2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.32), Inches(11.7), Inches(0.30))
    th2 = t_head2.text_frame.paragraphs[0]
    th2.text = "Actual Measured Experimental Results (UNSW-NB15 Benchmark Test Set: 175,341 flows)"
    th2.font.name = FONT_TITLE
    th2.font.size = Pt(13.5)
    th2.font.bold = True
    th2.font.color.rgb = PRIMARY_BLUE

    # Draw Table inside Card 1 (Top: 1.68")
    t_shape2 = slide2.shapes.add_table(5, 10, Inches(0.8), Inches(1.68), Inches(11.733), Inches(2.15))
    t2 = t_shape2.table

    # Column widths strictly adjusted so "Features" NEVER wraps and model names fit cleanly
    col_w = [
        Inches(2.50),  # Model
        Inches(0.95),  # Acc
        Inches(0.95),  # Prec
        Inches(0.95),  # Recall
        Inches(0.95),  # F1
        Inches(0.85),  # FPR
        Inches(1.05),  # Train
        Inches(1.25),  # Infer 175k
        Inches(1.30),  # Latency
        Inches(0.98),  # Features
    ]
    for i, w in enumerate(col_w):
        t2.columns[i].width = w

    headers2 = [
        "Model", "Accuracy", "Precision", "Recall", "F1-Score",
        "FPR", "Training Time", "Inference Time\n(175k flows)", "Per-Sample\nLatency", "Features"
    ]
    for c_idx, h in enumerate(headers2):
        cell = t2.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        cell.margin_left = Inches(0.04)
        cell.margin_right = Inches(0.04)
        cell.margin_top = Inches(0.03)
        cell.margin_bottom = Inches(0.03)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_TITLE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    data2 = [
        ["Proposed Model (Lightweight Ensemble)", "91.34%", "97.07%", "89.99%", "93.40%", "5.80%", "0.38 s", "0.2211 s", "1.26 μs", "15"],
        ["Rerun SVM (RBF Kernel)",                "90.31%", "97.69%", "87.84%", "92.50%", "4.43%", "43.46 s", "167.70 s", "956.4 μs", "15"],
        ["Rerun CNN+SVM (Hybrid)",                  "89.67%", "98.42%", "86.21%", "91.91%", "2.96%", "63.94 s", "142.39 s", "812.1 μs", "15"],
        ["Rerun CNN (MLP Feature Extractor)",      "89.38%", "98.64%", "85.57%", "91.64%", "2.51%", "6.39 s",  "0.0498 s", "0.28 μs",  "15"],
    ]

    for r_idx, r_vals in enumerate(data2):
        for c_idx, val in enumerate(r_vals):
            cell = t2.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.margin_left = Inches(0.04)
            cell.margin_right = Inches(0.04)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)

            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # Soft Emerald highlight
            else:
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = SUCCESS_DARK if r_idx == 0 else DARK_NAVY
            elif c_idx in [1, 4]:
                p.font.bold = True
                p.font.color.rgb = SUCCESS_DARK if r_idx == 0 else ACCENT_BLUE

    # Card 2: Key Deductions & Technical Observations (Top: 4.15", completely separated!)
    add_card(slide2, Inches(0.6), Inches(4.15), Inches(12.133), Inches(3.10))
    i_head = slide2.shapes.add_textbox(Inches(0.8), Inches(4.25), Inches(11.7), Inches(0.35))
    ih = i_head.text_frame.paragraphs[0]
    ih.text = "Key Deductions and Technical Observations from the Final Results"
    ih.font.name = FONT_TITLE
    ih.font.size = Pt(13.5)
    ih.font.bold = True
    ih.font.color.rgb = PRIMARY_BLUE

    i_body = slide2.shapes.add_textbox(Inches(0.8), Inches(4.65), Inches(11.7), Inches(2.50))
    itf = i_body.text_frame
    itf.word_wrap = True

    takeaways = [
        ("Target Accuracy Benchmark Exceeded (>90%):",
         "The Proposed Model achieves 91.34% accuracy and 93.40% F1-score on only 15 features, capturing 107,399 out of 119,341 real attacks."),
        ("Sub-Microsecond Wire-Speed Inference:",
         "Our Proposed Model inspects all 175,341 flows in 0.2211 s (~1.26 μs/packet), running over 750× faster than SVM and clearing IoT wire-speed line-rate limits (<10 μs)."),
        ("Lowest False Alarm Rate (FPR = 2.51%):",
         "The CNN Feature Extractor achieved 98.64% precision and only 2.51% FPR (only 1,404 false alarms out of 56,000 benign packets), preventing operational alert fatigue."),
        ("Dimensionality Reduction (42 → 15 features, 64.3%):",
         "Eliminated 27 redundant attributes, reducing per-packet gateway buffer RAM while improving model generalization across unseen test distributions.")
    ]

    for title, desc in takeaways:
        pt = itf.add_paragraph() if itf.paragraphs[0].text else itf.paragraphs[0]
        pt.text = f"✔ {title} "
        pt.font.name = FONT_TITLE
        pt.font.size = Pt(10.5)
        pt.font.bold = True
        pt.font.color.rgb = SUCCESS_DARK

        run = pt.add_run()
        run.text = desc
        run.font.name = FONT_BODY
        run.font.size = Pt(10)
        run.font.bold = False
        run.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 3: GRAPHS OF ORIGINAL RESULT & RESOURCE BENCHMARK
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, prs, LIGHT_BG)
    add_header(slide3, "Comparative Analysis: Original IEEE Paper vs. Our Models",
               "Evaluating Computational Complexity, Memory Footprint, and Processing Latency")

    add_card(slide3, Inches(0.6), Inches(1.25), Inches(12.133), Inches(6.0))

    g3_img = os.path.join(graphs_dir, "computational_power_comparison.png")
    g4_img = os.path.join(graphs_dir, "processing_time_comparison.png")

    if os.path.exists(g3_img) and os.path.exists(g4_img):
        slide3.shapes.add_picture(g3_img, Inches(0.8), Inches(1.40), width=Inches(5.75), height=Inches(4.35))
        slide3.shapes.add_picture(g4_img, Inches(6.78), Inches(1.40), width=Inches(5.75), height=Inches(4.35))

    # Captions below both graphs
    c1 = slide3.shapes.add_textbox(Inches(0.8), Inches(5.82), Inches(5.75), Inches(1.30))
    c1_tf = c1.text_frame
    c1_tf.word_wrap = True
    p = c1_tf.paragraphs[0]
    p.text = "Fig 1: Computational Power & Resource Benchmark (Log Scale)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p_desc = c1_tf.add_paragraph()
    p_desc.text = "• Parameters reduced from 512,000 (IEEE paper) to 12,400 (97.6% reduction).\n• Operations reduced from 3.5 MFLOPs to 1,200 comparisons (>99.9% reduction).\n• Memory allocation slashed from 28.4 MB to 482 KB (deployable on microcontroller SRAM)."
    p_desc.font.size = Pt(9)
    p_desc.font.color.rgb = TEXT_MUTED

    c2 = slide3.shapes.add_textbox(Inches(6.78), Inches(5.82), Inches(5.75), Inches(1.30))
    c2_tf = c2.text_frame
    c2_tf.word_wrap = True
    p2 = c2_tf.paragraphs[0]
    p2.text = "Fig 2: Processing Time & Latency Comparison (Log Scale)"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = PRIMARY_BLUE
    p2_desc = c2_tf.add_paragraph()
    p2_desc.text = "• Training duration slashed from 1,850 s (~31 min GPU) to 0.38 s (>4,800× speedup).\n• Per-flow latency reduced from ~120 μs to 1.26 μs (95× faster inference).\n• Easily meets the 10 μs IoT wire-speed line-rate threshold without GPU acceleration."
    p2_desc.font.size = Pt(9)
    p2_desc.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: GRAPHS OF FINAL RESULTS (NO OVERLAP, 4 CLEAN QUADRANTS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, prs, LIGHT_BG)
    add_header(slide4, "Final Result Visualisations - Empirical Deductions & Validation",
               "Model Metrics, Confusion Matrices, Feature Importance, and Dimensionality Reduction Curve")

    add_card(slide4, Inches(0.6), Inches(1.25), Inches(12.133), Inches(6.0))

    g1_img = os.path.join(graphs_dir, "model_performance_comparison.png")
    g2_img = os.path.join(graphs_dir, "confusion_matrices.png")
    g5_img = os.path.join(graphs_dir, "feature_importance_ranking.png")
    g6_img = os.path.join(graphs_dir, "feature_reduction_vs_accuracy.png")

    # 4 Quadrants:
    # Top-Left: Model Performance (g1)
    if os.path.exists(g1_img):
        slide4.shapes.add_picture(g1_img, Inches(0.8), Inches(1.38), width=Inches(5.75), height=Inches(2.62))

    # Top-Right: Feature Reduction vs Accuracy Curve (g6)
    if os.path.exists(g6_img):
        slide4.shapes.add_picture(g6_img, Inches(6.78), Inches(1.38), width=Inches(5.75), height=Inches(2.62))

    # Bottom-Left: Feature Importance Ranking (g5)
    if os.path.exists(g5_img):
        slide4.shapes.add_picture(g5_img, Inches(0.8), Inches(4.12), width=Inches(5.75), height=Inches(2.72))

    # Bottom-Right: 2x2 Confusion Matrices (g2)
    if os.path.exists(g2_img):
        # Position 2x2 confusion matrix cleanly in right quadrant
        slide4.shapes.add_picture(g2_img, Inches(7.15), Inches(4.10), width=Inches(5.0), height=Inches(2.75))

    # Captions below quadrants
    lbl_box = slide4.shapes.add_textbox(Inches(0.8), Inches(6.90), Inches(11.7), Inches(0.32))
    lp = lbl_box.text_frame.paragraphs[0]
    lp.alignment = PP_ALIGN.CENTER
    lp.text = "Top Left: Classification Scores  |  Top Right: Feature Sweep (k=15 Sweet Spot)  |  Bottom Left: Top 15 Feature Importances  |  Bottom Right: Confusion Matrices"
    lp.font.name = FONT_BODY
    lp.font.size = Pt(10)
    lp.font.bold = True
    lp.font.color.rgb = PRIMARY_BLUE

    prs.save(output_path)
    print(f"Final presentation created successfully at: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = current_dir
    output_file = os.path.join(project_root, "Data_Networks_Final_Evaluation_Presentation.pptx")
    build_presentation(output_file, project_root)
