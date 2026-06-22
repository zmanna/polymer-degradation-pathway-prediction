# PolyDegradeML Repository Map

This document explains what lives where and which files are source code, generated outputs, research reports, raw data, or exploratory material.

## Root Files

- `README.md`: main project overview for scientific users.
- `CODEBASE_AUDIT.md`: health check, stability review, and recommended next steps.
- `RUNBOOK.md`: operational instructions for installing, running, and troubleshooting.
- `REPOSITORY_MAP.md`: this folder and major-file map.
- `pyproject.toml`: package metadata and runtime dependencies.
- `requirements.txt`: duplicate runtime dependency list for simple installs.
- `requirements-verified.txt`: exact tested package set for publication-oriented regeneration.
- `requirements-pytorch.txt`: optional PyTorch dependency set for the framework-based neural baseline.
- `activate-project.sh`: local activation helper for `.venv`, `PYTHONPATH`, and Kaggle config.
- `CITATION.cff`: citation metadata for the repository.
- `LICENSE`: repository license.
- `.gitignore`: local cache, environment, credential, and generated-example ignore rules.

## `src/biodegradation_ml_framework/`

Reusable source package for the scientific workflow.

- `data.py`: dataset paths, descriptor-column naming, loading, curation, and train/test splitting.
- `models.py`: Logistic Regression, Random Forest, feedforward neural-network classifier, and reusable tabular regression baselines.
- `cross_validation.py`: stratified cross-validation, SMOTE sampling, and fold-level diagnostics.
- `environment_validation.py`: proxy cross-environment validation using descriptor-space clustering.
- `descriptor_graph_model.py`: exploratory descriptor-graph prototype adapted to descriptor-only data.
- `feature_engineering.py`: baseline descriptors, chemistry-informed proxy features, and feature-set comparison.
- `feature_selection.py`: Random Forest importance, permutation importance, mutual information, and reduced feature-set evaluation.
- `uncertainty.py`: calibration, Brier/log-loss metrics, expected calibration error, uncertainty, and selective prediction.
- `reliability_scoreboard.py`: final reliability-centered candidate ranking and model-selection figures.
- `deep_learning.py`: optional PyTorch dense neural-network baseline for tabular QSAR descriptors.
- `__init__.py`: package marker.
- `README.md`: package-level navigation notes.

Classification: source code.

## `scripts/`

Executable workflow scripts. These are the main entry points for reproducing project artifacts.

- `01_curate_dataset.py`: builds curated QSAR dataset and metadata report.
- `02_run_baseline_models.py`: runs Logistic Regression and Random Forest baselines.
- `03_run_neural_network_baseline.py`: runs feedforward neural-network baseline and comparison report.
- `04_run_descriptor_graph_prototype.py`: runs exploratory descriptor-graph prototype.
- `05_run_cross_environment_validation.py`: runs proxy environment validation and figures.
- `06_run_stratified_cross_validation.py`: runs stratified cross-validation and SMOTE comparison.
- `07_run_feature_engineering_comparison.py`: compares baseline descriptors with proxy chemistry features.
- `08_run_feature_importance_selection.py`: ranks features and evaluates reduced sets.
- `09_run_uncertainty_reliability_analysis.py`: generates calibration, uncertainty, selective prediction, and cross-environment reliability artifacts.
- `10_run_model_reliability_scoreboard.py`: generates final model-selection scoreboard, report, and figures.
- `11_run_pytorch_neural_network_baseline.py`: optional PyTorch dense neural-network baseline; not part of `generate_all_results.py`.
- `generate_all_results.py`: orchestrates scripts `01` through `10`.
- `smoke_test_pipeline.py`: quick Random Forest pipeline sanity check.
- `template_run_tabular_regression_baselines.py`: reusable template for numeric QSAR/QSPR regression datasets.
- `dataset_tools/build_homopolymer_bigsmiles_dataset.py`: downloads/curates the homopolymer BigSMILES/Tg benchmark and provides optional SMILES-to-BigSMILES helper behavior.
- `README.md`: script navigation notes.

