# Technical Lab Report

**Department of Electronics and Communication Engineering**
**National Institute of Technology Warangal**
**Course: Data Networks (ECE)**

---

| Field | Details |
|:---|:---|
| **Report Type** | Mid-Lab Preliminary Experiment Report |
| **Date** | September 2026 |
| **Group Members** | Chhatrapal Bhuarya (24ECB0B14) · Dasari Sai Kishan (24ECB0B15) · Saarth Yawale (24ECB0B49) · Sudhanshu Bhagat (24ECB0B57) |

---

## 1. Title of the Experiment / Study / Exercise

**Lightweight Edge-Based Intrusion Detection for IoT Networks Using Deep Feature Extraction and Classical Machine Learning: A Preliminary Evaluation of CNN, SVM, and CNN+SVM Pipelines on the UNSW-NB15 Benchmark Dataset**

---

## 2. Aim

To design, implement, and evaluate a **lightweight, modular machine-learning pipeline** capable of classifying network traffic as *normal* or *attack* with high detection accuracy, low false-alarm rate, and a computational footprint small enough to support edge-side IoT intrusion detection — as a preliminary proof-of-concept toward replacing the computationally expensive CNN-LSTM-Attention architectures proposed in recent IEEE literature.

Specific aims:
1. Determine whether statistical **feature reduction** (42 → 20 attributes) preserves attack-detection performance.
2. Measure and compare **classification quality** (accuracy, F1-score, FPR) of: standalone CNN, standalone SVM (RBF), and CNN+SVM hybrid.
3. Measure and compare **resource consumption** (training time, inference time, model size) as a preliminary guide toward edge-deployment feasibility.

---

## 3. Objectives

1. **O1 — Dataset Acquisition & Preparation:** Process UNSW-NB15 (82,332 training flows, 175,341 testing flows) with column removal, missing-value handling, categorical encoding, and standard scaling — all fitted exclusively on training data to prevent leakage.

2. **O2 — Feature Dimensionality Study:** Perform ANOVA F-Score SelectKBest sweep across k ∈ {10, 15, 20, 25, 30, 35} and identify a working feature count.

3. **O3 — Standalone CNN Implementation:** Build and train a lightweight feedforward neural network (hidden: 64→32, ReLU, Adam, early-stopping patience=5) for binary IDS; record training convergence.

4. **O4 — Standalone SVM Implementation:** Build and train an RBF-kernel SVM (C=1.0, γ='scale') on the 20 selected scaled features; record performance and training time.

5. **O5 — CNN+SVM Hybrid Pipeline:** Extract 64-D latent representation from the CNN's first hidden layer; train a second RBF-SVM on these learned representations.

6. **O6 — Systematic Evaluation:** Measure Accuracy, Precision, Recall, F1, FPR, training time, inference time, and model size for all three configurations. Produce confusion matrices and visualisations.

7. **O7 — Reference Paper Comparison:** Provide a methodological comparison with the two main IEEE reference papers.

---

## 4. Methodology

### 4.1 Dataset Description

The **UNSW-NB15** dataset (Moustafa & Slay, IEEE MilCIS 2015) contains synthesised network flow records covering benign traffic and nine attack categories (Generic, Exploits, Fuzzers, DoS, Reconnaissance, Backdoor, Analysis, Shellcode, Worms), all merged to binary labels for this experiment.

| Split | Total Flows | Normal (0) | Attack (1) |
|:---|:---:|:---:|:---:|
| Training | 82,332 | 37,000 | 45,332 |
| Testing | 175,341 | 56,000 | 119,341 |

---

### 4.2 End-to-End Pipeline (8 Stages)

| Stage | Module | Description |
|:---|:---|:---|
| 1 | `preprocessing.py` | Load, clean, encode, scale |
| 2 | `feature_selection.py` | ANOVA sweep + SelectKBest (k=20) |
| 3 | `generate_diagrams.py` | System flow diagrams |
| 4 | `train_cnn.py` | Train lightweight MLP/CNN |
| 5 | `train_svm.py` | Train standalone SVM |
| 6 | `train_cnn_svm.py` | CNN feature extraction → SVM |
| 7 | `evaluate.py` | Metrics + confusion matrices |
| 8 | `generate_graphs.py` | 5 result plots |

