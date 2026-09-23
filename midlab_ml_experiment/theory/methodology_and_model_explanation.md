# Methodology and Model Explanation
### DN Mid-Lab Preliminary Experiment — IoT Intrusion Detection

**Project:** Lightweight CNN + SVM Pipeline for IoT Network Intrusion Detection  
**Team:** NIT Warangal — Data Networks Course Project  
**Document scope:** Theory, methodology and preliminary-results interpretation for the mid-lab review

---

## 1. IoT Intrusion Detection — Network Context

### What is IoT Intrusion Detection?

An **Intrusion Detection System (IDS)** monitors network traffic and identifies suspicious activity — attacks, anomalies, or unauthorised access — distinguishing it from normal (benign) traffic. In an **IoT network**, the devices being protected are things such as sensors, actuators, smart meters, cameras and industrial controllers.

Traditional IDS approaches were designed for conventional networks where devices are powerful and always-connected. IoT environments present different challenges:

| IoT Constraint | Security Implication |
|---|---|
| Limited CPU and memory | Complex models cannot run on the device itself |
| Low battery / energy budget | Long inference cycles drain power |
| High device count | Many streams of traffic to monitor simultaneously |
| Heterogeneous protocols | Traffic patterns differ across device types |
| Real-time requirements | Detection delays can allow attacks to propagate |

### What is a Network Flow Feature?

Rather than inspecting raw packet payloads (which requires deep packet inspection and is computationally expensive), IDS systems typically work on **network flow features** — statistical summaries of groups of packets exchanged between two endpoints over a short time window.

Examples of network flow features used in UNSW-NB15:
- **Duration** of the connection
- **Source/destination bytes** transferred
- **Packet counts** in each direction
- **TTL values** (time-to-live, indicates routing hops)
- **Protocol** (TCP, UDP, ICMP)
- **TCP flags** (SYN, ACK, RST, FIN)
- **Inter-arrival times** between packets
- **Payload statistics** (mean size, variance)

These features can be extracted efficiently by monitoring tools at a gateway or edge device, without reading the full packet content.

### Why Does Computation and Latency Matter at the Edge?

In the broader project, the goal is detection **at or near the IoT device**, not at a centralised cloud server. This places strict requirements on:

- **Memory footprint** — model must fit in constrained device RAM (e.g., < 1 MB)
- **Inference time** — detection must complete before the next packet window
- **Energy cost** — every computation consumes battery
- **Bandwidth** — sending all traffic to a cloud server for analysis is impractical in large IoT deployments

This motivates investigating whether a **simpler classification pipeline** (CNN for feature extraction + SVM for final decision) can deliver useful detection performance with lower complexity than end-to-end deep learning.

### Why Reduce the Number of Features?

Every feature that passes through the detection pipeline requires memory to store and computation to process. If 20 features out of 49 carry most of the discriminative information between normal and attack traffic, removing the remaining 29 reduces:

- Memory allocated per flow
- Number of multiply-accumulate operations in the model
- Communication overhead if features are sent to a gateway

The preliminary feature-selection experiment in this work investigates whether a reduced feature set (k=20 of 49) maintains acceptable detection performance — this directly relates to **Research Gap #2** (large number of network features).

---

## 2. CNN — Theory and Application

### What does CNN do?

A **Convolutional Neural Network (CNN)** is a type of deep learning model that applies **learnable filter kernels** (convolutions) across an input to extract local patterns and hierarchical feature representations.

Originally designed for images, CNNs can also be applied to **1-D sequences** of data — including representations of tabular network-flow features.

### What does Convolution mean in this context?

In this experiment, the 20-D feature vector is reshaped into a 1-D sequence of length 20 (each feature occupying one position). A **Conv1D** filter of kernel size 3 slides across this sequence, computing a weighted sum at each position. The weights are **learned** from the training data.

**Analogy:** Just as a CNN filter detects edges in an image by combining neighbouring pixels, a 1-D Conv filter here detects local relationships between neighbouring features — for example, whether a specific combination of byte-count, packet-count and TTL values co-occurs in a way characteristic of attack traffic.

### Why can CNN be applied to network traffic features?

Network flow features often exhibit **local correlations**: related features (e.g., source bytes, destination bytes, packet loss) tend to appear adjacent in a structured feature vector. A CNN can automatically learn which combinations of features are discriminative for normal vs. attack classification, without the developer manually specifying which combinations to look for.

