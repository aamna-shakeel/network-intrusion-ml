from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def make_models(seed: int = 42) -> dict:
    return {
        "logistic_regression": LogisticRegression(max_iter=300, solver="lbfgs", random_state=seed),
        "random_forest": RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=seed, class_weight=None),
        "hist_gradient_boosting": HistGradientBoostingClassifier(max_iter=100, learning_rate=0.1, random_state=seed),
    }