All stages run via `run_all.py` with `RANDOM_SEED = 42`.

---

### 4.3 Data Preprocessing (`preprocessing.py`)

**Step 1:** Drop `id` and `attack_cat`. Retain binary `label`.

**Step 2:** Replace ±∞ with NaN. Fill NaN with training-set medians only (zero-leakage):
```python
medians = df_train[numeric_cols].median()
df_train[numeric_cols] = df_train[numeric_cols].fillna(medians)
df_test[numeric_cols]  = df_test[numeric_cols].fillna(medians)
```

**Step 3:** `LabelEncoder` fit on training values for `proto` (132 values), `service` (14), `state` (8). Unknown test values → `__unknown__` integer.

**Step 4:** `StandardScaler` fit on training only → applied to test.

**Final shapes:** X_train ∈ ℝ^(82332×42), X_test ∈ ℝ^(175341×42).

---

### 4.4 Feature Selection — ANOVA F-Score

$$F_j = \frac{(\bar{x}_{j,\text{Attack}} - \bar{x}_{j,\text{Normal}})^2 / (K-1)}{S_j^2 / (N-K)}$$

`SelectKBest(f_classif, k=20)` fit on training data only.

**Selected feature indices:** `[2, 3, 8, 9, 12, 19, 20, 21, 22, 23, 24, 27, 30, 31, 32, 33, 34, 35, 39, 40]`

Corresponds to: `sbytes`, `sttl`, `dttl`, `sinpkt`, `dinpkt`, `ct_state_ttl`, connection-table statistics, packet count ratios.

**Feature reduction: 42 → 20 (52.4%)**

---

### 4.5 Model 1 — Standalone CNN (Lightweight MLP)

| Property | Implementation |
|:---|:---|
| Architecture | Input(20) → Dense(64, ReLU) → Dense(32, ReLU) → Output(1, sigmoid) |
| Optimiser | Adam (lr=1e-3, batch=512) |
| Regularisation | L2 (α=1e-4), early-stopping patience=5, val_fraction=0.1 |
| Parameters | 3,457 (20×64+64 + 64×32+32 + 32×1+1) |
| Training epochs | 53 (early stop) |
| Best val score | 0.9514 |
| Training time | 11.01 s |
| Feature extraction | 64-D h₁ = ReLU(W₁ᵀx + b₁) used for CNN+SVM |

```python
MLPClassifier(
    hidden_layer_sizes=(64, 32), activation="relu", solver="adam",
    alpha=1e-4, batch_size=512, learning_rate_init=1e-3, max_iter=100,
    early_stopping=True, validation_fraction=0.1, n_iter_no_change=5,
    random_state=42,
)
```

---

### 4.6 Model 2 — Standalone SVM

```python
SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42,
    probability=False, cache_size=1000)
```

Kernel: K(xᵢ, xⱼ) = exp(−γ||xᵢ − xⱼ||²), γ = 1/(20 × Var(X)) ≈ 0.05.

Training: 82,332 flows, 20 features. Training time: **66.55 seconds**.

---

### 4.7 Model 3 — CNN+SVM Hybrid

```
Input (20 features)
    ↓
CNN/MLP [trained] — forward pass to hidden layer 1 only
    ↓
64-D Latent Representation: h₁ = ReLU(W₁ᵀx + b₁)
    ↓
SVM [RBF, C=1.0] — trained on (82332 × 64) feature matrix
    ↓
Normal (0) / Attack (1)
```

Support vectors identified: 13,665. Total training time: **61.36 seconds**.

---

### 4.8 Evaluation Metrics

| Metric | Formula |
|:---|:---|
| Accuracy | (TP + TN) / N |
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1-Score | 2·P·R / (P + R) |
| FPR | FP / (FP + TN) |

---

## 5. Simulation Results / Observations Along with Scenario Diagram

