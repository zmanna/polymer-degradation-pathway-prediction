# PyTorch Extension Run: 2026-06-22

This file records the first framework-based neural-network extension run for PolyDegradeML.

## Purpose

The existing feedforward neural-network baseline uses scikit-learn's `MLPClassifier`. This extension adds a true PyTorch implementation so future work can test deeper neural training workflows, custom losses, representation learning, and eventually graph or hybrid architectures without replacing the stable canonical pipeline.

## Command

```sh
PYTHONPATH=/tmp/polydegrade_health_deps:src \
  /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 \
  scripts/11_run_pytorch_neural_network_baseline.py
```

For normal reuse, install the optional dependency file:

```sh
python -m pip install -r requirements-pytorch.txt
PYTHONPATH=src python scripts/11_run_pytorch_neural_network_baseline.py
```

## Framework Versions Used

```text
Python 3.11
torch==2.12.1
numpy==2.3.5
pandas==2.3.3
scikit-learn==1.7.2
```

## Output Files

- `results/metadata/pytorch_neural_network_baseline_metrics.json`
- `results/predictions/pytorch_neural_network_predictions.csv`
- `reports/pytorch_neural_network_baseline.md`

## Model Configuration

- Model type: dense feedforward neural network
- Input representation: 41 numeric QSAR descriptor features
- Hidden layers: `[128, 64, 32]`
- Activation: ReLU
- Dropout: `0.15`
- Loss: `BCEWithLogitsLoss`
- Class imbalance handling: positive-class weighting
- Optimizer: Adam
- Learning rate: `0.001`
- Weight decay: `0.0001`
- Batch size: `32`
- Maximum epochs: `250`
- Early-stopping patience: `25`
- Internal validation fraction: `0.1`
- Random state: `42`

## Held-Out Test Metrics

```text
accuracy: 0.8436018957345972
precision: 0.7111111111111111
recall: 0.9014084507042254
f1_score: 0.7950310559006211
roc_auc: 0.9201207243460765
best_validation_loss: 0.45899805426597595
epochs_trained: 32
```

Confusion matrix rows are true classes `[NRB, RB]`; columns are predicted classes `[NRB, RB]`:

```text
[114, 26]
[7, 64]
```

## Interpretation

This run is scientifically useful because it changes the neural-network comparison from "scikit-learn MLP only" to "framework-based neural training is available and testable." The PyTorch model produced high RB recall on the held-out split, suggesting that class-weighted neural training may be useful when the scientific goal prioritizes identifying readily biodegradable cases.

This result should still be treated as an optional extension, not a final model-selection claim. It has not yet been evaluated through the full reliability pipeline: cross-validation, SMOTE comparison, calibration, uncertainty, selective prediction, and cross-environment validation.

## Next Integration Step

Before using the PyTorch result in the manuscript as a major finding, integrate it into the same reliability-aware evaluation protocol used by the classical models:

- stratified cross-validation
- calibration metrics
- uncertainty separation
- selective prediction
- cross-environment validation
- final reliability scoreboard comparison

## Verification

The full test suite passed with PyTorch installed in the verification sandbox:

```text
Ran 17 tests in 153.003s
OK
```
