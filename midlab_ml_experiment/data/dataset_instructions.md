# UNSW-NB15 Dataset — Download Instructions

## Dataset Overview

**Name:** UNSW-NB15  
**Source:** Cyber Range Lab, University of New South Wales (UNSW), Canberra, Australia  
**Academic use:** Freely available for research and academic purposes  
**Reference:** Moustafa, N. and Slay, J. (2015). UNSW-NB15: A Comprehensive Dataset for Network Intrusion Detection Systems. Military Communications and Information Systems Conference (MilCIS).

---

## Why UNSW-NB15?

UNSW-NB15 was selected as the dataset for this preliminary experiment for the following reasons:

1. **Appropriate domain:** Contains labelled network traffic records — both normal and attack traffic — directly relevant to network intrusion detection for IoT and edge environments.
2. **Binary label:** Provides a clean binary label (0 = Normal, 1 = Attack) suitable for CNN and SVM classification.
3. **Manageable size:** Pre-split into ~175K training and ~82K testing rows — practical for a preliminary CNN + SVM experiment on standard hardware.
4. **Standard benchmark:** Extensively used in recent IEEE publications on CNN-based and SVM-based IDS, making methodological comparison meaningful.
5. **Public availability:** Freely downloadable for academic use.
6. **49 network-flow features:** Includes duration, bytes, packet counts, protocol info, statistical flow metrics — standard network-flow feature types used in IoT intrusion detection literature.

---

## Download Instructions

### Option A — Kaggle (Easiest)

1. Go to: https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15
2. Click **Download** (requires a free Kaggle account).
3. Unzip the downloaded archive.
4. Locate these two specific files:
   - `UNSW_NB15_training-set.csv`
   - `UNSW_NB15_testing-set.csv`

### Option B — Official UNSW Source

1. Go to: https://research.unsw.edu.au/projects/unsw-nb15-dataset
2. Navigate to the dataset files section.
3. Download the training and testing CSV files.

---

## File Placement

After downloading, place the two CSV files here:

```
midlab_ml_experiment/
└── data/
    └── raw/
        ├── UNSW_NB15_training-set.csv    ← place here
        └── UNSW_NB15_testing-set.csv     ← place here
```

**The `data/raw/` folder will be created automatically when you first run any script, but you must place the CSV files there manually.**

---

## Expected File Properties

| File | Rows (approx.) | Columns | Size (approx.) |
|------|---------------|---------|----------------|
| `UNSW_NB15_training-set.csv` | 175,341 | 49 features + label + attack_cat | ~40 MB |
| `UNSW_NB15_testing-set.csv`  | 82,332  | 49 features + label + attack_cat | ~20 MB |

---

## Dataset Features

The 49 features cover:

| Category | Examples |
|----------|---------|
| Basic flow | `dur` (duration), `proto`, `service`, `state` |
| Content | `sbytes`, `dbytes`, `sttl`, `dttl` |
| Time | `Sintpkt`, `Dintpkt`, `tcprtt`, `synack`, `ackdat` |
| Statistical | `smean`, `dmean`, `trans_depth` |
| Connection | `spkts`, `dpkts`, `sload`, `dload`, `sloss`, `dloss` |

The **label** column: `0` = Normal, `1` = Attack  
The `attack_cat` column (attack category): dropped for binary classification.

---

## Data Citation

If referencing this dataset in a report or presentation, use:

> N. Moustafa and J. Slay, "UNSW-NB15: A Comprehensive Dataset for Network Intrusion Detection Systems (UNSW-NB15 Network Data Set)," in 2015 Military Communications and Information Systems Conference (MilCIS), Canberra, Australia, 2015, pp. 1–6.
