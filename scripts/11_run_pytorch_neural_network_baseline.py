from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from biodegradation_ml_framework.deep_learning import run_qsar_pytorch_fnn_classifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
RESULTS_METADATA_DIR = PROJECT_ROOT / "results" / "metadata"
RESULTS_PREDICTIONS_DIR = PROJECT_ROOT / "results" / "predictions"
JSON_PATH = RESULTS_METADATA_DIR / "pytorch_neural_network_baseline_metrics.json"
PREDICTIONS_PATH = RESULTS_PREDICTIONS_DIR / "pytorch_neural_network_predictions.csv"
REPORT_PATH = REPORTS_DIR / "pytorch_neural_network_baseline.md"


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_METADATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        result = run_qsar_pytorch_fnn_classifier()
    except ImportError as exc:
        raise SystemExit(str(exc)) from exc

    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": "qsar_biodegradation",
        "task_type": "classification",
        "framework": "PyTorch",
        "model": {
            "model_name": result.model_name,
            "metrics": result.metrics,
            "confusion_matrix_labels": ["NRB", "RB"],
            "confusion_matrix": result.confusion_matrix,
            "training_config": result.training_config,
            "training_history": result.training_history,
        },
        "output_files": {
            "metadata": str(JSON_PATH.relative_to(PROJECT_ROOT)),
            "predictions": str(PREDICTIONS_PATH.relative_to(PROJECT_ROOT)),
            "report": str(REPORT_PATH.relative_to(PROJECT_ROOT)),
        },
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n")

    predictions = pd.DataFrame(
        {
            "true_label": result.test_labels,
            "predicted_label": result.test_predictions,
            "predicted_probability_rb": result.test_probabilities,
        }
    )
    predictions["true_class"] = predictions["true_label"].map({0: "NRB", 1: "RB"})
    predictions["predicted_class"] = predictions["predicted_label"].map({0: "NRB", 1: "RB"})
    predictions.to_csv(PREDICTIONS_PATH, index=False)

    lines = [
        "# PyTorch Feedforward Neural-Network Baseline",
        "",
        "## Purpose",
        "This optional experiment adds a framework-based dense neural-network baseline using PyTorch. It does not replace the canonical scikit-learn `MLPClassifier` baseline in `scripts/03_run_neural_network_baseline.py`; instead, it provides a next-level implementation for future deep-learning extensions.",
        "",
        "## Scope",
        "- Dataset: QSAR biodegradation descriptor benchmark",
        "- Task: binary classification (`NRB` vs `RB`)",
        "- Representation: 41 tabular descriptor features",
        "- Framework: PyTorch",
        "- Loss: weighted binary cross-entropy with logits",
        "- Split: same 80/20 stratified project split pattern, with an internal validation split for early stopping",
        "",
        "## Metrics",
    ]
    for metric_name, value in result.metrics.items():
        lines.append(f"- {metric_name}: {value:.4f}")
    lines.extend(
        [
            "",
            "## Confusion Matrix",
            "Rows are true classes `[NRB, RB]`; columns are predicted classes `[NRB, RB]`.",
        ]
    )
    for row in result.confusion_matrix:
        lines.append(f"- {row}")
    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "This run is intended to test whether a true deep-learning framework implementation changes the neural-network story relative to the existing scikit-learn FNN baseline. It should be interpreted as an optional extension until it is integrated into the reliability scoreboard and cross-validation workflow.",
            "",
            "## Outputs",
            f"- Metadata: `{JSON_PATH.relative_to(PROJECT_ROOT)}`",
            f"- Predictions: `{PREDICTIONS_PATH.relative_to(PROJECT_ROOT)}`",
            f"- Report: `{REPORT_PATH.relative_to(PROJECT_ROOT)}`",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n")

    print(f"Wrote PyTorch neural network metadata to {JSON_PATH}")
    print(f"Wrote PyTorch neural network predictions to {PREDICTIONS_PATH}")
    print(f"Wrote PyTorch neural network report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
