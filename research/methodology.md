# Methodology

## Research question

How does increasing class imbalance in the training data affect binary network-intrusion detection performance for a linear model, a tree ensemble, and a boosting model?

## Dataset and target

The study uses the UNSW-NB15 train/test partition documented by UNSW Research. The binary `label` is retained as the target (`0` normal, `1` attack). The identifier `id`, multiclass `attack_cat`, and target are excluded from predictors. The official source reports 175,341 training rows and 82,332 testing rows; the local run records observed counts in `results/data_summary.json`.

## Controlled imbalance

The supplied test partition remains fixed for every condition. Only the training partition is sampled. Four attack prevalences are evaluated: 50%, 20%, 10%, and 5%. Sampling is without replacement with seed 42. The actual row counts and prevalence are written to `results/tables/metrics.csv`.

## Preprocessing and models

Numeric features are median-imputed and standardized. Categorical features are most-frequent-imputed and one-hot encoded. The transformer is fit separately on each sampled training set and never on the test partition. Models are Logistic Regression, Random Forest, and HistGradientBoostingClassifier. HistGradientBoosting is used as a scikit-learn gradient-boosting alternative to XGBoost so the baseline remains easy to install and inspect.

## Evaluation

The fixed test set is evaluated using accuracy, balanced accuracy, attack precision, attack recall, attack F1, ROC-AUC, PR-AUC, and the confusion-matrix counts. Minority-class metrics are emphasized because accuracy can remain high when the normal class dominates.

## Limitations

This is a controlled benchmark experiment, not evidence of production IDS performance. UNSW-NB15 traffic was collected in a cyber-range with synthetic attacks. The supplied feature set contains context/count variables; the official train/test partition is therefore retained rather than randomly re-split. The local sandbox run uses public mirror copies because the official SharePoint folder is not directly automated; hashes and URLs are recorded for audit.
