from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from biodegradation_ml_framework.data import (
    CURATED_DATA_PATH,
    DEFAULT_DATA_PATH,
    TARGET_COLUMN,
    build_curated_qsar_dataset,
    load_qsar_biodegradation,
    load_tabular_regression_dataset,
    split_qsar_biodegradation,
    split_tabular_regression_dataset,
)
from biodegradation_ml_framework.models import run_regression_baselines_from_csv
from biodegradation_ml_framework.models import run_qsar_fnn_classifier
from biodegradation_ml_framework.descriptor_graph_model import run_descriptor_graph_prototype
from biodegradation_ml_framework.environment_validation import run_cross_environment_validation
from biodegradation_ml_framework.cross_validation import apply_smote, run_cross_validation
from biodegradation_ml_framework.feature_engineering import build_tier2_proxy_features, build_feature_engineering_bundle, run_feature_engineering_evaluation
from biodegradation_ml_framework.feature_selection import compute_feature_rankings, evaluate_feature_sets
from biodegradation_ml_framework.uncertainty import run_uncertainty
from biodegradation_ml_framework.reliability_scoreboard import build_model_reliability_scoreboard
from biodegradation_ml_framework.deep_learning import is_torch_available, run_qsar_pytorch_fnn_classifier


class QSARDataTests(unittest.TestCase):
    def test_default_dataset_path_exists(self) -> None:
        self.assertTrue(Path(DEFAULT_DATA_PATH).exists())

    def test_load_qsar_biodegradation_shapes(self) -> None:
        bundle = load_qsar_biodegradation()
        self.assertEqual(bundle.frame.shape, (1055, 42))
        self.assertEqual(bundle.X.shape, (1055, 41))
        self.assertEqual(bundle.y.shape, (1055,))
        self.assertNotIn(TARGET_COLUMN, bundle.X.columns)
        self.assertEqual(set(bundle.y.astype(str).unique()), {"NRB", "RB"})

    def test_split_qsar_biodegradation_is_stratified(self) -> None:
        split = split_qsar_biodegradation(test_size=0.2, random_state=7)
        self.assertEqual(split.X_train.shape, (844, 41))
        self.assertEqual(split.X_test.shape, (211, 41))
        self.assertEqual(set(split.y_train.astype(str).unique()), {"NRB", "RB"})
        self.assertEqual(set(split.y_test.astype(str).unique()), {"NRB", "RB"})

    def test_build_curated_qsar_dataset(self) -> None:
        curated = build_curated_qsar_dataset(output_path=CURATED_DATA_PATH)
        self.assertEqual(curated.shape, (1055, 45))
        self.assertEqual(curated.columns[0], "sample_id")
        self.assertEqual(curated.iloc[0]["sample_id"], "qsar_00001")
        self.assertIn("SpMax_L", curated.columns)
        self.assertIn("nX", curated.columns)
        self.assertIn("biodegradation_class_id", curated.columns)
        self.assertIn("biodegradation_outcome", curated.columns)

    def test_generic_regression_pipeline(self) -> None:
        rng = np.random.default_rng(42)
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "synthetic_regression.csv"
            frame = pd.DataFrame(
                {
                    "f1": rng.normal(size=120),
                    "f2": rng.normal(size=120),
                    "f3": rng.normal(size=120),
                }
            )
            frame["target"] = 3.0 * frame["f1"] - 1.5 * frame["f2"] + 0.5 * frame["f3"]
            frame.to_csv(csv_path, index=False)

            bundle = load_tabular_regression_dataset(csv_path, target_column="target")
            self.assertEqual(bundle.X.shape, (120, 3))
            self.assertEqual(bundle.target_column, "target")

            split = split_tabular_regression_dataset(csv_path, target_column="target")
            self.assertEqual(split.X_train.shape[1], 3)

            results = run_regression_baselines_from_csv(str(csv_path), target_column="target")
            metric_names = {metric for result in results for metric in result.metrics}
            self.assertEqual(metric_names, {"mae", "rmse", "r2"})
            self.assertEqual(len(results), 2)

    def test_qsar_fnn_classifier(self) -> None:
        result = run_qsar_fnn_classifier(random_state=42)
        self.assertEqual(result.model_name, "feedforward_neural_network")
        self.assertEqual(set(result.metrics), {"accuracy", "precision", "recall", "f1_score", "roc_auc"})
        self.assertEqual(len(result.confusion_matrix), 2)
        self.assertEqual(len(result.confusion_matrix[0]), 2)

    @unittest.skipUnless(is_torch_available(), "PyTorch optional dependency is not installed")
    def test_qsar_pytorch_fnn_classifier(self) -> None:
        result = run_qsar_pytorch_fnn_classifier(random_state=42, max_epochs=5, patience=2)
        self.assertEqual(result.model_name, "pytorch_feedforward_neural_network")
        self.assertIn("accuracy", result.metrics)
        self.assertIn("roc_auc", result.metrics)
        self.assertEqual(len(result.confusion_matrix), 2)
        self.assertEqual(len(result.test_probabilities), len(result.test_labels))

    def test_descriptor_graph_prototype(self) -> None:
        result = run_descriptor_graph_prototype(random_state=42)
        self.assertEqual(result.model_name, "descriptor_graph_neural_network_prototype")
        self.assertEqual(set(result.metrics), {"accuracy", "precision", "recall", "f1_score", "roc_auc", "rb_recall"})
        self.assertEqual(result.graph_info["num_nodes"], 41)
        self.assertEqual(len(result.confusion_matrix), 2)

    def test_cross_environment_validation(self) -> None:
        results, summary = run_cross_environment_validation(random_state=42)
        self.assertEqual(len(results), 12)
        self.assertEqual(summary.shape[0], 12)
        self.assertIn("model_name", summary.columns)
        self.assertIn("rb_recall", summary.columns)

    def test_apply_smote_balances_training_data(self) -> None:
        X = np.array([[0.0], [1.0], [2.0], [10.0], [11.0], [12.0]], dtype=float)
        y = np.array([0, 0, 0, 1, 1, 1], dtype=int)
        X_res, y_res = apply_smote(X, y, random_state=42)
        self.assertEqual(X_res.shape[0], 6)
        self.assertEqual(np.bincount(y_res).tolist(), [3, 3])

    def test_cross_validation_shapes(self) -> None:
        diagnostics, results = run_cross_validation(random_state=42)
        self.assertEqual(diagnostics.shape[0], 5)
        self.assertEqual(results.shape[0], 30)
        self.assertIn("sampling", results.columns)
        self.assertIn("rb_recall", results.columns)

    def test_proxy_feature_building(self) -> None:
        bundle = build_feature_engineering_bundle()
        proxy = build_tier2_proxy_features(bundle.baseline_X)
        self.assertEqual(proxy.shape[1], 12)
        self.assertEqual(bundle.enhanced_X.shape[1], bundle.baseline_X.shape[1] + 12)

    def test_feature_engineering_evaluation_shapes(self) -> None:
        diagnostics, results = run_feature_engineering_evaluation(random_state=42)
        self.assertEqual(diagnostics.shape[0], 10)
        self.assertEqual(results.shape[0], 60)
        self.assertIn("feature_set", results.columns)

    def test_feature_rankings(self) -> None:
        ranking = compute_feature_rankings(random_state=42)
        self.assertIn("feature_name", ranking.columns)
        self.assertIn("combined_rank", ranking.columns)
        self.assertGreaterEqual(ranking.shape[0], 53)

    def test_feature_selection_evaluation_shapes(self) -> None:
        diagnostics, results, generalization, feature_sets = evaluate_feature_sets(random_state=42)
        self.assertEqual(diagnostics["feature_set"].nunique(), 4)
        self.assertEqual(results["feature_set"].nunique(), 4)
        self.assertEqual(generalization.shape[0], 4)
        self.assertGreaterEqual(len(feature_sets.top_ranked), 10)

    def test_uncertainty_outputs(self) -> None:
        predictions, metrics, selective, cross_env = run_uncertainty(
            random_state=42,
            model_names=("random_forest_classifier",),
        )
        self.assertEqual(predictions["feature_set"].nunique(), 4)
        self.assertEqual(metrics["feature_set"].nunique(), 4)
        self.assertIn("brier_score", metrics.columns)
        self.assertIn("ece", metrics.columns)
        self.assertIn("coverage", selective.columns)
        self.assertTrue((cross_env["evaluation_type"] == "cross_environment").all())

    def test_model_reliability_scoreboard_outputs(self) -> None:
        predictions, metrics, selective, scoreboard = build_model_reliability_scoreboard(
            random_state=42,
            model_names=("random_forest_classifier",),
        )
        self.assertEqual(scoreboard.shape[0], 4)
        self.assertEqual(scoreboard["feature_set"].nunique(), 4)
        self.assertIn("overall_reliability_score", scoreboard.columns)
        self.assertIn("candidate", scoreboard.columns)
        self.assertTrue(((scoreboard["selective_accuracy_25"] >= 0.0) & (scoreboard["selective_accuracy_25"] <= 1.0)).all())
        self.assertTrue((scoreboard["overall_rank"] >= 1).all())


if __name__ == "__main__":
    unittest.main()
