from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
plt.rcParams["axes.unicode_minus"] = False
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import ATTACK_PREVALENCE, RESULTS_DIR, SEED, TEST_PATH, TRAIN_PATH
from src.data_loader import dataset_summary, load_unsw_csv
from src.evaluation import evaluate_binary
from src.models import make_models
from src.preprocessing import make_preprocessor, sample_training_data


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "figures").mkdir(exist_ok=True)
    (RESULTS_DIR / "tables").mkdir(exist_ok=True)
    train_summary = dataset_summary(TRAIN_PATH)
    test_summary = dataset_summary(TEST_PATH)
    (RESULTS_DIR / "data_summary.json").write_text(json.dumps({"train": train_summary, "test": test_summary}, indent=2))
    (RESULTS_DIR / "data_provenance.json").write_text(json.dumps({
        "train_source": "https://raw.githubusercontent.com/Nir-J/ML-Projects/master/UNSW-Network_Packet_Classification/UNSW_NB15_training-set.csv",
        "test_source": "https://raw.githubusercontent.com/Nir-J/ML-Projects/master/UNSW-Network_Packet_Classification/UNSW_NB15_testing-set.csv",
        "train_sha256": "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa",
        "test_sha256": "734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559",
        "official_source": "https://research.unsw.edu.au/projects/unsw-nb15-dataset",
        "note": "Mirror used for sandbox execution; official UNSW source remains the reproducibility target."
    }, indent=2))
    X_train, y_train = load_unsw_csv(TRAIN_PATH)
    X_test, y_test = load_unsw_csv(TEST_PATH)
    rows = []
    models = make_models(SEED)
    for condition, prevalence in ATTACK_PREVALENCE.items():
        X_sample, y_sample = sample_training_data(X_train, y_train, prevalence, SEED)
        preprocessor = make_preprocessor(X_sample)
        X_fit = preprocessor.fit_transform(X_sample)
        X_eval = preprocessor.transform(X_test)
        actual_prevalence = float(y_sample.mean())
        for model_name, model in models.items():
            model.fit(X_fit, y_sample)
            pred = model.predict(X_eval)
            score = model.predict_proba(X_eval)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X_eval)
            metrics = evaluate_binary(y_test, pred, score)
            rows.append({"condition": condition, "target_attack_prevalence": prevalence, "actual_train_attack_prevalence": actual_prevalence, "train_rows": len(y_sample), "model": model_name, **metrics})
            print(condition, model_name, metrics)
    results = pd.DataFrame(rows)
    results.to_csv(RESULTS_DIR / "tables" / "metrics.csv", index=False)
    for metric, ylabel, filename in [("f1_attack", "Attack-class F1", "f1_vs_imbalance.png"), ("recall_attack", "Attack-class recall", "recall_vs_imbalance.png"), ("pr_auc", "Average precision (PR-AUC)", "pr_auc_vs_imbalance.png")]:
        fig, ax = plt.subplots(figsize=(8, 5))
        for model_name, group in results.groupby("model"):
            group = group.sort_values("actual_train_attack_prevalence")
            ax.plot(group["actual_train_attack_prevalence"], group[metric], marker="o", label=model_name)
        ax.set_xlabel("Training attack prevalence")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{ylabel} under controlled training imbalance")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(RESULTS_DIR / "figures" / filename, dpi=160)
        plt.close(fig)
    print(f"Wrote {len(results)} model-condition rows to {RESULTS_DIR / 'tables' / 'metrics.csv'}")


if __name__ == "__main__":
    main()
