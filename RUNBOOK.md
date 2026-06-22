# PolyDegradeML Runbook

This runbook explains how to install, run, verify, and troubleshoot the repository without changing model logic.

## Environment Setup

Recommended environment for reproducible scientific runs:

- Python 3.11
- A fresh virtual environment
- Editable install from the repository root

Health-check note: the full test suite passed in an isolated Python 3.11 target with `numpy==2.3.5`, `pandas==2.3.3`, `scikit-learn==1.7.2`, `imbalanced-learn==0.14.0`, and `matplotlib==3.10.7`. The dependency files now avoid the incompatible `scikit-learn==1.8.0` / `imbalanced-learn==0.14.0` pairing found during the audit.

```sh
cd "/Users/mannz/workspaces/polymer degredation/biodegradation-ml-framework"
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

For the most reproducible publication run, install the verified package set:

```sh
python -m pip install -r requirements-verified.txt
```

If `python3.11` is not available, use a Python version compatible with `pyproject.toml`, but verify that `numpy`, `pandas`, `scikit-learn`, `imbalanced-learn`, and `matplotlib` install cleanly.

## Local Activation Helper

After `.venv/` exists, this helper sets `PYTHONPATH` and Kaggle credential variables:

```sh
source ./activate-project.sh
```

The helper expects `.venv/` to already exist. It does not create the environment.

## Quick Verification

Run the smoke test:

```sh
PYTHONPATH=src python scripts/smoke_test_pipeline.py
```

Run the unit/regression tests:

```sh
PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py'
```

Use a noninteractive plotting backend for full workflow regeneration:

```sh
PYTHONPATH=src MPLBACKEND=Agg python scripts/generate_all_results.py
```

## Main Workflow

Run every main script in order:

```sh
PYTHONPATH=src MPLBACKEND=Agg python scripts/01_curate_dataset.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/02_run_baseline_models.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/03_run_neural_network_baseline.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/04_run_descriptor_graph_prototype.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/05_run_cross_environment_validation.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/06_run_stratified_cross_validation.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/07_run_feature_engineering_comparison.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/08_run_feature_importance_selection.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/09_run_uncertainty_reliability_analysis.py
PYTHONPATH=src MPLBACKEND=Agg python scripts/10_run_model_reliability_scoreboard.py
```

Or run the full sequence:

```sh
PYTHONPATH=src MPLBACKEND=Agg python scripts/generate_all_results.py
```

## Optional PyTorch Neural Baseline

The PyTorch baseline is an optional next-level neural-network experiment. It is not part of the canonical `generate_all_results.py` workflow because PyTorch is a heavier dependency and the result is not yet integrated into the reliability scoreboard.

Install and run it with:

```sh
python -m pip install -r requirements-pytorch.txt
PYTHONPATH=src python scripts/11_run_pytorch_neural_network_baseline.py
```

Expected outputs:

- `results/metadata/pytorch_neural_network_baseline_metrics.json`
- `results/predictions/pytorch_neural_network_predictions.csv`
- `reports/pytorch_neural_network_baseline.md`

## Expected Inputs

Primary biodegradation workflow input:

```text
datasets/qsar_biodegradation_descriptor_benchmark/raw/qsar_biodegradation.csv
```

Required columns:

- `V1` through `V41`
- `Class`

The `Class` labels are mapped as:

- `1`: `NRB`, not readily biodegradable
- `2`: `RB`, readily biodegradable

## Expected Outputs

Dataset curation:

- `datasets/qsar_biodegradation_descriptor_benchmark/processed/qsar_biodegradation_curated.csv`
- `datasets/qsar_biodegradation_descriptor_benchmark/metadata/qsar_biodegradation_metadata.json`
- `reports/dataset_curation.md`

Baseline and model outputs:

- `results/metadata/baseline_model_metrics.json`
- `results/metadata/neural_network_baseline_metrics.json`
- `results/metadata/pytorch_neural_network_baseline_metrics.json` if the optional PyTorch script is run
- `results/metadata/descriptor_graph_prototype_metrics.json`
- `reports/baseline_modeling.md`
- `reports/neural_network_baseline_summary.txt`
- `reports/pytorch_neural_network_baseline.md` if the optional PyTorch script is run
- `reports/descriptor_graph_prototype_summary.txt`

Validation and feature outputs:

- `results/tables/cross_environment_validation_summary.csv`
- `results/tables/stratified_cv_model_results.csv`
- `results/tables/feature_engineering_model_results.csv`
- `results/tables/feature_importance_rankings.csv`
- `results/tables/feature_selection_model_results.csv`
- `figures/cross_environment/`
- `figures/feature_engineering/`
- `figures/feature_importance/`

Reliability outputs:

- `results/tables/uncertainty_reliability_metrics.csv`
- `results/tables/cross_environment_uncertainty_metrics.csv`
- `results/tables/final_uncertainty_metrics.csv`
- `results/tables/model_reliability_scoreboard.csv`
- `results/predictions/prediction_level_uncertainty.csv`
- `results/predictions/selective_prediction_results.csv`
- `results/predictions/final_model_predictions.csv`
- `reports/uncertainty_reliability_summary.txt`
- `reports/model_reliability_report.md`
- `figures/uncertainty_calibration/`
- `figures/model_selection/`

## Dataset Utility Workflow

The BigSMILES/Tg dataset builder is separate from the biodegradation classifier workflow:

```sh
PYTHONPATH=src python scripts/dataset_tools/build_homopolymer_bigsmiles_dataset.py
```

Expected outputs:

- `datasets/homopolymer_bigsmiles_tg_benchmark/processed/homopolymer_bigsmiles_tg_curated.csv`
- `datasets/homopolymer_bigsmiles_tg_benchmark/metadata/source_manifest.json`

This dataset supports polymer representation work but does not contain biodegradation labels.

## Regression Template

The generic QSAR/QSPR regression template requires a user-provided CSV with a numeric target:

```sh
PYTHONPATH=src python scripts/template_run_tabular_regression_baselines.py \
  --csv /path/to/regression_dataset.csv \
  --target target_column_name \
  --output results/metadata/regression_baseline_metrics.json
```

This is a reusable template, not part of the canonical biodegradation classification result set.

## Troubleshooting

### Import errors

Use either an editable install:

```sh
python -m pip install -e .
```

or set `PYTHONPATH`:

```sh
export PYTHONPATH="$PWD/src"
```

### Matplotlib or GUI backend errors

Use:

```sh
export MPLBACKEND=Agg
```

or prefix commands with `MPLBACKEND=Agg`.

### Broken local virtual environment

If `.venv` was moved or created under a different path, recreate it:

```sh
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Only remove `.venv` when you are comfortable recreating local dependencies.

### Kaggle credentials

The repository ignores `.kaggle/`. Do not commit access tokens. For Kaggle downloads, either configure credentials locally or use the documented Kaggle/KaggleHub workflow outside the core modeling scripts.

### Generated outputs changed

Small changes can happen if dependency versions differ. Before treating a metric change as scientific, record:

```sh
python --version
python -m pip freeze
git status --short
```

Then rerun the relevant script with `MPLBACKEND=Agg`.
