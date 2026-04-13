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
