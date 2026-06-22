# PolyDegradeML

Reliability-aware machine learning for polymer biodegradation prediction from descriptor-based chemical data.

![PolyDegradeML banner](figures/branding/polydegrademl_banner.png)

This repository organizes a QSAR/QSPR-style biodegradation prediction study as a reusable scientific evaluation framework. The current implementation uses a descriptor-based biodegradation dataset, compares multiple machine learning models, evaluates chemistry-informed feature engineering, and emphasizes reliability metrics such as calibration, uncertainty separation, selective prediction, and cross-environment generalization.

Repository URL: [zmanna/PolyDegradeML](https://github.com/zmanna/PolyDegradeML)

## Quickstart

```sh
git clone https://github.com/zmanna/PolyDegradeML.git
cd PolyDegradeML
source ./activate-project.sh
python -m pip install -e .
python scripts/generate_all_results.py
```

For deeper developer orientation, see `RUNBOOK.md`, `REPOSITORY_MAP.md`, and `CODEBASE_AUDIT.md`.

For manuscript and presentation traceability, see `docs/publication_artifact_provenance.md`.

## Key Findings

- Random Forest with the top-ranked feature set achieved the strongest final reliability profile in the current scoreboard.
- Calibration, uncertainty separation, selective prediction, and cross-environment behavior changed the interpretation of model quality beyond accuracy alone.
- Chemistry-informed proxy features and feature selection were scientifically useful because their value could be evaluated through reliability metrics rather than a single headline score.
- The feedforward neural-network baseline was informative as a nonlinear complexity check, but model complexity alone did not supersede the strongest classical baseline on this descriptor-only dataset.

## Research Workflow

![PolyDegradeML research workflow](figures/paper/figure_1_research_workflow.png)

## Result Highlights

| Feature Importance | Calibration | Reliability Scoreboard |
| --- | --- | --- |
| ![Top feature importance](figures/paper/figure_2_feature_importance.png) | ![Calibration curve](figures/paper/figure_3_calibration_curve.png) | ![Reliability scoreboard](figures/paper/figure_4_reliability_scoreboard.png) |

The curated paper-facing figure set lives in `figures/paper/`. The canonical generated plots remain grouped by analysis workflow under `figures/`.

## Research Question

Can chemistry-informed feature engineering and reliability-focused evaluation improve the trustworthiness of machine learning models for biodegradation prediction?

The project is framed around model trustworthiness rather than raw accuracy alone. Standard classification metrics are reported alongside calibration, uncertainty, and distribution-shift behavior.

## Project Structure

```text
.
├── datasets/
│   └── qsar_biodegradation_descriptor_benchmark/
│       ├── raw/                     # Original descriptor-only QSAR biodegradation CSV
│       ├── processed/               # Curated dataset with stable labels/columns
│       └── metadata/                # Dataset metadata and curation decisions
├── src/biodegradation_ml_framework/ # Reusable Python package
├── scripts/                         # Ordered research workflow scripts
├── results/
│   ├── tables/                      # Generated CSV result tables
│   ├── predictions/                 # Prediction-level outputs
│   └── metadata/                    # Generated JSON metrics/config artifacts
├── figures/                         # Generated figures plus curated branding/paper views
├── reports/                         # Human-readable analysis summaries
├── source_materials/                # Original weekly reports and reading reports
├── presentation/                    # Slide deck and slide assets
├── notebooks/exploratory/           # Non-canonical exploratory notebooks
├── docs/uml/                        # UML-style architecture diagrams
├── paper/                           # Manuscript planning space
└── tests/                           # Regression tests for data/model workflows
```

## Dataset

The current dataset is the QSAR biodegradation dataset stored at:

```text
datasets/qsar_biodegradation_descriptor_benchmark/raw/qsar_biodegradation.csv
```

The curated version is generated at:

```text
datasets/qsar_biodegradation_descriptor_benchmark/processed/qsar_biodegradation_curated.csv
```

The dataset contains 1055 samples, 41 numeric descriptor columns, and a binary biodegradation class target:

- `NRB`: not readily biodegradable
- `RB`: readily biodegradable

Important limitation: this dataset is descriptor-only. It does not include polymer names, molecular structures, SMILES, BigSMILES, Morgan fingerprints, or continuous degradation-rate constants. The folder name intentionally labels it as a descriptor benchmark so it is not confused with future polymer-structure datasets.

Additional structure-aware datasets are stored as separate benchmarks under `datasets/`, including `homopolymer_bigsmiles_tg_benchmark/`, which contains SMILES, BigSMILES, polymer names for the experimental subset, and glass-transition-temperature labels from Choi et al. (2024). That dataset supports polymer representation and property-modeling experiments, but it does not contain biodegradation outcomes.

## How To Run

From the repository root:

```sh
source ./activate-project.sh
python -m pip install -e .
```

Then run the workflow scripts in order:

```sh
python scripts/01_curate_dataset.py
python scripts/02_run_baseline_models.py
python scripts/03_run_neural_network_baseline.py
python scripts/04_run_descriptor_graph_prototype.py
python scripts/05_run_cross_environment_validation.py
python scripts/06_run_stratified_cross_validation.py
python scripts/07_run_feature_engineering_comparison.py
python scripts/08_run_feature_importance_selection.py
python scripts/09_run_uncertainty_reliability_analysis.py
python scripts/10_run_model_reliability_scoreboard.py
```

An optional PyTorch neural-network extension is available separately:

```sh
python -m pip install -r requirements-pytorch.txt
python scripts/11_run_pytorch_neural_network_baseline.py
```

Or regenerate the full project in one command:

```sh
python scripts/generate_all_results.py
```

For a quick pipeline check:

```sh
python scripts/smoke_test_pipeline.py
```

To run the reusable tabular regression template on a separate QSAR/QSPR dataset:

```sh
python scripts/template_run_tabular_regression_baselines.py \
  --csv /path/to/regression_dataset.csv \
  --target numeric_target_column \
  --output results/metadata/regression_baseline_metrics.json
```

## Reproducibility

The project uses deterministic random seeds in the main model workflows, usually `random_state=42`. Generated outputs are organized by artifact type:

- `results/tables/`: model comparison tables, cross-validation results, feature selection outputs, uncertainty metrics, and the final reliability scoreboard.
- `results/predictions/`: prediction-level uncertainty and selective prediction outputs.
- `results/metadata/`: JSON metadata and machine-readable run summaries.
- `figures/`: generated plots for cross-environment validation, feature engineering, feature importance, uncertainty, calibration, final model selection, and curated paper-facing copies.
- `reports/`: human-readable summaries suitable for a research writeup or manuscript draft.
- `source_materials/`: preserved applied-work and outside-reading reports used as research provenance for the literature review and scientific interpretation.

The most important final output is:

```text
results/tables/model_reliability_scoreboard.csv
```

The main narrative summary is:

```text
reports/main_findings.md
reports/model_reliability_report.md
```

## Architecture Diagrams

UML-style Mermaid diagrams are available in `docs/uml/`:

- `project_architecture.mmd`: package/module-level architecture
- `class_diagram.mmd`: major dataclasses and model classes
- `workflow_sequence.mmd`: end-to-end workflow sequence

These diagrams are intended to help future developers and research collaborators understand how data, scripts, source modules, generated outputs, and reports connect.

## Methods Summary

The project currently evaluates:

- Logistic Regression
- Random Forest Classifier
- Feedforward Neural Network
- Optional PyTorch Feedforward Neural Network
- Descriptor-graph neural network prototype

The Feedforward Neural Network is included as a nonlinear dense baseline for tabular QSAR descriptor inputs. It was tested to determine whether a more flexible neural model could learn descriptor interactions that simpler classical models might miss. The main lesson so far is that neural-network complexity alone did not outperform the strongest classical baseline on this descriptor-only dataset. Its value is as a comparison point in the reliability story: it shows that model class matters less than representation quality, feature selection, calibration, and robustness under distribution shift.

Evaluation includes:

- Train/test baseline metrics
- Stratified cross-validation
- SMOTE imbalance comparison
- Proxy cross-environment validation
- Chemistry-aware proxy feature engineering
- Feature importance and reduced feature-set comparison
- Calibration metrics including Brier score, log loss, and expected calibration error
- Prediction-level uncertainty
- Selective prediction accuracy at reduced coverage
- Final reliability-centered model ranking

## Feedforward Neural Network Context

The separate workspace folder `fnn_biodegradability/` contains an earlier downloaded Kaggle notebook focused on feedforward neural-network classification by biodegradability. That notebook is best treated as historical exploration. The reproducible version of that idea is incorporated here through:

```text
scripts/03_run_neural_network_baseline.py
reports/neural_network_baseline_summary.txt
results/metadata/neural_network_baseline_metrics.json
```

In the research narrative, the feedforward neural network helps answer a specific methodological question: does a dense neural model improve biodegradation prediction from tabular descriptors compared with Logistic Regression and Random Forest? The current result is cautious. The neural baseline is valid and sometimes competitive under later feature/reliability analysis, but it is not the final recommended model. That negative or mixed result is useful because it supports the broader conclusion that trustworthy biodegradation prediction depends on reliability-centered evaluation, not simply using a more complex model.

The optional PyTorch baseline extends this idea into a true deep-learning framework implementation:

```text
scripts/11_run_pytorch_neural_network_baseline.py
src/biodegradation_ml_framework/deep_learning.py
reports/pytorch_neural_network_baseline.md
results/metadata/pytorch_neural_network_baseline_metrics.json
results/predictions/pytorch_neural_network_predictions.csv
```

The first PyTorch extension run is documented in `docs/pytorch_extension_run_2026-06-22.md`. This PyTorch path is intentionally not part of the canonical `generate_all_results.py` workflow yet. It should be treated as a next-level extension for comparing framework-based neural training against the existing scikit-learn FNN baseline before deciding whether it belongs in the final reliability scoreboard.

Exploratory notebooks should live in `notebooks/exploratory/`. They are useful for research development, but the canonical, reproducible workflow should remain in `scripts/` and `src/`.

## Tests

Run the test suite with:

```sh
PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py'
```

The tests check dataset loading, curation, model workflow outputs, feature engineering, cross-validation, uncertainty analysis, and final reliability scoreboard construction.

## Developer Notes

This repository was reorganized from an earlier course-style project layout into a research-oriented layout. The old public interface used names such as `firstdataset`, `week10_features.py`, `run_week12_uncertainty_analysis.py`, and root-level files such as `WEEK9_VALIDATION_SUMMARY.txt`. Those names were replaced with scientific workflow names so the repository reads as a reusable biodegradation machine learning framework and QSAR/QSPR evaluation study rather than a weekly assignment archive.

The reorganization was intentionally scoped as Phase 1:

- File, folder, package, script, and output names were cleaned up.
- Generated artifacts were separated into `results/`, `figures/`, and `reports/`.
- The package was renamed to `biodegradation_ml_framework`.
- The README was rewritten for scientific users.
- Model behavior and evaluation logic were preserved unless a change was required by the move.

Phase 2 should focus on deeper maintainability only after the scientific structure is stable. Good next steps would be adding a shared configuration file, reducing duplicated report-writing code, adding a lockfile or environment export, and formalizing dataset citation/license metadata.

### Verification Notes

The full workflow was verified after the reorganization with:

```sh
PYTHONPATH=src MPLBACKEND=Agg python scripts/generate_all_results.py
PYTHONPATH=src MPLBACKEND=Agg python -m unittest discover -s tests -p 'test*.py'
```

At the time of reorganization, the local project `.venv` was tied to a Homebrew Python 3.14 build with a broken `pyexpat`/matplotlib linkage. The code itself compiled and ran successfully in a clean temporary Python 3.13 environment with `numpy`, `pandas`, `scikit-learn`, `imbalanced-learn`, and `matplotlib` installed. Because the code does not require Python 3.14-specific features, `pyproject.toml` now declares `requires-python = ">=3.11"`.

During workflow and test runs, NumPy may emit a correlation warning during descriptor-graph prototype construction if a descriptor column is constant or near-constant. The prototype already handles this with `nan_to_num`; the warning is not currently a test failure.

## Notes For Scientific Use

This repository is suitable as a reusable template for descriptor-based biodegradation or related QSAR/QSPR machine learning studies. Before using it for publication, confirm the dataset citation, decide on a code license, and document the exact software environment used for the final reported results.
