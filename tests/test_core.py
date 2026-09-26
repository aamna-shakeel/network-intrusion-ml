import pandas as pd

from src.data_loader import load_unsw_csv
from src.evaluation import evaluate_binary
from src.preprocessing import make_preprocessor, sample_training_data


def test_target_columns_are_excluded(tmp_path):
    path = tmp_path / "sample.csv"
    pd.DataFrame({"id": [1, 2], "proto": ["tcp", "udp"], "feature": [1.0, None], "attack_cat": ["Normal", "Generic"], "label": [0, 1]}).to_csv(path, index=False)
    X, y = load_unsw_csv(path)
    assert list(X.columns) == ["proto", "feature"]
    assert y.tolist() == [0, 1]


def test_sampling_hits_requested_prevalence():
    X = pd.DataFrame({"x": range(100)})
    y = pd.Series([0] * 60 + [1] * 40)
    _, sampled_y = sample_training_data(X, y, 0.2, seed=7)
    assert abs(sampled_y.mean() - 0.2) < 0.01


def test_preprocessor_handles_missing_and_categories():
    X = pd.DataFrame({"num": [1.0, None, 3.0], "cat": ["a", "b", "a"]})
    transformed = make_preprocessor(X).fit_transform(X)
    assert transformed.shape[0] == 3
    assert transformed.shape[1] >= 2


def test_evaluation_metrics_are_computed():
    result = evaluate_binary([0, 0, 1, 1], [0, 1, 1, 1], [0.1, 0.8, 0.7, 0.9])
    assert result["tp"] == 2
    assert result["fp"] == 1
    assert 0 <= result["pr_auc"] <= 1
