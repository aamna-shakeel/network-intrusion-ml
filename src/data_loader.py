from __future__ import annotations

from pathlib import Path
import pandas as pd

TARGET = "label"
LEAKAGE_COLUMNS = {"id", "attack_cat", TARGET}


def load_unsw_csv(path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load one official UNSW-NB15 partition and return features plus binary Label."""
    frame = pd.read_csv(path)
    frame.columns = [str(c).strip() for c in frame.columns]
    if TARGET not in frame:
        raise ValueError(f"Expected binary target column {TARGET!r}; found {list(frame.columns)}")
    y = frame[TARGET].astype("int8")
    if not set(y.unique()).issubset({0, 1}):
        raise ValueError("UNSW-NB15 label must contain only 0 (normal) and 1 (attack)")
    feature_columns = [c for c in frame.columns if c not in LEAKAGE_COLUMNS]
    X = frame[feature_columns].copy()
    X = X.replace([float("inf"), float("-inf")], pd.NA)
    return X, y


def dataset_summary(path: str | Path) -> dict:
    X, y = load_unsw_csv(path)
    return {"path": str(path), "rows": int(len(X)), "features": int(X.shape[1]), "attack": int(y.sum()), "normal": int((y == 0).sum()), "missing_cells": int(X.isna().sum().sum()), "duplicate_rows": int(X.duplicated().sum())}
