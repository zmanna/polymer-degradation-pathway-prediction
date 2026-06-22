# biodegradation_ml_framework

Reusable Python package for PolyDegradeML.

Main modules:

- `data.py`: dataset loading, splitting, and curation
- `models.py`: baseline classification and regression model helpers
- `cross_validation.py`: stratified cross-validation and SMOTE comparison
- `environment_validation.py`: proxy cross-environment validation
- `feature_engineering.py`: chemistry-informed proxy features
- `feature_selection.py`: feature importance and selected feature sets
- `uncertainty.py`: calibration, uncertainty, and selective prediction
- `reliability_scoreboard.py`: final reliability-centered model comparison
- `descriptor_graph_model.py`: descriptor-graph prototype model
- `deep_learning.py`: optional PyTorch feedforward neural-network baseline

The package initializer is intentionally lightweight; import from specific modules when possible.

For a visual overview of these modules, see `docs/uml/project_architecture.mmd` and `docs/uml/class_diagram.mmd`.