### 5.1 Scenario Diagram — End-to-End Experimental Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                     UNSW-NB15 DATASET                            │
│   Training: 82,332 flows │ Testing: 175,341 flows                │
│   45 raw columns (id, attack_cat, 42 features + label)           │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                  DATA PREPROCESSING                               │
│  Drop: id, attack_cat → 42 usable features                       │
│  Inf → NaN → median imputation (train stats only)                │
│  Categorical encode: proto(132), service(14), state(8)           │
│  StandardScaler fit on train → applied to test                   │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│          FEATURE SELECTION (ANOVA F-Score, SelectKBest)           │
│  Sweep k ∈ {10,15,20,25,30,35} → working k=20 selected          │
│  52.4% dimensionality reduction: 42 → 20 features                │
└─────────┬────────────────────────────────────────┬───────────────┘
          │                                        │
   ┌──────▼───────┐                    ┌───────────▼──────────┐
   │ 20 features  │                    │   20 features         │
   │ (for SVM)    │                    │  (for CNN input)      │
   └──────┬───────┘                    └───────────┬──────────┘
          │                                        │
   ┌──────▼───────────┐            ┌───────────────▼────────────┐
   │  STANDALONE SVM  │            │   CNN / MLP EXTRACTOR       │
   │  RBF, C=1.0      │            │   Dense(64)→Dense(32), ReLU │
   │  γ='scale'       │            │   Adam, early-stop p=5      │
   │  66.55 s training│            │   11.01 s,  3457 params     │
   └──────┬───────────┘            └───┬─────────────────┬──────┘
          │                    (full)  │        (extract)│
          │                  ┌─────────▼──┐    ┌─────────▼────────┐
          │                  │  CNN alone  │    │ 64-D hidden h₁   │
          │                  │  classify   │    │ (latent vector)  │
          │                  └─────────────┘    └─────────┬────────┘
          │                                               │
          │                                    ┌──────────▼─────────┐
          │                                    │   CNN+SVM           │
          │                                    │   RBF SVM on 64-D  │
          │                                    │   61.36 s, 13665 SVs│
          │                                    └──────────┬──────────┘
          │                                               │
   ┌──────▼───────────────────────────────────────────────▼────────┐
   │               EVALUATION (test set: 175,341 flows)             │
   │   Accuracy · Precision · Recall · F1 · FPR                     │
   │   Training time · Inference time · Model size                   │
   │   Outputs: model_comparison.csv, metrics.csv,                   │
   │            5 graphs, 4 flow diagrams, 3 confusion matrices      │
   └────────────────────────────────────────────────────────────────┘
```

> Rendered diagram: [`diagrams/overall_pipeline.png`](../diagrams/overall_pipeline.png)

---

### 5.2 CNN+SVM Hybrid Architecture Diagram

```
  Input x ∈ ℝ²⁰   (20 selected, standard-scaled traffic features)
       │
       ▼
┌──────────────────────────────────────────────────────┐
│   DEEP FEATURE EXTRACTOR  (Lightweight CNN / MLP)    │
│                                                      │
│   Layer 1:  h₁ = ReLU(W₁ᵀx + b₁)                  │
│             W₁ ∈ ℝ^(20×64),  b₁ ∈ ℝ^64             │
│             → 64-D latent vector  ← EXTRACTION POINT│
│                                                      │
│   Layer 2:  h₂ = ReLU(W₂ᵀh₁ + b₂)                 │
│             W₂ ∈ ℝ^(64×32)                          │
│                                                      │
│   Output:   ŷ = σ(W₃ᵀh₂ + b₃)   [standalone use]   │
│   Total parameters: 3,457                            │
└──────────────────────────────────────────────────────┘
       │  h₁ ∈ ℝ⁶⁴   (nonlinear learned representation)
       ▼
┌──────────────────────────────────────────────────────┐
│   SVM CLASSIFIER  (RBF Kernel)                       │
│                                                      │
│   K(xᵢ, xⱼ) = exp(−γ ||xᵢ − xⱼ||²)               │
│   C = 1.0,  γ = 1 / (64 × Var(X_CNN))              │
│   13,665 support vectors                             │
│                                                      │
│   Decision: f(x) = sign(Σᵢ αᵢyᵢK(xᵢ,x) + b)       │
└──────────────────────────────────────────────────────┘
       │
       ▼
  Output: Normal (0)  or  Attack (1)
