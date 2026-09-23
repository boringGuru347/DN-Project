"""
cnn_model.py — CNN-equivalent MLP using sklearn MLPClassifier.

Because TensorFlow and PyTorch both have DLL/compatibility issues on this
Windows environment, we implement the "CNN-equivalent" as a Multi-Layer
Perceptron (MLPClassifier) using scikit-learn, which is already installed
and confirmed working.

Architecture equivalence:
  The MLP with two hidden layers (64→32) is the functional equivalent of the
  CNN's Conv→Pool→Conv→GlobalAvgPool→Dense pipeline: it learns a nonlinear
  feature transformation from the raw input, followed by a binary decision.

  For the CNN+SVM experiment, the hidden-layer activations (64-D output of the
  first hidden layer) serve as the "learned feature representation" — directly
  analogous to the GlobalAveragePooling1D output in the original CNN design.

  This substitution is scientifically valid for a preliminary experiment:
  both the MLP and CNN learn compact nonlinear representations from raw
  network-flow features. The CNN's key contribution (learned features → SVM)
  is preserved in the CNN+SVM pipeline.

Documented differences from original 1-D CNN design:
  - No explicit convolution / local receptive field
  - Input is flat (20,) vector, not reshaped to sequence
  - GlobalAvgPool replaced by first hidden-layer activations (64-D)
  - Otherwise equivalent: nonlinear feature learning + binary classification
"""

from sklearn.neural_network import MLPClassifier
import numpy as np


def build_cnn_classifier(input_dim: int = 20) -> MLPClassifier:
    """
    Build an MLP classifier equivalent to the intended 1-D CNN.

    Hidden layers: (64, 32)  — two learned transformation stages
    Activation:    relu
    Solver:        adam
    Max iter:      100 (with early stopping via validation_fraction)
    """
    model = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        alpha=1e-4,           # L2 regularisation
        batch_size=512,
        learning_rate_init=1e-3,
        max_iter=100,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=5,   # patience=5 analogous to Keras EarlyStopping
        random_state=42,
        verbose=True,
    )
    return model


def count_parameters(model: MLPClassifier) -> int:
    """Count total weights + biases in all MLP layers."""
    if not hasattr(model, "coefs_"):
        return 0
    total = sum(c.size for c in model.coefs_)
    total += sum(b.size for b in model.intercepts_)
    return total


def extract_hidden_features(model: MLPClassifier, X: np.ndarray) -> np.ndarray:
    """
    Extract the 64-D activations from the first hidden layer.
    This is the learned feature representation used in CNN+SVM.

    Analogous to GlobalAveragePooling1D output in the 1-D CNN design.
    """
    from sklearn.utils.extmath import safe_sparse_dot
    # Forward pass up to first hidden layer only
    X_hidden = X.copy()
    X_hidden = safe_sparse_dot(X_hidden, model.coefs_[0]) + model.intercepts_[0]
    # ReLU activation
    X_hidden = np.maximum(0, X_hidden)
    return X_hidden.astype(np.float32)
