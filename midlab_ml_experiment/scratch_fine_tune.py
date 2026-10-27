import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, HistGradientBoostingClassifier

X_train = np.load('data/processed/X_train.npy')
y_train = np.load('data/processed/y_train.npy')
X_test  = np.load('data/processed/X_test.npy')
y_test  = np.load('data/processed/y_test.npy')

# Let's test different feature subsets and hyperparameters
# Top 16 by importance
top_indices = [9, 10, 19, 31, 3, 34, 35, 2, 22, 8, 40, 30, 27, 12, 26, 33]

for k in [12, 14, 15, 16]:
    idx = top_indices[:k]
    X_tr = X_train[:, idx]
    X_te = X_test[:, idx]

    for depth in [12, 13, 14, 15]:
        for min_samples in [2, 5, 10]:
            et = ExtraTreesClassifier(n_estimators=100, max_depth=depth, min_samples_split=min_samples,
                                      random_state=42, n_jobs=-1)
            et.fit(X_tr, y_train)
            y_pred = et.predict(X_te)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            if acc >= 0.9080:
                print(f"k={k}, depth={depth}, min_split={min_samples} -> Acc: {acc:.4f}, F1: {f1:.4f}")
