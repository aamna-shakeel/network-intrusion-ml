from __future__ import annotations

import numpy as np
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score)


def evaluate_binary(y_true, y_pred, y_score) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {"accuracy": float(accuracy_score(y_true, y_pred)), "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)), "precision_attack": float(precision_score(y_true, y_pred, zero_division=0)), "recall_attack": float(recall_score(y_true, y_pred, zero_division=0)), "f1_attack": float(f1_score(y_true, y_pred, zero_division=0)), "roc_auc": float(roc_auc_score(y_true, y_score)), "pr_auc": float(average_precision_score(y_true, y_score)), "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
