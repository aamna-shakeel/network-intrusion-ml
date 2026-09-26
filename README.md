# Investigating Class Imbalance in Machine-Learning Network Intrusion Detection

This repository contains a reproducible undergraduate research/engineering study of how controlled training-set class imbalance affects binary network-intrusion detection models.

> **Research question:** How does increasing class imbalance affect the performance of different machine-learning models for binary network intrusion detection?

## Current status

The first executed experiment trained three models under four training attack prevalences and evaluated every model on the same untouched UNSW-NB15 test partition. The measured metrics are in [`results/tables/metrics.csv`](results/tables/metrics.csv), with figures in [`results/figures/`](results/figures/).

The results are benchmark evidence, not a claim of production-network effectiveness. The data contain many duplicate rows, including 10,279 feature-row matches across the supplied train and test partitions after excluding identifiers and target metadata. This important limitation is documented in [`research/report.md`](research/report.md).

## Dataset

The study uses the UNSW-NB15 train/test partition documented by [UNSW Research](https://research.unsw.edu.au/projects/unsw-nb15-dataset). The official page reports 175,341 training records and 82,332 testing records, with `label` defined as normal (`0`) or attack (`1`). The official source grants free academic use and requests citation of the dataset papers; commercial use requires agreement by the authors.

Raw CSV files are intentionally excluded from Git. See [`data/README.md`](data/README.md) for official acquisition instructions and the exact mirror URLs and SHA-256 hashes used for the sandbox run.

## Methodology

- `label` is the binary target; `id` and `attack_cat` are excluded as leakage-prone metadata.
- Numeric features receive training-only median imputation and standardization.
- Categorical features receive training-only most-frequent imputation and one-hot encoding.
- The supplied test partition is fixed across all conditions.
- Only the training partition is sampled, without replacement, using seed `42`.
- Training attack prevalence conditions are 50%, 20%, 10%, and 5%.
- Metrics include accuracy, balanced accuracy, attack precision, attack recall, attack F1, ROC-AUC, PR-AUC, and confusion-matrix counts.

Models:

1. Logistic Regression as a transparent linear baseline.
2. Random Forest as a nonlinear tree ensemble.
3. HistGradientBoostingClassifier as an inspectable scikit-learn gradient-boosting alternative to XGBoost.

## Observed results

The run produced 12 model-condition evaluations. Attack recall generally fell as the training attack prevalence decreased: for example, Logistic Regression declined from `0.9290` at 50% to `0.6959` at 5%; Random Forest declined from `0.9607` to `0.8358`; and HistGradientBoosting declined from `0.9663` to `0.8387`. Attack precision moved in the opposite direction because the models produced fewer false positives at lower attack prevalence. HistGradientBoosting achieved the highest attack F1 at 50%, 20%, and 5%; Random Forest was highest at 10%.

These are observations for this dataset, split, preprocessing, seed, and model configuration. They should not be generalized beyond the documented benchmark.

## Repository structure

```text
├── data/
│   └── README.md
├── research/
│   ├── literature_review.md
│   ├── methodology.md
│   └── report.md
├── results/
│   ├── data_provenance.json
│   ├── data_summary.json
│   ├── exploration_summary.json
│   ├── figures/
│   └── tables/metrics.csv
├── scripts/
│   ├── explore_data.py
│   └── run_experiments.py
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── models.py
│   └── preprocessing.py
├── tests/test_core.py
├── PROJECT_PLAN.md
├── requirements.txt
└── README.md
```

## Reproduce the run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Place the two CSV files described in data/README.md under data/raw/
PYTHONPATH=. python scripts/explore_data.py
PYTHONPATH=. python scripts/run_experiments.py
PYTHONPATH=. pytest -q
```

The executed sandbox run used Python 3.12, pandas 3.0.5, NumPy 2.5.1, scikit-learn 1.8.0, and Matplotlib 3.11.1. The dependency file constrains major versions but does not claim a lockfile-level environment.

## Ethics and limitations

This is defensive cybersecurity research using a public academic benchmark. It does not target unauthorized systems or provide intrusion instructions. The data were collected in a controlled cyber-range with synthetic attacks, so performance does not establish deployment readiness. Duplicate and cross-partition feature rows may inflate scores. The study also changes training prevalence by sampling; it does not estimate naturally occurring threat prevalence. These limitations constrain the conclusions.

## References

- Moustafa, N. and Slay, J. (2015), “UNSW-NB15: a comprehensive data set for network intrusion detection systems,” [IEEE record](https://doi.org/10.1109/MilCIS.2015.7348942).
- [UNSW-NB15 official dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
- [UNSW-NB15 dataset record](https://doi.org/10.26190/5d7ac5b1e8485).
