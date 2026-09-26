from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric = X.select_dtypes(include=["number"]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    numeric_pipe = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical_pipe = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([("numeric", numeric_pipe, numeric), ("categorical", categorical_pipe, categorical)], remainder="drop")


def sample_training_data(X: pd.DataFrame, y: pd.Series, attack_prevalence: float, seed: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """Sample only training data to a target attack prevalence without replacement."""
    if not 0 < attack_prevalence < 1:
        raise ValueError("attack_prevalence must be strictly between 0 and 1")
    normal_idx = y.index[y == 0].to_numpy()
    attack_idx = y.index[y == 1].to_numpy()
    rng = np.random.default_rng(seed)
    if attack_prevalence <= (len(attack_idx) / len(y)):
        n_normal = len(normal_idx)
        n_attack = min(len(attack_idx), max(1, int(round(n_normal * attack_prevalence / (1 - attack_prevalence)))))
    else:
        n_attack = len(attack_idx)
        n_normal = min(len(normal_idx), max(1, int(round(n_attack * (1 - attack_prevalence) / attack_prevalence))))
    chosen = np.concatenate([rng.choice(normal_idx, n_normal, replace=False), rng.choice(attack_idx, n_attack, replace=False)])
    rng.shuffle(chosen)
    return X.loc[chosen].reset_index(drop=True), y.loc[chosen].reset_index(drop=True)
