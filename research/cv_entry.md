# CV-ready project entry

**Investigating Class Imbalance in Machine-Learning Network Intrusion Detection** — Independent research/engineering project

- Designed and executed a reproducible benchmark study on UNSW-NB15 measuring how 50%, 20%, 10%, and 5% training attack prevalence affected Logistic Regression, Random Forest, and HistGradientBoosting models.
- Implemented leakage-aware preprocessing, fixed-test evaluation, attack-focused metrics, automated tests, machine-readable results, and reproducible experiment scripts.
- Found an attack-recall decline as training attacks became rarer across all models; documented 10,279 cross-partition feature-row matches as a material limitation rather than overstating generalization.

## Interview explanation

I chose the problem because intrusion detection is a practical classification setting where missing attacks and generating false alarms have different costs. Class imbalance means that one label, usually benign traffic, is much more common than the other. Accuracy can look strong even when a model misses many attacks, so I reported attack precision, recall, F1, PR-AUC, balanced accuracy, and confusion matrices.

I selected Logistic Regression as a transparent baseline, Random Forest as a nonlinear ensemble, and HistGradientBoosting as a compact gradient-boosting alternative. I kept the supplied test partition fixed and changed only the training attack prevalence using seeded sampling. The main result was a consistent recall decline at lower training attack prevalence, with higher precision and a trade-off in F1. The most important limitation was substantial duplication, including cross-partition feature overlap, so I would next use grouped or temporal evaluation, multiple seeds, and deduplication before making stronger claims.
