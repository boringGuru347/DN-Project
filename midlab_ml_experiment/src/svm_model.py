"""
svm_model.py — SVM model definition for network intrusion detection.

Configuration:
  Kernel : RBF (Radial Basis Function)
  C      : 1.0   (regularisation — trades off margin width vs. misclassification)
  gamma  : 'scale'  (1 / (n_features * X.var()), avoids manual tuning)

Design rationale:
  - RBF kernel is the standard first-pass kernel for non-linear classification.
  - C=1.0 and gamma='scale' are sensible baselines — no exhaustive search.
  - probability=False for speed (not needed for preliminary binary classification).
  - The SVM operates on the 20 selected/scaled features for the standalone model,
    and on the 64-D CNN feature representation for the CNN+SVM model.
"""

from sklearn.svm import SVC


def build_svm(C: float = 1.0, kernel: str = "rbf", gamma: str = "scale",
              random_state: int = 42) -> SVC:
    """
    Build and return an SVC classifier with RBF kernel.

    Parameters
    ----------
    C : float
        Regularisation parameter. Default 1.0.
    kernel : str
        SVM kernel type. Default 'rbf'.
    gamma : str or float
        Kernel coefficient. Default 'scale'.
    random_state : int
        Random seed for reproducibility. Default 42.

    Returns
    -------
    SVC
        Unfitted scikit-learn SVC instance.
    """
    clf = SVC(
        kernel=kernel,
        C=C,
        gamma=gamma,
        random_state=random_state,
        probability=False,   # set True only if probability estimates are needed
        cache_size=1000,     # MB of cache — speeds up RBF kernel on large datasets
    )
    return clf


if __name__ == "__main__":
    svm = build_svm()
    print("SVM configuration:")
    print(f"  Kernel : {svm.kernel}")
    print(f"  C      : {svm.C}")
    print(f"  gamma  : {svm.gamma}")