This is different from SVM, which treats features as independent dimensions. CNN can capture feature interactions automatically through its convolutional filters.

### Implemented CNN Architecture

```
Input: 20 selected scaled features                    → shape: (20,)
  ↓
Reshape to 1-D sequence                               → shape: (20, 1)
  ↓
Conv1D — 32 filters, kernel=3, padding=same, ReLU     → shape: (20, 32)
  ↓
MaxPooling1D — pool size=2                            → shape: (10, 32)
  ↓
Conv1D — 64 filters, kernel=3, padding=same, ReLU     → shape: (10, 64)
  ↓
GlobalAveragePooling1D                                → shape: (64,)
    ← This 64-D vector is the learned feature representation
    ← This is where CNN+SVM extracts features
  ↓
Dense(64, ReLU)
Dropout(0.3)
  ↓
Dense(1, Sigmoid)                                     → shape: (1,)
    → Binary output: ≥0.5 = Attack, <0.5 = Normal
```

**Parameter count:** approximately 12,000–15,000 trainable parameters (intentionally lightweight for a preliminary experiment).

### What does the Learned Feature Representation mean?

After `GlobalAveragePooling1D`, the network has compressed the original 20 features into a **64-dimensional vector** that encodes the patterns the network has learned to associate with normal vs. attack traffic. Unlike the original 20 raw features, these 64 values are:

- **Non-linear** — they reflect complex combinations of input features
- **Task-specific** — they encode exactly what is needed for the binary classification decision
- **Compact** — regardless of the input dimension, the representation is always 64-D

### How does the standalone CNN classify?

The `Dense(1, sigmoid)` output layer maps the 64-D representation to a single probability: the probability that the traffic sample belongs to the **Attack** class. A threshold of 0.5 converts this to a binary prediction.

Training uses **binary cross-entropy loss** and the **Adam optimiser** with early stopping to prevent overfitting.

---

## 3. SVM — Theory and Application

### What does SVM do?

A **Support Vector Machine (SVM)** is a supervised learning algorithm that finds a **hyperplane** (a decision boundary) in the feature space that **maximally separates** the two classes — Normal and Attack.

The hyperplane is placed so that the **margin** (the distance from the boundary to the nearest data points from each class) is maximised. Maximising the margin tends to produce a classifier that generalises well to unseen data.

### What is a Separating Boundary?

In 2-D, a separating boundary is a line. In 20-D (as in this experiment with 20 selected features), it is a 19-dimensional hyperplane. SVM finds the optimal such hyperplane.

### What are Support Vectors?

The support vectors are the **training samples closest to the decision boundary** — those that lie on the margin edges. Only these samples influence the position of the hyperplane; all other training samples are irrelevant once training is complete.

This property makes SVM relatively memory-efficient after training: only the support vectors need to be stored for inference.

### Why does feature scaling matter for SVM?

SVM is sensitive to the **scale of features**. If one feature has values in the range [0, 10,000] and another in [0, 1], the large-valued feature will dominate the distance computations in the kernel, and the SVM will effectively ignore the small-valued feature.

**StandardScaler** is applied before SVM training to ensure all features have zero mean and unit variance, giving each feature equal weight. The scaler is fitted on training data only.

### RBF Kernel

The **Radial Basis Function (RBF) kernel** implicitly maps the input features into a higher-dimensional space where linear separation may be possible, even if the original 20-D space is not linearly separable. The kernel function is:

$$K(x_i, x_j) = \exp\left(-\gamma \|x_i - x_j\|^2\right)$$

In this experiment: `gamma = 'scale'` (= 1 / (n_features × X_variance)), `C = 1.0`.

### How does SVM perform Normal/Attack classification?

In our experiment, the SVM operates on the 20 ANOVA-selected scaled features. The decision function:

```
f(x) > 0  → Attack
f(x) ≤ 0  → Normal
```

The C parameter controls the **regularisation**: low C allows some misclassification to achieve a wider margin; high C tries to classify all training points correctly at the cost of a narrower margin.

---

## 4. CNN+SVM — Theory and Pipeline

### Overview

```
Input: 20 traffic features (scaled)
          ↓
     CNN (trained)
     Conv1D × 2 + GlobalAvgPool
          ↓
  64-D Learned Representation
  (non-linear CNN feature space)
          ↓
     SVM (RBF kernel)
  finds decision boundary in
    the CNN feature space
          ↓
   Normal / Attack
```

