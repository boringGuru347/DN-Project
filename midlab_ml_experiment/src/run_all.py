"""
run_all.py — Master script: runs the complete preliminary ML experiment.

Execution order:
  1. preprocessing.py      — load, clean, encode, scale UNSW-NB15
  2. feature_selection.py  — select k=20 features + generate sweep data
  3. generate_diagrams.py  — produce flow diagrams (does not depend on results)
  4. train_cnn.py          — train standalone CNN
  5. train_svm.py          — train standalone SVM
  6. train_cnn_svm.py      — train CNN+SVM (requires trained CNN)
  7. evaluate.py           — evaluate all three models and save metrics
  8. generate_graphs.py    — generate all 5 result graphs

Run from inside the midlab_ml_experiment/ directory:
  python src/run_all.py

Or, if calling from another directory, provide the full path:
  python "C:/path/to/midlab_ml_experiment/src/run_all.py"
"""

import os
import sys
import time
import json

# Ensure src/ is on the path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from utils import (
    MODELS_DIR, ensure_dirs, get_logger, save_json,
)

log = get_logger("run_all")

SEPARATOR = "=" * 60


def step(title: str):
    log.info(SEPARATOR)
    log.info("STEP: %s", title)
    log.info(SEPARATOR)


def main():
    ensure_dirs()
    total_start = time.perf_counter()

    # ------------------------------------------------------------------
    # Step 1 — Preprocessing
    # ------------------------------------------------------------------
    step("1 / 8 — Preprocessing")
    from preprocessing import run_preprocessing
    run_preprocessing()

    # ------------------------------------------------------------------
    # Step 2 — Feature Selection
    # ------------------------------------------------------------------
    step("2 / 8 — Feature Selection")
    from feature_selection import run_feature_selection
    run_feature_selection()

    # ------------------------------------------------------------------
    # Step 3 — Generate diagrams (independent of results)
    # ------------------------------------------------------------------
    step("3 / 8 — Generating Flow Diagrams")
    from generate_diagrams import run_generate_diagrams
    run_generate_diagrams()

    # ------------------------------------------------------------------
    # Step 4 — Train CNN
    # ------------------------------------------------------------------
    step("4 / 8 — Training CNN")
    from train_cnn import run_train_cnn
    _, cnn_time = run_train_cnn()
    # cnn_time is already saved inside run_train_cnn via CNN_HISTORY_PATH

    # ------------------------------------------------------------------
    # Step 5 — Train SVM
    # ------------------------------------------------------------------
    step("5 / 8 — Training SVM")
    from train_svm import run_train_svm
    _, svm_time = run_train_svm()
    # Save SVM timing so evaluate.py can load it
    save_json({"training_time_sec": svm_time},
              os.path.join(MODELS_DIR, "svm_timing.json"))

    # ------------------------------------------------------------------
    # Step 6 — Train CNN+SVM
    # ------------------------------------------------------------------
    step("6 / 8 — Training CNN+SVM")
    from train_cnn_svm import run_train_cnn_svm
    _, _, cnn_svm_time = run_train_cnn_svm()
    save_json({"training_time_sec": cnn_svm_time},
              os.path.join(MODELS_DIR, "cnn_svm_timing.json"))

    # ------------------------------------------------------------------
    # Step 7 — Evaluate
    # ------------------------------------------------------------------
    step("7 / 8 — Evaluating All Models")
    from evaluate import run_evaluate
    results = run_evaluate()

    # ------------------------------------------------------------------
    # Step 8 — Generate Result Graphs
    # ------------------------------------------------------------------
    step("8 / 8 — Generating Result Graphs")
    from generate_graphs import run_generate_graphs
    run_generate_graphs()

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    total_time = time.perf_counter() - total_start
    log.info(SEPARATOR)
    log.info("ALL STEPS COMPLETE")
    log.info("Total wall-clock time: %.1f seconds (%.1f minutes)",
             total_time, total_time / 60)
    log.info(SEPARATOR)

    log.info("\nKey output locations:")
    log.info("  Comparison table : results/model_comparison.csv")
    log.info("  Detailed metrics : results/metrics.csv")
    log.info("  Graphs           : graphs/")
    log.info("  Diagrams         : diagrams/")
    log.info("  Confusion matrices: results/confusion_matrices/")

    log.info("\nPreliminary Results Summary:")
    for r in results:
        log.info(
            "  %-10s  Acc=%.4f  F1=%.4f  Train=%.1fs  Infer=%.4fs",
            r["model"], r["accuracy"], r["f1"],
            r["training_time_s"], r["inference_time_s"],
        )


if __name__ == "__main__":
    main()
