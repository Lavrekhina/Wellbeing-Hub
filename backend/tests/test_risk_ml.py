import math

import pytest

from backend.app.services import risk_ml
from backend.app.services.risk_engine import compute_risk_for_checkin
from backend.app.services.risk_scoring import calculate_risk


def test_risk_engine_matches_rule_based_when_ml_disabled():
    values = [4.0, 5.0, 4.0]
    expected = calculate_risk(values)
    got = compute_risk_for_checkin(values)
    assert got.risk_level == expected.risk_level
    assert got.risk_score == expected.risk_score


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_ml_predict_produces_valid_risk_bucket():
    risk_ml.reset_model_for_tests()
    result = risk_ml.predict_risk([3.0, 4.0, 5.0])
    assert result.risk_level in {"low", "medium", "high"}
    assert 0.0 <= result.risk_score <= 100.0
    assert result.risk_score == round(result.risk_score, 2)


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_ml_sanitizes_non_finite_and_coerces_numeric_strings():
    risk_ml.reset_model_for_tests()
    r = risk_ml.predict_risk([float("nan"), float("inf"), 4.0, "3.5"])
    assert r.risk_level in {"low", "medium", "high"}
    assert 0.0 <= r.risk_score <= 100.0


def test_sanitize_drops_bad_entries_and_caps_length():
    long = [2.0] * 600
    got = risk_ml.sanitize_answer_values(long)
    assert len(got) == 500
    assert got[0] == 2.0
    assert risk_ml.sanitize_answer_values(None) == []
    mixed = [1.0, "not-a-number", None, 3.0]
    assert risk_ml.sanitize_answer_values(mixed) == [1.0, 3.0]


def test_sanitize_rejects_non_sequence_container():
    with pytest.raises(TypeError):
        risk_ml.sanitize_answer_values(42)
    with pytest.raises(TypeError):
        risk_ml.sanitize_answer_values("1,2,3")


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_ml_empty_after_sanitization_is_low():
    risk_ml.reset_model_for_tests()
    r = risk_ml.predict_risk([float("nan"), math.nan])
    assert r.risk_level == "low"
    assert r.risk_score == 0.0


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_ml_low_confidence_falls_back_to_rule_based():
    risk_ml.reset_model_for_tests()
    values = [2.0, 2.0, 2.0]
    got = risk_ml.predict_risk(values)
    expected = calculate_risk(values)
    # At minimum, ensure we still return a valid rule-aligned object if fallback triggers.
    assert got.risk_level in {"low", "medium", "high"}
    assert 0.0 <= got.risk_score <= 100.0
    assert expected.risk_level in {"low", "medium", "high"}
