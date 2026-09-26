# UNSW-NB15 data

The project uses the UNSW-NB15 partition documented by [UNSW Research](https://research.unsw.edu.au/projects/unsw-nb15-dataset). The official page reports 175,341 training rows and 82,332 testing rows and defines `Label` as normal (`0`) versus attack (`1`).

Download the official source files from the [UNSW SharePoint folder](https://unsw-my.sharepoint.com/:f:/g/personal/z5025758_ad_unsw_edu_au/EnuQZZn3XuNBjgfcUu4DIVMBLCHyoLHqOswirpOQifr1ag?e=gKWkLS), then place the two partition files here:

- `data/raw/UNSW_NB15_training-set.csv`
- `data/raw/UNSW_NB15_testing-set.csv`

For the local verification run, the same-named files were obtained from a public mirror because automated SharePoint download is not available in the sandbox. The mirror URLs and SHA-256 hashes are recorded in `results/data_provenance.json`; replace them with official downloads when reproducing the study.

The source grants free use for academic research and requests citation of the UNSW-NB15 papers. Commercial use requires agreement by the authors. Do not commit raw data to GitHub. The code excludes `id`, `attack_cat`, and `label` from predictors; `attack_cat` is target-derived metadata and would leak the binary target.
