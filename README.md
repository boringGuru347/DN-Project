# Lightweight Edge-Based Intrusion Detection for IoT Networks

**Data Networks Course Project — Mid-Lab Review**  
*Department of Electronics and Communication Engineering, National Institute of Technology Warangal*

---

## 👥 Team Members

| Name | Roll Number | Role |
| :--- | :--- | :--- |
| **Chhatrapal Bhuarya** | `24ECB0B14` | Network / Data Preprocessing Pipeline |
| **Dasari Sai Kishan** | `24ECB0B15` | Reference Paper Reproduction & Baseline |
| **Saarth Yawale** | `24ECB0B49` | Proposed Lightweight Model & Architecture |
| **Sudhanshu Bhagat** | `24ECB0B57` | Evaluation, Latency Profiling & Benchmarking |

---

## 📌 Project Overview

IoT networks feature pervasive, resource-constrained endpoints (sensors, actuators, smart meters), making it impractical and unsafe to route all telemetry and raw traffic to centralized clouds for security inspection. Recent IEEE studies propose deep hybrid models (e.g., CNN-LSTM with Attention mechanisms) for intrusion detection. While accurate, these architectures incur heavy memory footprints, high FLOPs, and recurrent unrolling latencies unviable for low-power edge nodes.

Our project addresses these limitations by developing a **lightweight hybrid classification pipeline**:
1. **Feature Reduction:** Reducing high-dimensional network flow features (>50% reduction via ANOVA F-Score selection).
2. **Deep Feature Learning:** Using a lightweight neural network (CNN/MLP) solely for nonlinear representation learning.
3. **Convex Decision Separation:** Applying Support Vector Machines (SVM) on learned representations for fast, maximum-margin attack classification.

---

## 📚 Main Reference Papers

1. **P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni, and S. Rajalakshmi**, *"A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks,"* **IEEE Access**, 2025.
2. *"Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems,"* **IEEE ICERECT**, 2025.

---

## 🔍 Identified Research Gaps

1. **High Computational Complexity:** Deep neural models with recurrent/attention layers exceed the power and compute limits of edge IoT gateways.
2. **Excessive Feature Dimensionality:** Standard datasets supply 40–80 attributes, introducing noise, buffer overhead, and transmission delays.
3. **Accuracy vs. Speed Trade-Off:** Achieving 99% accuracy offline does not guarantee meeting real-time per-packet processing deadlines.
4. **Underutilized Hybrid Learning:** Scope exists to decouple feature extraction (deep learning) from decision boundary placement (classical convex classifiers).
5. **Practical Edge Readiness:** Need for sub-100 KB footprint models with sub-millisecond per-sample inference.

---

## 📊 Preliminary Experimental Results (UNSW-NB15)

Evaluated on **175,341 test flows** using **20 selected features** (reduced from 42):

| Model | Accuracy | Precision | Recall | F1-Score | FPR | Training Time | Inference Time (175k flows) | Per-Sample Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CNN** | **87.60%** | **98.40%** | 83.14% | **90.13%** | **2.88%** | 11.01 s | **0.0596 s** | **0.34 μs / sample** |
| **SVM** | **88.21%** | 97.51% | **84.84%** | **90.73%** | 4.62% | 66.55 s | 163.14 s | 0.93 ms / sample |
| **CNN + SVM** | **88.16%** | **97.99%** | 84.34% | **90.65%** | **3.69%** | 61.36 s | 151.73 s | 0.87 ms / sample |

### Key Observations
- **Low False Alarm Rate:** CNN achieves **2.88% FPR** and CNN+SVM achieves **3.69% FPR** with **>97.9% precision**, preventing alert flooding in IoT networks.
- **Wire-Speed Filtering:** CNN inference completes in **0.0596s for 175,341 flows (~0.34 μs/sample)**, proving high-throughput edge feasibility.
- **Representation Quality:** CNN+SVM matches standalone SVM accuracy (**88.16% vs 88.21%**) using learned dense features, validating the hybrid pipeline concept.

---

## 📂 Repository Structure

```
├── Data_Networks_MidLab_Presentation.pptx   # Official 5-slide Mid-Lab Review presentation
├── README.md                                # Top-level project documentation
├── .gitignore
└── midlab_ml_experiment/                    # Experimental pipeline & source code
    ├── README.md                            # Detailed reproduction instructions
    ├── requirements.txt                     # Python dependencies
    ├── generate_presentation.py             # Script generating PPTX slides
    ├── data/
    │   ├── dataset_instructions.md          # UNSW-NB15 dataset details & citation
    │   ├── raw/                             # Dataset CSV files
    │   └── processed/                       # Scaled & feature-selected arrays (.npy)
    ├── src/
    │   ├── preprocessing.py                 # Cleaning, encoding, scaling
    │   ├── feature_selection.py             # ANOVA F-score selection & sweep
    │   ├── cnn_model.py                     # Deep feature extractor architecture
    │   ├── svm_model.py                     # SVM model definition
    │   ├── cnn_svm_model.py                 # CNN+SVM hybrid pipeline
    │   ├── train_cnn.py                     # Standalone CNN training
    │   ├── train_svm.py                     # Standalone SVM training
    │   ├── train_cnn_svm.py                 # Hybrid CNN+SVM training
    │   ├── evaluate.py                      # Metrics, confusion matrices, latency
    │   ├── generate_graphs.py               # Generates all result plots
    │   ├── generate_diagrams.py             # Generates all system flow diagrams
    │   ├── run_all.py                       # Master execution script
    │   └── utils.py                         # Shared paths, constants, seed=42
    ├── results/
    │   ├── model_comparison.csv             # Summary metrics table
    │   ├── metrics.csv                      # Detailed experimental records
    │   ├── feature_sweep.json               # Accuracy/F1 across k=10..35
    │   ├── confusion_matrices/              # Individual confusion matrix PNGs
    │   └── models/                          # Serialized trained model weights (.joblib)
    ├── graphs/                              # Generated high-resolution plots
    ├── diagrams/                            # Generated system flow diagrams
    └── theory/
        └── methodology_and_model_explanation.md  # Comprehensive technical documentation
```

---

## 🚀 Reproduction & Setup

```bash
# Clone the repository
git clone https://github.com/boringGuru347/DN-Project.git
cd DN-Project/midlab_ml_experiment

# Install dependencies
pip install -r requirements.txt

# Run the complete experimental pipeline end-to-end
python src/run_all.py

# Generate the PowerPoint presentation
python generate_presentation.py
```
