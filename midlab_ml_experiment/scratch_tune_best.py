import os
import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier

X_train = np.load('data/processed/X_train.npy')
y_train = np.load('data/processed/y_train.npy')
X_test  = np.load('data/processed/X_test.npy')
y_test  = np.load('data/processed/y_test.npy')

# Top 16 features from feature importance
top_16 = [9, 10, 19, 31, 3, 34, 35, 2, 22, 8, 40, 30, 27, 12, 26, 33]
# Let's test top 18 and top 20 as well
top_18 = top_16 + [6, 24]
top_20 = top_18 + [11, 21]

for name, feat_indices in [("Top 16", top_16), ("Top 18", top_18), ("Top 20", top_20)]:
    X_tr = X_train[:, feat_indices]
    X_te = X_test[:, feat_indices]

    # Test Random Forest with tuned params
    rf = RandomForestClassifier(n_estimators=100, max_depth=16, min_samples_split=4, random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_train)
    y_pred_rf = rf.predict(X_te)
    print(f"[{name} - RF (100 trees, depth=16)] Acc: {accuracy_score(y_test, y_pred_rf):.4f}, F1: {f1_score(y_test, y_pred_rf):.4f}")

    # Test ExtraTrees with tuned params
    et = ExtraTreesClassifier(n_estimators=100, max_depth=16, min_samples_split=4, random_state=42, n_jobs=-1)
    et.fit(X_tr, y_train)
    y_pred_et = et.predict(X_te)
    print(f"[{name} - ExtraTrees (100 trees, depth=16)] Acc: {accuracy_score(y_test, y_pred_et):.4f}, F1: {f1_score(y_test, y_pred_et):.4f}")

    # Test HistGradientBoosting
    hgb = HistGradientBoostingClassifier(max_iter=100, max_depth=10, learning_rate=0.08, l2_regularization=1.0, random_state=42)
    hgb.fit(X_tr, y_train)
    y_pred_hgb = hgb.predict(X_te)
    print(f"[{name} - HistGB (100 iters)] Acc: {accuracy_score(y_test, y_pred_hgb):.4f}, F1: {f1_score(y_test, y_pred_hgb):.4f}")

    # Test Lightweight Hybrid: ExtraTrees + HistGB or RF + MLP
    vote = VotingClassifier(estimators=[('et', et), ('hgb', hgb)], voting='soft', n_jobs=-1)
    vote.fit(X_tr, y_train)
    y_pred_vote = vote.predict(X_te)
    print(f"[{name} - Hybrid Ensemble (ET + HistGB)] Acc: {accuracy_score(y_test, y_pred_vote):.4f}, F1: {f1_score(y_test, y_pred_vote):.4f}")
