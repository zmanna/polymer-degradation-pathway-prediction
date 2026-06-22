# Scripts

This folder contains ordered, reproducible workflow scripts.

Run the full workflow with:

```sh
python scripts/generate_all_results.py
```

Or run individual steps:

1. `01_curate_dataset.py`
2. `02_run_baseline_models.py`
3. `03_run_neural_network_baseline.py`
4. `04_run_descriptor_graph_prototype.py`
5. `05_run_cross_environment_validation.py`
6. `06_run_stratified_cross_validation.py`
7. `07_run_feature_engineering_comparison.py`
8. `08_run_feature_importance_selection.py`
9. `09_run_uncertainty_reliability_analysis.py`
10. `10_run_model_reliability_scoreboard.py`

Optional extension:

11. `11_run_pytorch_neural_network_baseline.py`

The PyTorch script is intentionally outside `generate_all_results.py` because it requires an optional deep-learning dependency and is not yet part of the canonical reliability scoreboard.

Scripts should orchestrate workflows. Reusable logic belongs in `src/biodegradation_ml_framework/`.

## Dataset Tools

Additional dataset preparation tools live in `scripts/dataset_tools/`.

- `build_homopolymer_bigsmiles_dataset.py`: downloads and curates the Choi et al. (2024) homopolymer SMILES/BigSMILES Tg benchmark from Figshare. It also exposes an optional single-SMILES conversion command that can call the upstream `BigSMILES_homopolymer` package when that package and RDKit are installed.