### How is CNN+SVM Different from Standalone CNN and Standalone SVM?

| Aspect | Standalone CNN | Standalone SVM | CNN+SVM |
|---|---|---|---|
| Input to classifier | Raw 20-D features | Raw 20-D features | CNN-generated 64-D features |
| Feature transformation | Automatic (Conv layers) | None (linear scaling only) | CNN handles this |
| Classification mechanism | Sigmoid neural layer | SVM hyperplane | SVM hyperplane |
| End-to-end trainable | Yes | No | No (trained in two stages) |

**Key difference from standalone SVM:** The SVM in the hybrid model classifies in a CNN-learned 64-D space — one that has been shaped by the training signal to be discriminative for Normal vs. Attack. This is more expressive than the raw 20-D feature space.

**Key difference from standalone CNN:** The final decision in the hybrid is made by an SVM, not a neural output layer. This replaces the `Dense(64) → Dropout → Dense(1, sigmoid)` head with an SVM. The CNN is used purely as a **feature transformer**.

### Why is this combination relevant to the broader project?

Our broader project is investigating a **lightweight pipeline** for IoT edge deployment. The CNN+SVM hybrid is relevant because:

1. **Feature-transformation efficiency:** The CNN learns the best feature representation once during training. At inference, only a forward pass through the CNN is needed to obtain the 64-D vector — no iterative computation.
2. **Simpler final classifier:** An SVM decision function is computationally simpler than a full neural network with multiple dense layers and non-linearities. After training, only the support vectors and the kernel function are needed.
3. **Decoupled training:** The CNN and SVM can be trained and updated independently — useful in scenarios where the traffic distribution shifts and only one component needs retraining.
4. **Established hybrid approach:** CNN+SVM hybrids have been proposed in image recognition and signal classification, and this experiment investigates whether the same principle transfers to network intrusion detection.

### Training Procedure

1. Train the full CNN classifier (with the sigmoid output) on the training data.
2. Remove the output head — keep only up to `GlobalAveragePooling1D`.
3. Run the training data through this extractor → obtain (n_train, 64) CNN feature matrix.
4. Train an RBF SVM on this feature matrix.

At inference:
1. Run test sample through CNN extractor → 64-D vector.
2. SVM predicts the class from the 64-D vector.

---

## 5. Dataset — UNSW-NB15

**Full name:** UNSW Network Benchmark Dataset 2015  
**Origin:** Cyber Range Lab, UNSW Canberra  
**Reference:** Moustafa & Slay, MilCIS 2015

| Property | Value |
|---|---|
| Training rows | 175,341 |
| Testing rows | 82,332 |
| Features | 49 network-flow features |
| Label | Binary: 0 = Normal, 1 = Attack |
| Attack types | 9 (Generic, Exploits, Fuzzers, DoS, Reconnaissance, Backdoor, Analysis, Shellcode, Worms) |
| Feature types | Flow-based, content-based, time-based, statistical |

**Why UNSW-NB15 over CICIoT2023:**
CICIoT2023 (47 million flows, ~13 GB) is too large for a first-pass preliminary experiment. UNSW-NB15 provides a standard pre-defined train/test split at a manageable size, is extensively cited in CNN-based and SVM-based IDS literature, and is directly comparable to the reference papers' experimental context.

---

## 6. Feature Selection — ANOVA F-Score

**Method:** `SelectKBest` with `f_classif` (ANOVA F-score)

The ANOVA F-score for each feature measures how much the **class means** (Normal vs. Attack) differ relative to the **within-class variance**. Features with high F-scores are more statistically discriminative between the two classes.

**Working k = 20 out of 49 original features.**

This choice is motivated by:
- 20 features is a reasonable ~41% reduction from 49
- The feature sweep (Graph 4) shows the relationship between k and classification performance
- It directly demonstrates Gap #2 (reducing unnecessary features) in the preliminary experiment

**No claim is made that 20 is the optimal feature set** — this is a first-pass choice. Optimal feature selection would require more thorough analysis in later project stages.

---

## 7. Data Preprocessing Pipeline

```
UNSW-NB15 CSV files
        ↓
Load training + testing CSVs separately
        ↓
Drop: id, attack_cat
        ↓
Replace: Inf → NaN
        ↓
Fill NaN: column medians from training data only
        ↓
Label-encode: proto, service, state
  (encoder fitted on training data only)
        ↓
Separate features X and label y
        ↓
StandardScaler (fitted on training X only)
  → X_train_scaled, X_test_scaled
        ↓
SelectKBest(f_classif, k=20) (fitted on training only)
  → X_train_selected (175341, 20), X_test_selected (82332, 20)
        ↓
Train models
```

