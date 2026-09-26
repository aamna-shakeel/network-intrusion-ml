from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import RESULTS_DIR, TEST_PATH, TRAIN_PATH
from src.data_loader import dataset_summary


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "figures").mkdir(exist_ok=True)
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    summary = {"train": dataset_summary(TRAIN_PATH), "test": dataset_summary(TEST_PATH), "train_dtypes": {k: str(v) for k, v in train.dtypes.items()}, "train_label_counts": train["label"].value_counts().to_dict(), "test_label_counts": test["label"].value_counts().to_dict(), "train_attack_categories": train["attack_cat"].value_counts(dropna=False).to_dict(), "infinite_values": int(train.select_dtypes("number").isin([float("inf"), float("-inf")]).sum().sum())}
    (RESULTS_DIR / "exploration_summary.json").write_text(json.dumps(summary, indent=2, default=int))
    counts = train["label"].map({0: "Normal", 1: "Attack"}).value_counts().reindex(["Normal", "Attack"])
    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot.bar(ax=ax, color=["#4c78a8", "#e45756"])
    ax.set_ylabel("Rows")
    ax.set_title("UNSW-NB15 training labels")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figures" / "training_label_distribution.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
