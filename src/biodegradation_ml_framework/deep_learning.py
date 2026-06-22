from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .data import split_qsar_biodegradation


@dataclass(frozen=True)
class PyTorchClassificationResult:
    model_name: str
    metrics: dict[str, float]
    confusion_matrix: list[list[int]]
    training_config: dict[str, int | float | str | list[int]]
    training_history: list[dict[str, float]]
    test_labels: list[int]
    test_predictions: list[int]
    test_probabilities: list[float]


def is_torch_available() -> bool:
    try:
        import torch  # noqa: F401
    except ImportError:
        return False
    return True


def _require_torch() -> tuple[Any, Any]:
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise ImportError(
            "PyTorch is required for this optional baseline. Install it with "
            "`python -m pip install -r requirements-pytorch.txt`."
        ) from exc
    return torch, nn


def _set_torch_reproducibility(torch: Any, random_state: int) -> None:
    random.seed(random_state)
    np.random.seed(random_state)
    torch.manual_seed(random_state)
    if hasattr(torch, "use_deterministic_algorithms"):
        torch.use_deterministic_algorithms(True, warn_only=True)


def run_qsar_pytorch_fnn_classifier(
    *,
    random_state: int = 42,
    hidden_layer_sizes: tuple[int, ...] = (128, 64, 32),
    learning_rate: float = 1e-3,
    weight_decay: float = 1e-4,
    batch_size: int = 32,
    max_epochs: int = 250,
    patience: int = 25,
    validation_fraction: float = 0.1,
) -> PyTorchClassificationResult:
    """Train an optional PyTorch dense neural baseline on tabular QSAR descriptors."""
    torch, nn = _require_torch()
    _set_torch_reproducibility(torch, random_state)

    split = split_qsar_biodegradation(random_state=random_state, target_as_category=False)
    y_train_full = (split.y_train.to_numpy(dtype=np.int64) == 2).astype(np.float32)
    y_test = (split.y_test.to_numpy(dtype=np.int64) == 2).astype(np.int64)

    scaler = StandardScaler()
    X_train_full = scaler.fit_transform(split.X_train).astype(np.float32)
    X_test = scaler.transform(split.X_test).astype(np.float32)

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full,
        y_train_full,
        test_size=validation_fraction,
        random_state=random_state,
        stratify=y_train_full.astype(np.int64),
    )

    layers: list[Any] = []
    input_size = X_train.shape[1]
    for hidden_size in hidden_layer_sizes:
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(p=0.15))
        input_size = hidden_size
    layers.append(nn.Linear(input_size, 1))
    model = nn.Sequential(*layers)

    negative_count = float((y_train == 0).sum())
    positive_count = float((y_train == 1).sum())
    pos_weight = negative_count / max(positive_count, 1.0)

    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight], dtype=torch.float32))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    y_val_tensor = torch.tensor(y_val.reshape(-1, 1), dtype=torch.float32)

    history: list[dict[str, float]] = []
    best_state: dict[str, Any] | None = None
    best_val_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(1, max_epochs + 1):
        model.train()
        permutation = torch.randperm(X_train_tensor.shape[0])
        batch_losses: list[float] = []
        for start in range(0, X_train_tensor.shape[0], batch_size):
            indices = permutation[start : start + batch_size]
            batch_X = X_train_tensor[indices]
            batch_y = y_train_tensor[indices]

            optimizer.zero_grad()
            logits = model(batch_X)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            batch_losses.append(float(loss.detach().item()))

        model.eval()
        with torch.no_grad():
            val_logits = model(X_val_tensor)
            val_loss = float(criterion(val_logits, y_val_tensor).item())
            val_probabilities = torch.sigmoid(val_logits).numpy().reshape(-1)
            val_predictions = (val_probabilities >= 0.5).astype(np.int64)
            val_accuracy = float(accuracy_score(y_val.astype(np.int64), val_predictions))

        train_loss = float(np.mean(batch_losses))
        history.append(
            {
                "epoch": float(epoch),
                "train_loss": train_loss,
                "validation_loss": val_loss,
                "validation_accuracy": val_accuracy,
            }
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {key: value.detach().clone() for key, value in model.state_dict().items()}
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= patience:
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    model.eval()
    with torch.no_grad():
        test_logits = model(X_test_tensor)
        probabilities = torch.sigmoid(test_logits).numpy().reshape(-1)

    predictions = (probabilities >= 0.5).astype(np.int64)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, pos_label=1, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, pos_label=1, zero_division=0)),
        "f1_score": float(f1_score(y_test, predictions, pos_label=1, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "best_validation_loss": float(best_val_loss),
        "epochs_trained": float(len(history)),
    }
    matrix = confusion_matrix(y_test, predictions, labels=[0, 1]).tolist()
    return PyTorchClassificationResult(
        model_name="pytorch_feedforward_neural_network",
        metrics=metrics,
        confusion_matrix=matrix,
        training_config={
            "random_state": random_state,
            "hidden_layer_sizes": list(hidden_layer_sizes),
            "learning_rate": learning_rate,
            "weight_decay": weight_decay,
            "batch_size": batch_size,
            "max_epochs": max_epochs,
            "patience": patience,
            "validation_fraction": validation_fraction,
            "loss": "BCEWithLogitsLoss",
            "class_imbalance_handling": "positive_class_weight",
        },
        training_history=history,
        test_labels=y_test.astype(int).tolist(),
        test_predictions=predictions.astype(int).tolist(),
        test_probabilities=probabilities.astype(float).tolist(),
    )