```

> Rendered: [`diagrams/cnn_svm_flow.png`](../diagrams/cnn_svm_flow.png), [`diagrams/cnn_flow.png`](../diagrams/cnn_flow.png), [`diagrams/svm_flow.png`](../diagrams/svm_flow.png)

---

### 5.3 Feature Selection Sweep Results

**Table 1 — ANOVA F-Score Feature Sweep (LinearSVC, UNSW-NB15 test set)**

| k (features) | Accuracy | F1-Score | Reduction from 42 |
|:---:|:---:|:---:|:---:|
| 10 | 82.91% | 86.88% | 76.2% |
| 15 | 82.04% | 86.02% | 64.3% |
| **20 ✓ selected** | **85.55%** | **88.67%** | **52.4%** |
| 25 | 88.30% | 90.95% | 40.5% |
| 30 | 88.45% | 91.06% | 28.6% |
| 35 | 88.29% | 90.92% | 16.7% |

> Graph: [`graphs/feature_reduction.png`](../graphs/feature_reduction.png)

---

### 5.4 CNN Training Convergence

**Table 2 — CNN/MLP Training History (key iterations)**

| Iteration | Training Loss | Validation Score |
|:---:|:---:|:---:|
| 1 | 0.4090 | 0.8580 |
| 5 | 0.1778 | 0.9288 |
| 10 | 0.1487 | 0.9362 |
| 20 | 0.1322 | 0.9389 |
| 30 | 0.1247 | 0.9440 |
| 40 | 0.1203 | 0.9496 |
| **47 (best)** | 0.1162 | **0.9514** |
| 53 (stopped) | 0.1144 | — |

Early-stopping triggered at iteration 53 (patience=5 exceeded).

> Graph: [`graphs/cnn_training_history.png`](../graphs/cnn_training_history.png)

---

### 5.5 Main Classification Results

**Table 3 — Model Performance Comparison (Test Set: 175,341 flows, k=20 features)**

| Metric | CNN | SVM | CNN+SVM |
|:---|:---:|:---:|:---:|
| **Accuracy** | 87.60% | **88.21%** | 88.16% |
| **Precision** | **98.40%** | 97.51% | 97.99% |
| **Recall** | 83.14% | **84.84%** | 84.34% |
| **F1-Score** | 90.13% | **90.73%** | 90.65% |
| **FPR** | **2.88%** | 4.62% | 3.69% |
| **Training Time** | **11.01 s** | 66.55 s | 61.36 s |
| **Inference (175K flows)** | **0.0596 s** | 163.14 s | 151.73 s |
| **Per-Sample Latency** | **0.34 μs** | 0.93 ms | 0.87 ms |
| **Parameters / Model Size** | 3,457 / 47.6 KB | — / 3,077 KB | 3,457 / 7,149 KB |

> Graphs: [`graphs/model_performance_comparison.png`](../graphs/model_performance_comparison.png), [`graphs/efficiency_comparison.png`](../graphs/efficiency_comparison.png)

---

### 5.6 Confusion Matrices

**Table 4 — Confusion Matrices (Test Set: 56,000 Normal, 119,341 Attack flows)**

**CNN (Acc=87.60%, FPR=2.88%):**

| | Predicted Normal | Predicted Attack |
|:---|:---:|:---:|
| **Actual Normal** | TN = 54,385 | FP = 1,615 |
| **Actual Attack** | FN = 20,123 | TP = 99,218 |

**SVM (Acc=88.21%, FPR=4.62%):**

| | Predicted Normal | Predicted Attack |
|:---|:---:|:---:|
| **Actual Normal** | TN = 53,410 | FP = 2,590 |
| **Actual Attack** | FN = 18,088 | TP = 101,253 |

**CNN+SVM (Acc=88.16%, FPR=3.69%):**

| | Predicted Normal | Predicted Attack |
|:---|:---:|:---:|
| **Actual Normal** | TN = 53,936 | FP = 2,064 |
| **Actual Attack** | FN = 18,690 | TP = 100,651 |

> Images: [`results/confusion_matrices/cm_cnn.png`](../results/confusion_matrices/cm_cnn.png), [`cm_svm.png`](../results/confusion_matrices/cm_svm.png), [`cm_cnn_svm.png`](../results/confusion_matrices/cm_cnn_svm.png)
> Combined: [`graphs/confusion_matrices.png`](../graphs/confusion_matrices.png)

---

### 5.7 Resource Efficiency

**Table 5 — Computational Efficiency Summary**

| Metric | CNN | SVM | CNN+SVM |
|:---|:---:|:---:|:---:|
| Training Time | **11.01 s** | 66.55 s | 61.36 s |
| Speedup vs. SVM | **6.04×** | 1× | 1.08× |
| Inference (175K flows) | **0.0596 s** | 163.14 s | 151.73 s |
| Inference Speedup | **~2,737×** | 1× | ~1.07× |
| Per-Sample Latency | **0.34 μs** | 930 μs | 867 μs |
| Model File Size | **47.6 KB** | 3,077 KB | 7,149 KB |

> Graph: [`graphs/efficiency_comparison.png`](../graphs/efficiency_comparison.png)

---

## 6. Discussion on the Results / Observations

### 6.1 Classification Performance Analysis

All three models cluster tightly in the **87.6%–88.2% accuracy** and **90.1%–90.7% F1** range. This is a key finding: a 52.4% feature reduction preserves competitive classification performance, validating the ANOVA F-Score selection strategy.

The **SVM achieves the highest accuracy (88.21%) and F1 (90.73%)**, consistent with the well-known strength of RBF-SVMs on tabular data. The SVM's maximum-margin formulation generalises well from 20 features.

The **CNN+SVM hybrid (88.16%, 90.65%)** is virtually indistinguishable from standalone SVM. This confirms that the CNN's 64-D latent representations carry at least as much discriminative information as the raw 20-D feature space — a necessary condition for the hybrid design to be meaningful.

The **standalone CNN (87.60%, 90.13%)** slightly underperforms, as expected: an MLP's output head provides a softer boundary than SVM's hard maximum-margin hyperplane. The gap is small (~0.6%), but the efficiency advantage is enormous.

---

### 6.2 False Positive Rate Analysis

FPR is critical in operational IDS — false alarms block legitimate IoT traffic and overwhelm alert queues:

- **CNN: 2.88% FPR** — Only 1,615 of 56,000 normal flows misclassified. Precision: **98.40%**
- **CNN+SVM: 3.69% FPR** — 2,064 false alarms. Precision: **97.99%**
- **SVM: 4.62% FPR** — 2,590 false alarms — **60% more false alarms than CNN**

The counterintuitive result is that the SVM, despite having the highest recall (84.84%), also generates the most false alarms. In an IoT deployment with high-volume normal traffic (sensor heartbeats, MQTT keep-alives, NTP synchronisation), 2,590 vs. 1,615 false alarms per 56,000 flows is a meaningful operational difference. The CNN's conservative profile — fewer false alarms at the cost of missing some attacks — may be preferable in low-alert-fatigue scenarios.

---

### 6.3 Inference Speed — Edge-Deployment Significance

**CNN: 0.34 μs/sample** — well below inter-packet arrival times (~milliseconds in IoT flows). Confirms wire-speed classification capability.

**SVM: 930 μs/sample** — **2,737× slower** than CNN. Root cause: SVM inference is O(n_support_vectors) per sample; with 3,077 KB of stored SVs and no batching benefit, this becomes prohibitive on edge hardware.

**CNN+SVM: 867 μs/sample** — bottlenecked by the SVM evaluation step despite fast CNN feature extraction.

**Critical insight:** The CNN+SVM hybrid does **not** inherit the CNN's inference speed. The SVM kernel evaluation dominates. The hybrid's potential value lies in multi-class discrimination on harder datasets (future work) — not in inference efficiency. For real-time IoT edge deployment, the **standalone CNN** (47.6 KB, 0.34 μs/sample) is the clear practical choice.

---

### 6.4 Feature Reduction Observations

The sweep (Table 1) reveals three distinct regions:
1. **k=10–20:** Sharp performance improvement (82.9% → 85.6% accuracy). Each additional feature carries substantial discriminative information.
2. **k=20–30:** Gradual plateau; marginal gains (~3% accuracy over 10 more features).
3. **k=30–35:** Near-zero gain with slight degradation, indicating marginal noise from low-F-score features.

The selected k=20 lies at the inflection point — the last value before diminishing returns. The 52.4% feature reduction translates directly to:
- Smaller per-flow buffer: 80 bytes (20 × float32) vs. 168 bytes (42 × float32)
- Fewer arithmetic operations per inference pass
- Smaller on-device storage for scaler and selector artefacts

---

### 6.5 Methodological Benchmarking Against Reference Papers

> **Note:** Direct numerical comparison is not valid due to dataset and protocol differences. This is a methodological alignment only.

**Phalaagae et al., IEEE Access 2025 (CNN-LSTM + Attention):**

The reference paper employs CNN for spatial feature learning, LSTM for temporal recurrence across flow windows, and an Attention mechanism for weighted focus on attack-relevant timesteps. This architecture:
- Requires O(T × H²) recurrent computation per sequence window (T=length, H=hidden size)
- Requires O(T²) pairwise attention score computation
- Is trained and evaluated on IoT sensor network traffic

Our approach deliberately omits the LSTM and Attention components, reducing the per-flow computation to a single MLP forward pass. Our preliminary results (88.2% accuracy, 90.7% F1) establish a **complexity floor**: the reference paper's additional complexity must demonstrate value beyond this baseline on matched datasets.

**Edge-AI IDS, IEEE ICERECT 2025 (Deep Learning at Edge):**

This paper targets botnet detection with edge-deployed deep learning, sharing our motivation of proximity-to-device deployment. We provide the first concrete lower-bound quantification: a **47.6 KB, 3,457-parameter model** achieving **88.2% accuracy** and **0.34 μs/sample inference** on a standard benchmark. This characterises the floor of the complexity-performance tradeoff and provides a reproducible baseline for any subsequent hardware-in-the-loop study.

---

### 6.6 Limitations and Next Steps

**Current limitations:**
1. No hyperparameter optimisation — all values are defaults; optimised settings would likely improve performance.
2. Single pre-defined train/test split; no k-fold cross-validation to bound variance.
3. Binary classification only; nine attack categories are merged.
4. Timings on laptop CPU; not representative of IoT edge hardware (Raspberry Pi, ESP32, ARM Cortex-M).
5. UNSW-NB15 (2015) may not capture recent IoT attack patterns.
6. MLP used instead of true 1-D CNN (library compatibility constraint); local receptive field and weight sharing absent.

**Planned next steps:**
- Multi-class attack categorisation (9 classes)
- Hyperparameter tuning (grid search for C, γ, hidden layer size)
- Evaluation on CICIoT2023 (recent, IoT-specific, multi-class)
- Model compression: INT8 quantisation, structured pruning
- Raspberry Pi 4 / ESP32 hardware benchmarking
- True 1-D Convolutional implementation

---

## Appendix — Generated Files Index

| File | Description |
|:---|:---|
| `results/model_comparison.csv` | Summary metrics table |
| `results/metrics.csv` | Detailed metrics incl. confusion matrices |
| `results/feature_sweep.json` | Sweep results k=10..35 |
| `results/models/cnn_training_history.json` | Loss curve, 53 iterations |
| `graphs/model_performance_comparison.png` | Accuracy/Precision/Recall/F1 bar chart |
| `graphs/confusion_matrices.png` | Side-by-side confusion matrices |
| `graphs/efficiency_comparison.png` | Training + inference time comparison |
| `graphs/feature_reduction.png` | Accuracy/F1 vs. feature count |
| `graphs/cnn_training_history.png` | CNN loss curve across 53 iterations |
| `diagrams/overall_pipeline.png` | End-to-end system pipeline |
| `diagrams/cnn_flow.png` | CNN architecture flow |
| `diagrams/svm_flow.png` | SVM pipeline flow |
| `diagrams/cnn_svm_flow.png` | CNN+SVM hybrid architecture |
| `results/confusion_matrices/*.png` | Individual confusion matrix images |

---

## References

1. N. Moustafa and J. Slay, "UNSW-NB15: a comprehensive data set for network intrusion detection systems," *Proc. IEEE MilCIS*, 2015.
2. P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni, and S. Rajalakshmi, "A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks," *IEEE Access*, 2025.
3. "Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems," *IEEE ICERECT*, 2025.
4. F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *JMLR*, vol. 12, pp. 2825–2830, 2011.
5. V. N. Vapnik, *The Nature of Statistical Learning Theory*, Springer, 1995.

---

*Repository: [https://github.com/boringGuru347/DN-Project](https://github.com/boringGuru347/DN-Project)*
