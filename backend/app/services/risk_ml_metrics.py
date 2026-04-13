"""
Hold-out evaluation of the ML risk classifier against rule-based labels on synthetic data.

Used for demos and regression checks; does not touch the production DB.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np

from backend.app.services import risk_ml
from backend.app.services.risk_scoring import calculate_risk


def _build_synthetic_xy(
    n_samples: int, random_state: int
) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.RandomState(random_state)
    X_list: list[np.ndarray] = []
    y_labels: list[str] = []

    for _ in range(n_samples):
        n_answers = int(rng.randint(1, 9))
        raw = rng.uniform(0.0, 5.0, size=n_answers).tolist()
        rule = calculate_risk(raw)
        X_list.append(risk_ml.feature_vector(raw))
        y_labels.append(rule.risk_level)

    return np.vstack(X_list), np.asarray(y_labels)


def evaluate_synthetic_holdout(
    n_samples: int = 4000,
    test_size: float = 0.2,
    random_state: int = 7,
) -> Dict[str, Any]:
    """
    Train a fresh LogisticRegression on a random train split and report
    accuracy / F1 vs rule-based risk_level on the held-out test split.
    """
    if not risk_ml.is_available():
        raise RuntimeError("scikit-learn is not installed")

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    X, y_str = _build_synthetic_xy(n_samples, random_state)

    try:
        X_train, X_test, y_train_str, y_test_str = train_test_split(
            X,
            y_str,
            test_size=test_size,
            random_state=random_state,
            stratify=y_str,
        )
    except ValueError:
        X_train, X_test, y_train_str, y_test_str = train_test_split(
            X,
            y_str,
            test_size=test_size,
            random_state=random_state,
        )

    le = LabelEncoder()
    y_train = le.fit_transform(y_train_str)
    y_test = le.transform(y_test_str)

    clf = LogisticRegression(max_iter=2000, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    labels: List[str] = [str(c) for c in le.classes_]
    p, r, f1, sup = precision_recall_fscore_support(
        y_test, y_pred, labels=list(range(len(labels))), zero_division=0
    )
    per_class: Dict[str, Dict[str, float | int]] = {}
    for i, name in enumerate(labels):
        per_class[name] = {
            "precision": float(p[i]),
            "recall": float(r[i]),
            "f1": float(f1[i]),
            "support": int(sup[i]),
        }

    return {
        "n_total": int(n_samples),
        "n_train": int(X_train.shape[0]),
        "n_test": int(X_test.shape[0]),
        "test_size": float(test_size),
        "random_state": int(random_state),
        "accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "per_class": per_class,
    }
