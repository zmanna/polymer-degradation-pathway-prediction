# PyTorch Feedforward Neural-Network Baseline

## Purpose
This optional experiment adds a framework-based dense neural-network baseline using PyTorch. It does not replace the canonical scikit-learn `MLPClassifier` baseline in `scripts/03_run_neural_network_baseline.py`; instead, it provides a next-level implementation for future deep-learning extensions.

## Scope
- Dataset: QSAR biodegradation descriptor benchmark
- Task: binary classification (`NRB` vs `RB`)
- Representation: 41 tabular descriptor features
- Framework: PyTorch
- Loss: weighted binary cross-entropy with logits
- Split: same 80/20 stratified project split pattern, with an internal validation split for early stopping

## Metrics
- accuracy: 0.8436
- precision: 0.7111
- recall: 0.9014
- f1_score: 0.7950
- roc_auc: 0.9201
- best_validation_loss: 0.4590
- epochs_trained: 32.0000

## Confusion Matrix
Rows are true classes `[NRB, RB]`; columns are predicted classes `[NRB, RB]`.
- [114, 26]
- [7, 64]

## Interpretation Notes
This run is intended to test whether a true deep-learning framework implementation changes the neural-network story relative to the existing scikit-learn FNN baseline. It should be interpreted as an optional extension until it is integrated into the reliability scoreboard and cross-validation workflow.

## Outputs
- Metadata: `results/metadata/pytorch_neural_network_baseline_metrics.json`
- Predictions: `results/predictions/pytorch_neural_network_predictions.csv`
- Report: `reports/pytorch_neural_network_baseline.md`
