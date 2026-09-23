"""
cnn_svm_model.py — CNN+SVM hybrid using sklearn MLP as feature extractor + SVM.

Pipeline:
  Input (20-D scaled features)
        ↓
  MLP (trained) — forward pass to first hidden layer (64-D ReLU activations)
        ↓
  64-D Learned Feature Representation
        ↓
  SVM (RBF kernel)
        ↓
  Normal / Attack
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cnn_model import extract_hidden_features, build_cnn_classifier
from svm_model import build_svm


def train_cnn_svm(cnn_model, X_train: np.ndarray, y_train: np.ndarray):
    """
    Extract 64-D learned features from the trained MLP's first hidden layer,
    then train an SVM on those features.
    """
    print("  [CNN+SVM] Extracting MLP hidden-layer features from training data...")
    X_train_cnn = extract_hidden_features(cnn_model, X_train)
    print(f"  [CNN+SVM] Feature shape: {X_train_cnn.shape}")

    svm = build_svm()
    print("  [CNN+SVM] Training SVM on learned features...")
    svm.fit(X_train_cnn, y_train)
    return svm


def predict_cnn_svm(cnn_model, svm, X: np.ndarray) -> np.ndarray:
    """Full CNN+SVM inference: MLP feature extraction → SVM prediction."""
    X_cnn = extract_hidden_features(cnn_model, X)
    return svm.predict(X_cnn)