Classification: executable source code and workflow entry points.

## `datasets/`

Dataset-specific storage. Each dataset folder uses `raw/`, `processed/`, and `metadata/` where applicable.

### `datasets/qsar_biodegradation_descriptor_benchmark/`

Primary biodegradation classification dataset.

- `raw/qsar_biodegradation.csv`: raw descriptor-only QSAR biodegradation data.
- `processed/qsar_biodegradation_curated.csv`: generated curated dataset with stable column names and labels.
- `metadata/qsar_biodegradation_metadata.json`: generated curation metadata.
- README files: dataset explanation and navigation.

Classification: raw data, generated processed data, generated metadata.

### `datasets/homopolymer_bigsmiles_tg_benchmark/`

Structure-aware polymer property dataset for BigSMILES and glass-transition-temperature representation work.

- `raw/with_Tg.zip`: downloaded source archive.
- `raw/with_Tg/Bicerano_bigsmiles.csv`: raw extracted experimental subset.
- `raw/with_Tg/JCIM_sup_bigsmiles.csv`: raw extracted supplementary subset.
- `processed/homopolymer_bigsmiles_tg_curated.csv`: generated curated BigSMILES/Tg table.
- `metadata/source_manifest.json`: generated provenance and curation summary.

Classification: raw data, generated processed data, generated metadata. This is not a biodegradation-label dataset.

### `datasets/big_molecules_smiles_activity_benchmark/`

Large SMILES/activity benchmark downloaded from Kaggle for structure-representation exploration.

- `raw/SMILES_Big_Data_Set.csv`: raw source file.
- `processed/big_molecules_smiles_activity_curated.csv`: curated copy.
- `metadata/source_manifest.json`: source metadata.

Classification: raw data, processed data, metadata. Publication/license status should be verified before formal use.

### `datasets/bigsmiles_common_repeat_units_reference/`

Reference/schema area for future curated polymer repeat-unit examples.

- `processed/bigsmiles_common_repeat_units_schema.csv`: schema/reference table.
- `metadata/source_manifest.json`: metadata.

Classification: reference data and metadata.

### `datasets/polymer_structure_dataset_sources.md`

Notes on possible structure-aware polymer dataset sources.

Classification: research notes.

## `results/`

Machine-readable generated outputs.

- `results/tables/`: generated CSV result tables.
- `results/metadata/`: generated JSON metrics and run metadata.
- `results/predictions/`: generated prediction-level outputs.
- README files: folder-level navigation.

Important canonical files:

- `results/tables/model_reliability_scoreboard.csv`
- `results/tables/final_uncertainty_metrics.csv`
- `results/predictions/final_model_predictions.csv`
- `results/metadata/feature_selection_sets.json`

Classification: generated outputs. Preserve for reproducible reporting, but regenerate when finalizing publication results.

## `figures/`

Generated and curated visual outputs.

- `figures/branding/`: banner and identity assets.
- `figures/cross_environment/`: proxy environment validation plots.
- `figures/feature_engineering/`: feature-set comparison plots.
- `figures/feature_importance/`: feature ranking and reduced-set plots.
- `figures/uncertainty_calibration/`: calibration, uncertainty, and selective prediction plots.
- `figures/model_selection/`: final reliability scoreboard plots.
- `figures/paper/`: curated paper-facing copies of key figures.

Classification: generated figures and curated presentation/publication assets.

## `reports/`

Human-readable generated summaries.

- `dataset_curation.md`: dataset curation and representation notes.
- `baseline_modeling.md`: train/test baseline report.
- `neural_network_baseline_summary.txt`: FNN baseline interpretation.
- `descriptor_graph_prototype_summary.txt`: descriptor-graph exploratory result summary.
- `cross_environment_validation.md`: proxy environment validation report.
- `stratified_cross_validation_summary.txt`: cross-validation and SMOTE summary.
- `feature_engineering_summary.txt`: feature-engineering comparison summary.
- `feature_importance_selection_summary.txt`: feature ranking and reduced-set summary.
- `uncertainty_reliability_summary.txt`: uncertainty and selective prediction summary.
- `model_reliability_report.md`: final reliability-centered model-selection report.
- `model_reliability_summary.txt`: compact final model-selection summary.
- `main_findings.md`: high-level research findings.
- `archive/`: preserved earlier weekly/generated report snapshots.

