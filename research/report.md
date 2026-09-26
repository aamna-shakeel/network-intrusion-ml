# Investigating the Effect of Class Imbalance on Machine-Learning Network Intrusion Detection

## Abstract

This study investigates how controlled class imbalance in training data affects binary network-intrusion detection. Using the UNSW-NB15 train/test partition, three models—Logistic Regression, Random Forest, and HistGradientBoostingClassifier—were trained with attack prevalence set to 50%, 20%, 10%, and 5%. The same supplied test partition was used for every condition. The experiment was executed rather than simulated, and the complete metrics are in `results/tables/metrics.csv`. Attack recall decreased as attack prevalence became rarer for all three models, while attack precision increased. HistGradientBoosting produced the highest attack F1 in three of four conditions, with Random Forest highest at 10%. The results are limited by substantial duplicate rows and 10,279 feature-row matches across the supplied train and test partitions. They should therefore be interpreted as benchmark observations, not evidence of production-network performance.

## 1. Introduction and problem statement

Intrusion-detection systems must identify malicious traffic among benign traffic. A missed attack can be important, but excessive false alarms can also overwhelm analysts. Class imbalance is central to this problem because operational traffic is often dominated by benign activity and because some attack types are rare. A model trained on a balanced sample may behave differently from one trained with a small attack fraction.

The project asks: **How does increasing class imbalance affect the performance of different machine-learning models for binary network intrusion detection?** The contribution is a reproducible undergraduate empirical investigation, not a new detection algorithm.

## 2. Dataset

The study uses UNSW-NB15, created at UNSW Canberra with the IXIA PerfectStorm tool in a cyber-range. The official UNSW page reports 2,540,044 records in four source CSV files and a documented partition of 175,341 training records and 82,332 test records [1]. The binary `label` field is used as provided: `0` is normal and `1` is attack. The data include categorical protocol/service/state fields, numeric flow and context features, the target-derived `attack_cat`, and an identifier.

The local files matched the documented partition sizes. The training partition contained 119,341 attacks and 56,000 normal rows; the test partition contained 45,332 attacks and 37,000 normal rows. After removing `id`, `attack_cat`, and `label`, the loader retained 42 predictors. No missing cells were observed in either local CSV. Duplicate rows were common: 74,301 in training and 28,386 in testing under the loader's feature/row check.

The files used in the sandbox run came from a public mirror because the official SharePoint folder was not directly automated. The exact URLs and SHA-256 values are recorded in `results/data_provenance.json`; the official source and academic-use terms remain the reproducibility target. Raw data are excluded from Git.

## 3. Leakage and validity audit

The binary target and `attack_cat` were excluded from predictors. Preprocessing was fit separately on each sampled training partition and then applied to the fixed test partition. The experiment did not randomly re-split the supplied train/test files.

A further audit found 10,279 training rows whose non-identifier, non-target feature values matched at least one test row. This cross-partition overlap means the reported metrics may be optimistic and cannot be treated as a clean estimate of generalization to unseen flows. The project records this result rather than hiding it. A stronger follow-up would group or deduplicate related flows before evaluation and would use temporal, host, or scenario-aware separation where the required metadata are available.

## 4. Experimental methodology

The supplied test partition remained fixed across all conditions. Only the training partition was sampled without replacement, using random seed 42. The conditions targeted attack prevalences of 50%, 20%, 10%, and 5%; the achieved prevalences were 0.500000, 0.200000, 0.099997, and 0.049994. Training sizes were 112,000, 70,000, 62,222, and 58,947 rows respectively.

Numeric predictors were median-imputed and standardized. Categorical predictors were imputed with the most frequent category and one-hot encoded. The models were Logistic Regression, Random Forest, and HistGradientBoostingClassifier. The final model is a scikit-learn gradient-boosting alternative to XGBoost chosen to keep the dependency set small and the implementation inspectable.

Metrics were accuracy, balanced accuracy, attack precision, attack recall, attack F1, ROC-AUC, PR-AUC, and confusion-matrix counts. The runner saved all 12 model-condition rows in CSV and generated F1, recall, PR-AUC, and label-distribution figures.

## 5. Results

