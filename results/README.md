# Results

This folder stores generated numeric and machine-readable outputs.

- `tables/`: CSV tables for model metrics, feature rankings, uncertainty metrics, and reliability scores
- `predictions/`: prediction-level outputs and selective prediction results
- `metadata/`: JSON summaries, feature-set definitions, and run metadata

The most important final table is `tables/model_reliability_scoreboard.csv`.

Optional extension outputs from the PyTorch neural baseline are stored in:

- `metadata/pytorch_neural_network_baseline_metrics.json`
- `predictions/pytorch_neural_network_predictions.csv`