Classification: generated reports and archived research provenance.

Potentially stale/experimental:

- Files in `reports/archive/` reflect earlier project stages. They are useful provenance but should not be treated as final paper outputs without verification.

## `paper/`

Manuscript workspace.

- `manuscript_draft.md`: scientific manuscript draft.
- `PolyDegradeML_consolidated_manuscript.docx`: Word export for review/submission workflows.
- `evidence_mapped_outline.md`: outline mapped to repository evidence.
- `tables_and_figures_plan.md`: proposed paper table/figure plan.
- `publication_readiness_checklist.md`: checklist for publication review.
- `missing_information_to_ask_author.md`: unresolved information requests.
- `build_consolidated_docx.py`: document generation utility.
- `README.md`: paper folder navigation.

Classification: manuscript source, generated document artifact, publication planning.

## `presentation/`

Slide and communication workspace.

- `PolyDegradeML_comprehensive_defense.pptx`: comprehensive conference/thesis-style deck.
- `PolyDegradeML_comprehensive_defense_speaker_notes.md`: speaker notes.
- `PolyDegradeML_academic_ted_talk.pptx`: academic/TED-style deck.
- `PolyDegradeML_academic_ted_talk_speaker_notes.md`: speaker notes.
- `Plastic_Degradation_Project_Presentation.pptx`: earlier/project deck.
- `PROJECT_SLIDES.md`: markdown slide source/notes.
- `SLIDE_ASSET_GUIDE.md`: asset usage guide.
- `build_*.mjs` and `build_project_slides.py`: slide-building utilities.
- `assets/`: presentation-ready figure copies.

Classification: presentation source, generated decks, and visual assets.

## `source_materials/`

Preserved original Applied Work and Outside Reading reports.

- `source_materials/reports/Week_01_Applied_Work.docx` through Week 13 reports.
- Outside Reading report files for literature-review and interpretation provenance.
- `README.md`: source-material notes.

Classification: research provenance and literature/source material. These are not generated by the workflow scripts.

## `docs/`

Developer and architecture documentation.

- `docs/uml/project_architecture.mmd`: architecture diagram.
- `docs/uml/class_diagram.mmd`: major classes/dataclasses.
- `docs/uml/workflow_sequence.mmd`: workflow sequence.
- `docs/publication_artifact_provenance.md`: maps manuscript figures/tables to scripts and source outputs.
- `docs/publication_run_2026-05-28.md`: records the stabilized publication-run command, environment, and observed output changes.
- `docs/pytorch_extension_run_2026-06-22.md`: records the first optional PyTorch neural-network extension run.
- README files: navigation.

Classification: documentation.

## `notebooks/`

Exploratory notebook area.

- `notebooks/exploratory/README.md`: explains that exploratory notebooks are non-canonical.

Classification: exploratory workspace. Canonical reproducible work should remain in `scripts/` and `src/`.

## `tests/`

Test suite.

- `tests/test_data.py`: unit/regression tests for data loading, curation, model workflows, feature engineering, uncertainty, and reliability scoreboard.
- `tests/README.md`: test navigation.

Classification: test source code.

## Likely Obsolete, Local, or Generated Scratch Files

- `synthetic_regression_example.csv`: local generated example output, ignored by Git.
- `regression_scores_example.json`: local generated example output, ignored by Git.
- `.kaggle/access_token`: local credential/config file, ignored by Git. Do not commit.
- `__pycache__/`: Python bytecode cache directories. Removed during the health pass and ignored by Git.

Do not delete reports, paper files, presentations, datasets, or figures without explicit approval.
