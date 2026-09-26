from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "raw" / "UNSW_NB15_training-set.csv"
TEST_PATH = ROOT / "data" / "raw" / "UNSW_NB15_testing-set.csv"
RESULTS_DIR = ROOT / "results"
SEED = 42
ATTACK_PREVALENCE = {"balanced_50_50": 0.50, "imbalanced_80_20": 0.20, "imbalanced_90_10": 0.10, "imbalanced_95_5": 0.05}