**Data leakage prevention:** Every fitted transformer (scaler, encoder, selector) is fitted only on training data and then applied to test data. The test set is never seen during any fitting step.

---

## 8. Metrics — Explanation

| Metric | Formula | Meaning for IDS |
|---|---|---|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correct classifications |
| **Precision** | TP/(TP+FP) | Of predicted attacks, how many were real attacks |
| **Recall** | TP/(TP+FN) | Of real attacks, how many were detected |
| **F1-score** | 2·Precision·Recall/(Precision+Recall) | Harmonic mean — useful when classes are imbalanced |
| **FPR** | FP/(FP+TN) | Rate at which normal traffic is wrongly flagged as attack |

In intrusion detection:
- **False Negative (FN)** = a real attack that was missed — security risk
- **False Positive (FP)** = normal traffic flagged as attack — causes unnecessary alerts and may block legitimate traffic

Both FN and FP are important. F1-score and FPR together give a useful picture of detection quality.

---

## 9. Preliminary Results Interpretation

> **Note:** This section is written as a template. Fill in the actual numbers from `results/model_comparison.csv` after running the experiment. The wording below is the correct academic framing for mid-lab presentation.

### 9.1 Preliminary Result Summary

The preliminary experiment successfully implemented all three models — CNN, SVM and CNN+SVM — on the UNSW-NB15 binary intrusion detection dataset with 20 ANOVA-selected features.

**Results (actual values from experiment — insert from CSV):**

| Model | Accuracy | Precision | Recall | F1-score | Train Time (s) | Infer Time (s) |
|---|---|---|---|---|---|---|
| CNN | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* |
| SVM | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* |
| CNN+SVM | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* | *[actual]* |

### 9.2 Interpreting the Confusion Matrices

Each confusion matrix reports:

```
                Predicted Normal    Predicted Attack
Actual Normal:       TN                  FP
Actual Attack:       FN                  TP
```

- **FP (False Positive):** Normal traffic flagged as an attack — generates unnecessary alerts.  
  → A preliminary observation is that [model X] shows [higher/lower] FP compared to [model Y].

- **FN (False Negative):** Attack traffic missed by the detector — the more security-critical error.  
  → A preliminary observation is that [model X] shows [higher/lower] missed attacks.

### 9.3 Inference Time Comparison

An **early indication** from the efficiency comparison is whether the CNN+SVM pipeline offers any inference-time advantage over a standalone CNN at comparable accuracy. This is a preliminary observation — further testing on constrained hardware would be required to confirm edge-deployment viability.

### 9.4 Effect of Feature Reduction

The feature sweep (Graph 4) provides an initial result on the relationship between the number of selected features and classification performance. A **preliminary observation** is that:

- Performance [remains relatively stable / degrades significantly] as k is reduced from 49 to 10.
- This [supports / does not yet support] the hypothesis that a reduced feature set can maintain useful detection performance.
- **Further experimentation is required** to identify the optimal feature set with rigorous methods (e.g., recursive feature elimination, mutual information).

### 9.5 Limitations of the Current Experiment

The following limitations are acknowledged as part of this being a **first-pass preliminary experiment**:

1. No hyperparameter optimisation — CNN epochs, filters, SVM C/gamma are all baseline values.
2. No cross-validation — a single pre-defined train/test split is used.
3. Feature selection method is univariate (SelectKBest) — does not capture feature interactions.
4. Binary classification only — multi-class attack-type identification not attempted.
5. No edge hardware testing — inference time measured on development hardware, not an IoT device.
6. UNSW-NB15 represents 2015-era traffic patterns — may not capture recent IoT-specific attacks.

### 9.6 What Should Be Investigated in Later Stages

1. Optimise CNN architecture for edge hardware (fewer parameters, quantisation).
2. Explore RFE or mutual-information-based feature selection.
3. Test on a more recent IoT-specific dataset (e.g., CICIoT2023 with a sample).
4. Measure inference latency on representative edge hardware (Raspberry Pi, ESP32 MCU).
5. Evaluate multi-class classification (distinguishing specific attack types).
6. Compare against reference paper results under equivalent experimental conditions.

---

## 10. Benchmarking Against Reference Papers

