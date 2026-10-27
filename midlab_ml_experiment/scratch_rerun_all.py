import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.utils.extmath import safe_sparse_dot

X_train = np.load('data/processed/X_train.npy')
y_train = np.load('data/processed/y_train.npy')
X_test  = np.load('data/processed/X_test.npy')
y_test  = np.load('data/processed/y_test.npy')

# Top 15 features
# 9: sttl, 10: dttl, 19: swin, 31: ct_state_ttl, 3: state, 34: ct_dst_sport_ltm,
# 35: ct_dst_src_ltm, 2: service, 22: dwin, 8: rate, 40: ct_srv_dst, 30: ct_srv_src,
# 27: dmean, 12: dload, 26: smean
top_15 = [9, 10, 19, 31, 3, 34, 35, 2, 22, 8, 40, 30, 27, 12, 26]

X_tr = X_train[:, top_15]
X_te = X_test[:, top_15]

# 1. Final Proposed ML Model: Lightweight ExtraTrees
et = ExtraTreesClassifier(n_estimators=100, max_depth=12, min_samples_split=2, random_state=42, n_jobs=-1)
t0 = time.perf_counter()
et.fit(X_tr, y_train)
t_train_et = time.perf_counter() - t0
t0 = time.perf_counter()
y_pred_et = et.predict(X_te)
t_infer_et = time.perf_counter() - t0
acc_et = accuracy_score(y_test, y_pred_et)
prec_et = precision_score(y_test, y_pred_et)
rec_et = recall_score(y_test, y_pred_et)
f1_et = f1_score(y_test, y_pred_et)
cm_et = confusion_matrix(y_test, y_pred_et)
fpr_et = cm_et[0,1] / (cm_et[0,0] + cm_et[0,1])
print(f"Proposed Model (ExtraTrees): Acc={acc_et:.4f}, Prec={prec_et:.4f}, Rec={rec_et:.4f}, F1={f1_et:.4f}, FPR={fpr_et:.4f}, Train={t_train_et:.2f}s, Infer={t_infer_et:.4f}s")

# 2. Rerun CNN on new 15 features
mlp = MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu", solver="adam", alpha=1e-4,
                    batch_size=512, learning_rate_init=1e-3, max_iter=80, early_stopping=True,
                    validation_fraction=0.1, n_iter_no_change=5, random_state=42)
t0 = time.perf_counter()
mlp.fit(X_tr, y_train)
t_train_mlp = time.perf_counter() - t0
t0 = time.perf_counter()
y_pred_mlp = mlp.predict(X_te)
t_infer_mlp = time.perf_counter() - t0
acc_mlp = accuracy_score(y_test, y_pred_mlp)
prec_mlp = precision_score(y_test, y_pred_mlp)
rec_mlp = recall_score(y_test, y_pred_mlp)
f1_mlp = f1_score(y_test, y_pred_mlp)
cm_mlp = confusion_matrix(y_test, y_pred_mlp)
fpr_mlp = cm_mlp[0,1] / (cm_mlp[0,0] + cm_mlp[0,1])
print(f"Rerun CNN: Acc={acc_mlp:.4f}, Prec={prec_mlp:.4f}, Rec={rec_mlp:.4f}, F1={f1_mlp:.4f}, FPR={fpr_mlp:.4f}, Train={t_train_mlp:.2f}s, Infer={t_infer_mlp:.4f}s")

# 3. Rerun SVM on new 15 features
# Note: SVM on 82k train takes ~40-50s
svm = SVC(kernel="rbf", C=1.0, gamma="scale", cache_size=1000, random_state=42)
t0 = time.perf_counter()
svm.fit(X_tr, y_train)
t_train_svm = time.perf_counter() - t0
t0 = time.perf_counter()
y_pred_svm = svm.predict(X_te)
t_infer_svm = time.perf_counter() - t0
acc_svm = accuracy_score(y_test, y_pred_svm)
prec_svm = precision_score(y_test, y_pred_svm)
rec_svm = recall_score(y_test, y_pred_svm)
f1_svm = f1_score(y_test, y_pred_svm)
cm_svm = confusion_matrix(y_test, y_pred_svm)
fpr_svm = cm_svm[0,1] / (cm_svm[0,0] + cm_svm[0,1])
print(f"Rerun SVM: Acc={acc_svm:.4f}, Prec={prec_svm:.4f}, Rec={rec_svm:.4f}, F1={f1_svm:.4f}, FPR={fpr_svm:.4f}, Train={t_train_svm:.2f}s, Infer={t_infer_svm:.4f}s")

# 4. Rerun CNN+SVM
# Extract 64-D activations from hidden layer 1
X_tr_h1 = np.maximum(0, safe_sparse_dot(X_tr, mlp.coefs_[0]) + mlp.intercepts_[0])
X_te_h1 = np.maximum(0, safe_sparse_dot(X_te, mlp.coefs_[0]) + mlp.intercepts_[0])
svm_hybrid = SVC(kernel="rbf", C=1.0, gamma="scale", cache_size=1000, random_state=42)
t0 = time.perf_counter()
svm_hybrid.fit(X_tr_h1, y_train)
t_train_hybrid = time.perf_counter() - t0 + t_train_mlp
t0 = time.perf_counter()
y_pred_hybrid = svm_hybrid.predict(X_te_h1)
t_infer_hybrid = time.perf_counter() - t0 + t_infer_mlp
acc_hyb = accuracy_score(y_test, y_pred_hybrid)
prec_hyb = precision_score(y_test, y_pred_hybrid)
rec_hyb = recall_score(y_test, y_pred_hybrid)
f1_hyb = f1_score(y_test, y_pred_hybrid)
cm_hyb = confusion_matrix(y_test, y_pred_hybrid)
fpr_hyb = cm_hyb[0,1] / (cm_hyb[0,0] + cm_hyb[0,1])
print(f"Rerun CNN+SVM: Acc={acc_hyb:.4f}, Prec={prec_hyb:.4f}, Rec={rec_hyb:.4f}, F1={f1_hyb:.4f}, FPR={fpr_hyb:.4f}, Train={t_train_hybrid:.2f}s, Infer={t_infer_hybrid:.4f}s")
