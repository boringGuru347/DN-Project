# DN Mid-Lab Preliminary ML Experiment

**Course:** Data Networks  
**Institution:** NIT Warangal  
**Purpose:** Preliminary mid-lab review experiment — CNN, SVM, and CNN+SVM for IoT intrusion detection

---

## Overview

This repository contains the preliminary ML experiment for our Data Networks project.  
We implement and compare **three models only**:

1. **CNN** — standalone 1-D convolutional classifier on network traffic features
2. **SVM** — standalone Support Vector Machine classifier on selected features
3. **CNN + SVM** — CNN as feature extractor, SVM as final classifier

**Dataset:** UNSW-NB15 (University of New South Wales, Canberra)  
**Task:** Binary classification — Normal traffic vs. Attack traffic  
**Features used:** 20 selected features (from 49 original) via ANOVA F-score selection

---

## Folder Structure

```
midlab_ml_experiment/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/                         ← place dataset CSV files here
│   └── dataset_instructions.md
│
├── src/
│   ├── utils.py                     ← shared constants and helpers
│   ├── preprocessing.py             ← data loading, cleaning, encoding, scaling
│   ├── feature_selection.py         ← SelectKBest feature reduction
│   ├── cnn_model.py                 ← CNN architecture definition
│   ├── svm_model.py                 ← SVM model definition
│   ├── cnn_svm_model.py             ← CNN+SVM hybrid (extractor + SVM)
│   ├── train_cnn.py                 ← train and save standalone CNN
│   ├── train_svm.py                 ← train and save standalone SVM
│   ├── train_cnn_svm.py             ← train and save CNN+SVM pipeline
│   ├── evaluate.py                  ← compute and save all metrics
│   ├── generate_graphs.py           ← produce all 5 result graphs
│   ├── generate_diagrams.py         ← produce flow diagrams
│   └── run_all.py                   ← master script — runs everything in order
│
├── results/
│   ├── metrics.csv                  ← per-model detailed metrics (generated)
│   ├── model_comparison.csv         ← summary comparison table (generated)
│   ├── models/                      ← saved trained models
│   └── confusion_matrices/          ← confusion matrix images
│
├── graphs/
│   ├── model_performance_comparison.png
│   ├── confusion_matrices.png
│   ├── efficiency_comparison.png
│   ├── feature_reduction.png
│   └── cnn_training_history.png
│
├── diagrams/
│   ├── overall_pipeline.png
│   ├── cnn_flow.png
│   ├── svm_flow.png
│   └── cnn_svm_flow.png
│
└── theory/
    └── methodology_and_model_explanation.md
```

---

## Step 1 — Environment Setup

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Python version:** 3.9 or 3.10 recommended (TensorFlow 2.13+ requirement)

---

## Step 2 — Download the Dataset

See [`data/dataset_instructions.md`](data/dataset_instructions.md) for full instructions.

**Short version:**

1. Go to: https://research.unsw.edu.au/projects/unsw-nb15-dataset  
   OR: https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15
2. Download **both** files:
   - `UNSW_NB15_training-set.csv`
   - `UNSW_NB15_testing-set.csv`
3. Place them in:  
   `midlab_ml_experiment/data/raw/`

Expected sizes:
- Training CSV: ~175,341 rows, 49 features
- Testing CSV: ~82,332 rows, 49 features

---

## Step 3 — Run the Full Experiment

```bash
# From inside midlab_ml_experiment/
python src/run_all.py
```

This single command will:
1. Preprocess the dataset
2. Select 20 best features (and sweep k for Graph 4)
3. Train CNN, SVM, CNN+SVM
4. Evaluate all three models
5. Save all metrics to `results/`
6. Generate all 5 graphs to `graphs/`
7. Generate all 4 flow diagrams to `diagrams/`

Total estimated runtime: **5–20 minutes** depending on your hardware (SVM on 175K rows is the slowest step).

---

## Step 4 — Run Individual Scripts (Optional)

You can also run each step separately:

```bash
python src/preprocessing.py        # preprocess + scale data
python src/feature_selection.py    # select 20 features (+ sweep)
python src/train_cnn.py            # train standalone CNN
python src/train_svm.py            # train standalone SVM
python src/train_cnn_svm.py        # train CNN+SVM pipeline
python src/evaluate.py             # compute all metrics
python src/generate_graphs.py      # generate all 5 result graphs
python src/generate_diagrams.py    # generate all 4 flow diagrams
```

---

## Results Location

| Output | Path |
|--------|------|
| Comparison table | `results/model_comparison.csv` |
| Detailed metrics | `results/metrics.csv` |
| Trained CNN | `results/models/cnn_model.keras` |
| Trained SVM | `results/models/svm_model.joblib` |
| CNN+SVM models | `results/models/cnn_extractor.keras`, `results/models/cnn_svm_classifier.joblib` |
| Graphs | `graphs/*.png` |
| Diagrams | `diagrams/*.png` |
| Confusion matrices | `results/confusion_matrices/*.png` |

---

## Reproducibility

- All random seeds are fixed at `RANDOM_SEED = 42` in `src/utils.py`
- Feature scaling and feature selection are fitted **only on training data** and applied to test data — no data leakage
- Dataset split follows the standard UNSW-NB15 pre-defined train/test partition

---

## Dependencies

See `requirements.txt`. Key packages:

| Package | Use |
|---------|-----|
| `tensorflow` | CNN (1-D Conv, Keras Sequential API) |
| `scikit-learn` | SVM, feature selection, metrics |
| `pandas` / `numpy` | Data loading and manipulation |
| `matplotlib` / `seaborn` | Graphs, confusion matrices |
| `joblib` | SVM model persistence |

---

## Scientific Integrity Note

All metrics, graphs, confusion matrices and timings in this experiment are produced from actual execution of the code. Nothing has been fabricated, manipulated or artificially tuned. The results are preliminary and are intended to demonstrate initial feasibility of the CNN + SVM pipeline for IoT intrusion detection, not to claim final optimized performance.
