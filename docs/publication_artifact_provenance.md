# Publication Artifact Provenance

This document maps the main paper-facing results to their generating scripts and source artifacts. Use it when checking manuscript claims, presentation figures, or final publication tables.

## Canonical Environment

For publication regeneration, use:

```sh
python3.11 -m venv .venv-publication
source .venv-publication/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-verified.txt
PYTHONPATH=src MPLBACKEND=Agg python scripts/generate_all_results.py
```

The exact verified package set is recorded in `requirements-verified.txt`.

## Primary Workflow Artifacts

| Paper/Report Use | Artifact | Generating Script | Source Inputs | Status |
| --- | --- | --- | --- | --- |
| Dataset summary | `datasets/qsar_biodegradation_descriptor_benchmark/processed/qsar_biodegradation_curated.csv` | `scripts/01_curate_dataset.py` | `datasets/qsar_biodegradation_descriptor_benchmark/raw/qsar_biodegradation.csv` | Canonical |
| Dataset metadata | `datasets/qsar_biodegradation_descriptor_benchmark/metadata/qsar_biodegradation_metadata.json` | `scripts/01_curate_dataset.py` | raw QSAR dataset | Canonical |
| Baseline model comparison | `results/metadata/baseline_model_metrics.json` | `scripts/02_run_baseline_models.py` | curated QSAR features | Canonical |
| Neural-network baseline | `results/metadata/neural_network_baseline_metrics.json` | `scripts/03_run_neural_network_baseline.py` | curated QSAR features | Canonical |
| PyTorch neural-network extension | `results/metadata/pytorch_neural_network_baseline_metrics.json` | `scripts/11_run_pytorch_neural_network_baseline.py` | curated QSAR features | Optional extension; first run documented in `docs/pytorch_extension_run_2026-06-22.md` |
| Descriptor-graph exploratory result | `results/metadata/descriptor_graph_prototype_metrics.json` | `scripts/04_run_descriptor_graph_prototype.py` | curated QSAR features | Exploratory |
| Cross-environment validation | `results/tables/cross_environment_validation_summary.csv` | `scripts/05_run_cross_environment_validation.py` | curated QSAR features | Canonical |
| Stratified CV and SMOTE | `results/tables/stratified_cv_model_results.csv` | `scripts/06_run_stratified_cross_validation.py` | curated QSAR features | Canonical |
| Feature engineering comparison | `results/tables/feature_engineering_model_results.csv` | `scripts/07_run_feature_engineering_comparison.py` | baseline and proxy chemistry features | Canonical |
| Feature-set diagnostics | `results/tables/feature_engineering_diagnostics.csv` | `scripts/07_run_feature_engineering_comparison.py` | baseline and proxy chemistry features | Canonical |
| Feature ranking | `results/tables/feature_importance_rankings.csv` | `scripts/08_run_feature_importance_selection.py` | enhanced feature set | Canonical |
| Reduced feature-set testing | `results/tables/feature_selection_model_results.csv` | `scripts/08_run_feature_importance_selection.py` | feature rankings and selected sets | Canonical |
| Reduced-set environment validation | `results/tables/feature_selection_cross_environment.csv` | `scripts/08_run_feature_importance_selection.py` | selected feature sets | Canonical |
| Calibration and uncertainty metrics | `results/tables/uncertainty_reliability_metrics.csv` | `scripts/09_run_uncertainty_reliability_analysis.py` | selected feature sets and models | Canonical |
| Selective prediction | `results/predictions/selective_prediction_results.csv` | `scripts/09_run_uncertainty_reliability_analysis.py` | prediction-level probabilities | Canonical |
| Prediction-level uncertainty | `results/predictions/prediction_level_uncertainty.csv` | `scripts/09_run_uncertainty_reliability_analysis.py` | selected feature sets and models | Canonical |
| Final reliability scoreboard | `results/tables/model_reliability_scoreboard.csv` | `scripts/10_run_model_reliability_scoreboard.py` | uncertainty, CV, cross-environment, selective metrics | Canonical |
| Final prediction table | `results/predictions/final_model_predictions.csv` | `scripts/10_run_model_reliability_scoreboard.py` | final reliability candidates | Canonical |

## Paper-Facing Figure Set

| Figure | Artifact | Generating Source | What It Supports | Status |
| --- | --- | --- | --- | --- |
| Figure 1 | `figures/paper/figure_1_research_workflow.png` | manually curated from workflow structure | End-to-end project workflow | Curated |
| Figure 2 | `figures/paper/figure_2_feature_importance.png` | copied/curated from `figures/feature_importance/top_feature_importance.png` | Feature relevance and reduced-set rationale | Canonical copy |
| Figure 3 | `figures/paper/figure_3_calibration_curve.png` | copied/curated from `figures/uncertainty_calibration/calibration_curve.png` | Calibration and reliability discussion | Canonical copy |
| Figure 4 | `figures/paper/figure_4_reliability_scoreboard.png` | copied/curated from `figures/model_selection/overall_scoreboard.png` | Final reliability-centered model selection | Canonical copy |

## Generated Figure Directories

| Directory | Generating Script | Purpose |
| --- | --- | --- |
| `figures/cross_environment/` | `scripts/05_run_cross_environment_validation.py` | Generalization under descriptor-space proxy environments |
| `figures/feature_engineering/` | `scripts/07_run_feature_engineering_comparison.py` | Baseline versus proxy chemistry feature sets |
| `figures/feature_importance/` | `scripts/08_run_feature_importance_selection.py` | Feature importance and selected feature-set comparisons |
| `figures/uncertainty_calibration/` | `scripts/09_run_uncertainty_reliability_analysis.py` | Calibration, uncertainty separation, and selective prediction |
| `figures/model_selection/` | `scripts/10_run_model_reliability_scoreboard.py` | Final reliability scoreboard and selection diagnostics |
| `figures/paper/` | curated from generated figures plus workflow image | Paper-ready figure subset |

## Manuscript Tables To Build From Results

| Proposed Table | Source File | Notes |
| --- | --- | --- |
| Dataset summary | `datasets/qsar_biodegradation_descriptor_benchmark/metadata/qsar_biodegradation_metadata.json` | Include samples, descriptors, target labels, limitations |
| Baseline comparison | `results/metadata/baseline_model_metrics.json` | Use only verified metrics from regenerated output |
| Cross-validation metrics | `results/tables/stratified_cv_model_results.csv` | Report mean and variability by model/sampling condition |
| Feature engineering comparison | `results/tables/feature_engineering_model_results.csv` | Compare baseline, proxy, and enhanced feature sets |
| Feature selection comparison | `results/tables/feature_selection_model_results.csv` | Support reduced feature-set selection |
| Calibration/uncertainty metrics | `results/tables/uncertainty_reliability_metrics.csv` | Include Brier score, log loss, ECE, uncertainty gap |
| Final reliability scoreboard | `results/tables/model_reliability_scoreboard.csv` | Use as final model-selection evidence |

## Interpretation Rules

- Treat `results/`, `figures/`, and `reports/` as generated evidence, not as independent claims.
- Every manuscript metric should trace to one source artifact in this file.
- The PyTorch neural-network baseline is optional and should not be reported as a canonical final model until it is run, verified, and integrated into the same reliability evaluation protocol.
- The descriptor-graph prototype should be labeled exploratory because the primary QSAR dataset does not contain molecular graphs, SMILES, or BigSMILES.
- The BigSMILES/Tg benchmark supports polymer representation discussion, but it does not provide biodegradation labels and should not be presented as validating biodegradation prediction.
- Before submission, verify dataset licenses and citations for every dataset used or redistributed.
