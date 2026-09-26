# Literature and dataset review

## Network intrusion detection and machine learning

UNSW-NB15 was introduced to provide a newer intrusion-detection benchmark than older KDD-derived datasets. The original paper describes a hybrid collection of normal activity and contemporary synthetic attacks generated in the UNSW Canberra cyber range [1]. The official UNSW page documents nine attack categories, 49 generated features, raw packet captures, flow-derived files, and a published train/test partition [2].

Machine-learning results on intrusion datasets are sensitive to the data-generation process and evaluation split. A model can learn repeated flow patterns, context variables, or artifacts specific to a testbed rather than a transferable notion of malicious activity. For that reason, this project treats UNSW-NB15 as a controlled benchmark and not as a representative sample of operational traffic.

## Class imbalance and evaluation

When one class is common, accuracy can hide poor minority detection. In an intrusion-detection setting, attack recall measures how many attacks are found, while precision describes the false-alarm burden among predicted attacks. F1 summarizes the two at one threshold. ROC-AUC summarizes ranking across thresholds, while PR-AUC is especially useful to inspect when the positive class is rare because it focuses on precision-recall behavior.

This project therefore reports accuracy together with balanced accuracy, attack precision, attack recall, attack F1, ROC-AUC, PR-AUC, and confusion-matrix counts. No single metric is treated as sufficient.

## Dataset selection

CIC-IDS2017 was considered because it has official documentation and labeled flow products, but independent analyses report construction, timing, duplicate, and labeling problems that make casual random row splits particularly risky [3] [4]. NSL-KDD has convenient binary labels and fixed partitions, but the official page now says the original dataset is no longer available there and it remains a historical KDD'99-derived benchmark [5]. UNSW-NB15 was selected because its institutional source documents the binary label, train/test partition, acquisition materials, and academic-use terms [2] [6].

## References

[1]: https://doi.org/10.1109/MilCIS.2015.7348942 "UNSW-NB15: a comprehensive data set for network intrusion detection systems"
[2]: https://research.unsw.edu.au/projects/unsw-nb15-dataset "The UNSW-NB15 Dataset"
[3]: https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf "Troubleshooting an Intrusion Detection Dataset"
[4]: https://hal.science/hal-03775466v1/document "A critical analysis of CICIDS2017"
[5]: https://www.unb.ca/cic/datasets/nsl.html "NSL-KDD dataset"
[6]: https://doi.org/10.26190/5d7ac5b1e8485 "UNSW-NB15 dataset record"