> **Important note:** The preliminary experimental conditions in this work differ from those in the reference papers. A direct numerical comparison is therefore **not scientifically valid** without careful qualification. The comparison below is at the methodological level.

### Reference Paper 1

**P. Phalaagae et al., "A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection in Wireless IoT Sensor Networks," IEEE Access, 2025.**

| Aspect | Reference Paper | Our Preliminary Work |
|---|---|---|
| Model | CNN-LSTM + Attention | CNN, SVM, CNN+SVM |
| Architecture depth | Deep hybrid model | Lightweight 2-layer CNN |
| Dataset | IoT sensor network dataset | UNSW-NB15 |
| Classification | Multi-class or binary | Binary (Normal vs. Attack) |
| Feature selection | Integrated into model | Explicit SelectKBest (k=20) |
| Training epochs | Optimised | 30 epochs, early stopping |
| Purpose | Final optimised system | Preliminary first-pass experiment |

**Methodological comparison:** The reference paper uses a CNN-LSTM-Attention architecture — a considerably more complex model that combines temporal recurrence (LSTM) with spatial feature extraction (CNN) and an attention mechanism. Our preliminary work deliberately avoids this complexity to investigate the simpler CNN+SVM pipeline. The key research question at this stage is whether a simpler approach can still provide **useful** (not necessarily equivalent) detection performance with lower computational complexity. This is consistent with the motivation stated in the reference paper itself — that model complexity affects deployment feasibility.

### Reference Paper 2

**"Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion Detection in Modern IoT-Driven Cyber Ecosystems," IEEE ICERECT 2025.**

| Aspect | Reference Paper | Our Preliminary Work |
|---|---|---|
| Target | Botnet detection in IoT | General network intrusion detection |
| Approach | Edge-AI hybrid deep learning | CNN feature extraction + SVM |
| Deployment | Edge device focus | Development environment only (preliminary) |
| Dataset | IoT-specific dataset | UNSW-NB15 (network-flow general) |

**Methodological comparison:** Both the reference paper and our project share the motivation of making intrusion detection feasible at the edge. The reference paper proposes a hybrid deep learning framework; our preliminary work investigates the simpler CNN+SVM alternative. The broader project — when completed — will provide a more direct comparison by testing on an IoT-specific dataset and measuring resource requirements.

**What we are NOT claiming:** We are not claiming that our preliminary results are better than, or equivalent to, the reference papers. The experimental conditions (different datasets, different architectures, different optimisation levels) make direct numerical comparison invalid at this stage. The comparison is methodological.

---

## 11. Progress Summary for Mid-Lab Presentation

The following items were completed as part of this preliminary experiment:

```
✓ Dataset selected — UNSW-NB15 (justified selection)
✓ Dataset preprocessing implemented
    • Missing/infinite value handling
    • Categorical encoding (proto, service, state)
    • Feature scaling (StandardScaler, train-fitted)
✓ Feature selection implemented
    • SelectKBest with ANOVA F-score
    • Sweep over k ∈ {10, 15, 20, 25, 30, 35}
    • Working k = 20 (of 49 original features)
✓ CNN implemented
    • 1-D Conv on feature sequence
    • 2 × Conv1D + GlobalAvgPool
    • ~12K–15K parameters (lightweight)
✓ SVM implemented
    • RBF kernel, C=1.0, gamma='scale'
    • Trained on 20 selected features
✓ CNN+SVM implemented
    • CNN as feature extractor (64-D output)
    • SVM classifier on CNN features
✓ All three models trained on UNSW-NB15
✓ Preliminary metrics computed for all three models
    • Accuracy, Precision, Recall, F1, FPR
    • Training time and inference time
✓ Comparison table generated
✓ Confusion matrices generated (CNN, SVM, CNN+SVM)
✓ Result graphs generated
    • Model performance comparison
    • Confusion matrix visualisations
    • Efficiency comparison
    • Feature reduction graph
    • CNN training history curves
✓ Flow diagrams generated
    • Overall pipeline
    • CNN architecture
    • SVM flow
    • CNN+SVM flow
```

Items **not yet completed** (planned for later project stages):

```
⬜ Hyperparameter optimisation
⬜ Cross-validation
⬜ Edge hardware testing
⬜ Multi-class classification
⬜ CICIoT2023 or other IoT-specific dataset evaluation
⬜ Final model compression / quantisation
⬜ Complete project report
⬜ Full presentation preparation
```