| Training attack prevalence | Model | Attack precision | Attack recall | Attack F1 | ROC-AUC | PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 50% | Logistic Regression | 0.8039 | 0.9290 | 0.8619 | 0.9555 | 0.9669 |
| 50% | Random Forest | 0.8786 | 0.9607 | 0.9179 | 0.9815 | 0.9852 |
| 50% | HistGradientBoosting | 0.8844 | 0.9663 | 0.9235 | 0.9854 | 0.9893 |
| 20% | Logistic Regression | 0.9706 | 0.7946 | 0.8738 | 0.9547 | 0.9671 |
| 20% | Random Forest | 0.9691 | 0.8988 | 0.9326 | 0.9848 | 0.9886 |
| 20% | HistGradientBoosting | 0.9698 | 0.9017 | 0.9345 | 0.9845 | 0.9886 |
| 10% | Logistic Regression | 0.9935 | 0.7191 | 0.8343 | 0.9544 | 0.9669 |
| 10% | Random Forest | 0.9920 | 0.8625 | 0.9228 | 0.9842 | 0.9883 |
| 10% | HistGradientBoosting | 0.9859 | 0.8648 | 0.9214 | 0.9833 | 0.9877 |
| 5% | Logistic Regression | 0.9986 | 0.6959 | 0.8202 | 0.9538 | 0.9664 |
| 5% | Random Forest | 0.9979 | 0.8358 | 0.9097 | 0.9847 | 0.9885 |
| 5% | HistGradientBoosting | 0.9946 | 0.8387 | 0.9100 | 0.9841 | 0.9882 |

## 6. Discussion

The main observed pattern is a recall-precision trade-off. As attack prevalence decreased in the training sample, attack recall fell for every model. Logistic Regression showed the largest recall decline, from 0.9290 at 50% to 0.6959 at 5%. Random Forest declined from 0.9607 to 0.8358, and HistGradientBoosting from 0.9663 to 0.8387. At the same time, attack precision rose because the models generated fewer false positives on the fixed test set.

Accuracy alone would not explain this behavior. For example, Logistic Regression accuracy was 0.8320 at 5% and 0.8361 at 50%, while attack recall changed by more than 0.23. The precision, recall, F1, and PR-AUC columns provide a more useful view of the detection trade-off.

The nonlinear models were stronger than the linear baseline on attack F1 in every condition. HistGradientBoosting achieved the highest F1 at 50%, 20%, and 5%, while Random Forest was marginally highest at 10%. The differences between the two tree-based models were small at 10% and 5%, so this run does not justify claiming a universal winner.

The high ROC-AUC and PR-AUC values should be read with caution because of the duplicate and cross-partition overlap found in the audit. The evaluation is reproducible for the selected files and protocol, but it is not independent-flow generalization evidence.

## 7. Limitations

UNSW-NB15 was collected in a controlled cyber-range and includes synthetic attacks. Its feature engineering includes context/count variables, and the released train/test data contain substantial duplicate rows. The cross-partition feature overlap found here may inflate performance. The experiment manipulates training prevalence by sampling and does not estimate naturally occurring attack prevalence. Only one seed and one supplied test partition were used. The model set is intentionally small, and no threshold calibration, cost-sensitive learning, scenario-aware split, or deployment test was performed.

The local execution used a public mirror rather than a direct automated download from the official SharePoint folder. Although the official UNSW page grants academic use and the mirror files were hash-recorded, a future reproduction should download the files from the official source and record the exact release and checksums.

## 8. Ethics and responsible use

This project is defensive cybersecurity research. It analyzes a public academic benchmark and does not target unauthorized systems, generate real intrusions, or provide operational attack instructions. Reported model scores should not be used to claim that an IDS is safe to deploy without independent validation on representative, properly separated traffic.

## 9. Conclusion and future work

Under this controlled protocol, lower attack prevalence in training was associated with lower attack recall and higher attack precision for all three models. The tree-based models maintained higher attack recall and F1 than Logistic Regression, but the apparent performance is constrained by dataset duplication and cross-partition overlap. The result supports emphasizing imbalance-aware metrics and leakage audits rather than accuracy alone.

Next steps are to obtain the official release directly, deduplicate or group related flows, design a temporal/scenario-aware evaluation, repeat conditions across several seeds, compare class weighting and threshold tuning, and test whether the observed conclusions persist on CIC-IDS2017 or another independently sourced benchmark.

## References

[1]: https://research.unsw.edu.au/projects/unsw-nb15-dataset "The UNSW-NB15 Dataset"
[2]: https://doi.org/10.1109/MilCIS.2015.7348942 "UNSW-NB15: a comprehensive data set for network intrusion detection systems"
[3]: https://doi.org/10.26190/5d7ac5b1e8485 "UNSW-NB15 dataset record"
