"""
Simple ML-based risk classifier (LogisticRegression) trained on synthetic data.

Labels are generated from the existing rule-based scorer so behaviour stays aligned
with the MVP logic while satisfying a "simple ML classifier" requirement.

Enable with USE_ML_RISK_SCORING=true in the environment.
"""

from __future__ import annotations

import math
from typing import Any, List, Sequence

import numpy as np

from backend.app.services.risk_scoring import RiskScoreResult, calculate_risk

# Max answers scored per call (stability / DoS guard).
_MAX_ANSWERS = 500

_clf = None
_label_encoder = None
_class_score_means = None
_SKLEARN_OK = False
_MIN_CONFIDENCE = 0.45

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder

    _SKLEARN_OK = True
except ImportError:
    LogisticRegression = None  # type: ignore[misc, assignment]
    LabelEncoder = None  # type: ignore[misc, assignment]


def is_available() -> bool:
    return _SKLEARN_OK


def sanitize_answer_values(answer_values: Any) -> list[float]:
    """
    Coerce inputs to a bounded list of finite scores in [0, 5].

    - None -> []
    - Non-sequence (except str/bytes) -> TypeError
    - Non-finite or non-numeric entries are skipped
    - At most _MAX_ANSWERS values are kept (earliest first)
    """
    if answer_values is None:
        return []
    if isinstance(answer_values, (str, bytes)):
        raise TypeError("answer_values must be a sequence of numbers")
    if not isinstance(answer_values, Sequence):
        raise TypeError("answer_values must be a list or tuple of numbers")

    out: list[float] = []
    for v in answer_values:
        if len(out) >= _MAX_ANSWERS:
            break
        try:
            x = float(v)
        except (TypeError, ValueError):
            continue
        if not math.isfinite(x):
            continue
        out.append(max(0.0, min(5.0, x)))
    return out


def feature_vector(values: List[float]) -> np.ndarray:
    """
    Feature row aligned with rule-based signals: distribution shape + same
    normalized components used in calculate_risk.
    """
    dim = 11
    if not values:
        return np.zeros(dim, dtype=np.float64)
    arr = np.clip(np.asarray(values, dtype=np.float64), 0.0, 5.0)
    n = len(arr)
    spread = float(arr.max() - arr.min())
    std = float(arr.std(ddof=0)) if n else 0.0
    p_ge_4 = float(np.mean(arr >= 4.0))
    p_ge_3 = float(np.mean(arr >= 3.0))
    mean_v = float(arr.mean())
    max_v = float(arr.max())
    min_v = float(arr.min())
    norm_avg = (mean_v / 5.0) * 100.0
    norm_peak = (max_v / 5.0) * 100.0
    norm_spread = (spread / 5.0) * 100.0
    return np.array(
        [
            mean_v,
            max_v,
            min_v,
            spread,
            min(n / 10.0, 1.0),
            std,
            p_ge_4,
            p_ge_3,
            norm_avg,
            norm_peak,
            norm_spread,
        ],
        dtype=np.float64,
    )


def _train_model() -> tuple:
    rng = np.random.RandomState(42)
    n_samples = 10_000
    X_list: list[np.ndarray] = []
    y_labels: list[str] = []
    y_scores: list[float] = []

    for _ in range(n_samples):
        n_answers = int(rng.randint(1, 9))
        raw = rng.uniform(0.0, 5.0, size=n_answers).tolist()
        rule = calculate_risk(raw)
        X_list.append(feature_vector(raw))
        y_labels.append(rule.risk_level)
        y_scores.append(rule.risk_score)

    X = np.vstack(X_list)
    le = LabelEncoder()
    y = le.fit_transform(y_labels)
    clf = LogisticRegression(
        max_iter=4000,
        random_state=42,
        class_weight="balanced",
        C=0.75,
        solver="lbfgs",
    )
    clf.fit(X, y)
    score_means: dict[str, float] = {}
    for level in le.classes_:
        idxs = [i for i, lab in enumerate(y_labels) if lab == level]
        if not idxs:
            continue
        score_means[str(level)] = float(np.mean([y_scores[i] for i in idxs]))
    # Safety fallback if anything is missing.
    score_means.setdefault("low", 22.0)
    score_means.setdefault("medium", 52.0)
    score_means.setdefault("high", 82.0)
    return clf, le, score_means


def _ensure_model() -> None:
    global _clf, _label_encoder, _class_score_means
    if _clf is not None:
        return
    if not _SKLEARN_OK:
        raise RuntimeError("scikit-learn is not installed")
    _clf, _label_encoder, _class_score_means = _train_model()


def _risk_score_from_proba(proba: np.ndarray) -> float:
    idx_to_level = {i: str(_label_encoder.classes_[i]) for i in range(len(_label_encoder.classes_))}
    blended = sum(
        float(proba[i]) * float(_class_score_means.get(idx_to_level[i], 50.0))
        for i in range(len(proba))
    )
    return round(float(np.clip(blended, 0.0, 100.0)), 2)


def predict_risk(answer_values: Any) -> RiskScoreResult:
    """
    Predict risk using the trained classifier. Maps predicted class to a
    representative risk_score for API consistency.
    """
    values = sanitize_answer_values(answer_values)
    if not values:
        return RiskScoreResult(risk_score=0.0, risk_level="low")

    _ensure_model()
    feats = feature_vector(values).reshape(1, -1)
    proba = _clf.predict_proba(feats)[0]
    risk_score = _risk_score_from_proba(proba)

    # When the classifier is uncertain, defer to the rule-based scorer.
    if float(np.max(proba)) < _MIN_CONFIDENCE:
        return calculate_risk(values)

    pred_idx = int(np.argmax(proba))
    risk_level = str(_label_encoder.inverse_transform([pred_idx])[0])
    return RiskScoreResult(risk_score=risk_score, risk_level=risk_level)


def reset_model_for_tests() -> None:
    """Clear cached model (tests only)."""
    global _clf, _label_encoder, _class_score_means
    _clf = None
    _label_encoder = None
    _class_score_means = None
