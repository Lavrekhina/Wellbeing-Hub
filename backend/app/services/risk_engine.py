"""
Selects rule-based or ML risk scoring based on configuration.
"""

from backend.app.core.config import settings
from backend.app.services import risk_ml
from backend.app.services.risk_scoring import RiskScoreResult, calculate_risk


def compute_risk_for_checkin(answer_values: list[float]) -> RiskScoreResult:
    if settings.use_ml_risk_scoring and risk_ml.is_available():
        try:
            return risk_ml.predict_risk(answer_values)
        except Exception:
            pass
    return calculate_risk(answer_values)
