"""
Simple ML-based risk classifier (LogisticRegression) trained on synthetic data.

Labels are generated from the existing rule-based scorer so behaviour stays aligned
with the MVP logic while satisfying a "simple ML classifier" requirement.

Enable with USE_ML_RISK_SCORING=true in the environment.
"""

from __future__ import annotations

from typing import List

import numpy as np

from backend.app.services.risk_scoring import RiskScoreResult, calculate_risk

_clf = None
_label_encoder = None
_SKLEARN_OK = False

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder

    _SKLEARN_OK = True
except ImportError:
    LogisticRegression = None  # type: ignore[misc, assignment]
    LabelEncoder = None  # type: ignore[misc, assignment]


def is_available() -> bool:
    return _SKLEARN_OK


def feature_vector(values: List[float]) -> np.ndarray:
    if not values:
        return np.zeros(5, dtype=np.float64)
    arr = np.clip(np.asarray(values, dtype=np.float64), 0.0, 5.0)
    spread = float(arr.max() - arr.min())
    return np.array(
        [
            float(arr.mean()),
            float(arr.max()),
            float(arr.min()),
            spread,
            min(len(arr) / 10.0, 1.0),
        ],
        dtype=np.float64,
    )


def _train_model() -> tuple:
    rng = np.random.RandomState(42)
    n_samples = 2500
    X_list: list[np.ndarray] = []
    y_labels: list[str] = []

    for _ in range(n_samples):
        n_answers = int(rng.randint(1, 9))
        raw = rng.uniform(0.0, 5.0, size=n_answers).tolist()
        rule = calculate_risk(raw)
        X_list.append(feature_vector(raw))
        y_labels.append(rule.risk_level)

    X = np.vstack(X_list)
    le = LabelEncoder()
    y = le.fit_transform(y_labels)
    clf = LogisticRegression(max_iter=2000, random_state=42)
    clf.fit(X, y)
    return clf, le


def _ensure_model() -> None:
    global _clf, _label_encoder
    if _clf is not None:
        return
    if not _SKLEARN_OK:
        raise RuntimeError("scikit-learn is not installed")
    _clf, _label_encoder = _train_model()


def predict_risk(answer_values: List[float]) -> RiskScoreResult:
    """
    Predict risk using the trained classifier. Maps predicted class to a
    representative risk_score for API consistency.
    """
    _ensure_model()
    values = [max(0.0, min(5.0, float(v))) for v in answer_values]
    if not values:
        return RiskScoreResult(risk_score=0.0, risk_level="low")

    feats = feature_vector(values).reshape(1, -1)
    pred_idx = int(_clf.predict(feats)[0])
    risk_level = str(_label_encoder.inverse_transform([pred_idx])[0])

    proba = _clf.predict_proba(feats)[0]
    class_scores = {"low": 22.0, "medium": 52.0, "high": 82.0}
    idx_to_level = {i: _label_encoder.classes_[i] for i in range(len(_label_encoder.classes_))}
    blended = sum(proba[i] * class_scores.get(idx_to_level[i], 50.0) for i in range(len(proba)))
    risk_score = round(float(np.clip(blended, 0.0, 100.0)), 2)

    return RiskScoreResult(risk_score=risk_score, risk_level=risk_level)


def reset_model_for_tests() -> None:
    """Clear cached model (tests only)."""
    global _clf, _label_encoder
    _clf = None
    _label_encoder = None
