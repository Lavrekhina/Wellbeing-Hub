from typing import Iterable


class RiskScoreResult:
    def __init__(self, risk_score: float, risk_level: str):
        self.risk_score = risk_score
        self.risk_level = risk_level


def calculate_risk(answers: Iterable[float]) -> RiskScoreResult:
    values = list(answers)
    if not values:
        return RiskScoreResult(risk_score=0.0, risk_level="low")

    average_answer = sum(values) / len(values)
    risk_score = max(0.0, min(100.0, average_answer * 20.0))

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return RiskScoreResult(risk_score=round(risk_score, 2), risk_level=risk_level)
