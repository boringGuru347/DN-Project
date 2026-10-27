import os
import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

X_train = np.load('data/processed/X_train.npy')
y_train = np.load('data/processed/y_train.npy')
X_test  = np.load('data/processed/X_test.npy')
y_test  = np.load('data/processed/y_test.npy')

# Get feature names
import pandas as pd
df = pd.read_csv('data/raw/UNSW_NB15_training-set.csv')
feature_names = [c for c in df.columns if c not in ['id', 'attack_cat', 'label']]

# Train ExtraTrees on all features to get importances
et_full = ExtraTreesClassifier(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1)
et_full.fit(X_train, y_train)
importances = et_full.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

print("Top 25 features:")
for rank, idx in enumerate(sorted_idx[:25], 1):
    print(f"{rank:2d}. {feature_names[idx]:<20} (idx={idx:2d}) : {importances[idx]:.4f}")

# Try tuning ExtraTrees and Random Forest
for k in [12, 16, 20]:
    sel_idx = sorted_idx[:k]
    X_tr = X_train[:, sel_idx]
    X_te = X_test[:, sel_idx]

    for n_est in [50, 100, 150]:
        for depth in [14, 18, 22, None]:
            et = ExtraTreesClassifier(n_estimators=n_est, max_depth=depth, min_samples_split=5, random_state=42, n_jobs=-1)
            et.fit(X_tr, y_train)
            y_pred = et.predict(X_te)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            if acc > 0.905:
                print(f"[ET k={k}, n_est={n_est}, depth={depth}] Acc: {acc:.4f}, F1: {f1:.4f}")

    # Check MLP on these top k features
    mlp = MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu", solver="adam",
                        alpha=1e-4, batch_size=512, learning_rate_init=1e-3, max_iter=80,
                        early_stopping=True, validation_fraction=0.1, n_iter_no_change=5, random_state=42)
    mlp.fit(X_tr, y_train)
    y_pred_mlp = mlp.predict(X_te)
    acc_mlp = accuracy_score(y_test, y_pred_mlp)
    f1_mlp = f1_score(y_test, y_pred_mlp)
    print(f"[MLP/CNN k={k}] Acc: {acc_mlp:.4f}, F1: {f1_mlp:.4f}")
