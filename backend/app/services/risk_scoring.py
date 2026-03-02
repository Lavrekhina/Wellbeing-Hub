from typing import Iterable


class RiskScoreResult:
    """
    Simple value object representing the result of a risk calculation.

    Attributes:
        risk_score (float): Normalized score between 0 and 100.
        risk_level (str): Categorized risk level ("low", "medium", "high").
    """

    def __init__(self, risk_score: float, risk_level: str):
        self.risk_score = risk_score
        self.risk_level = risk_level


def calculate_risk(answers: Iterable[float]) -> RiskScoreResult:
    """
    Calculates a normalized risk score and corresponding risk level
    from a collection of numeric survey answers.

    Scoring logic:
    - Average the answer values
    - Scale to a 0–100 range (assuming answers are 0–5 scale → *20)
    - Clamp between 0 and 100
    - Categorize into low / medium / high

    Args:
        answers (Iterable[float]): Numeric answer values.

    Returns:
        RiskScoreResult: Contains the final risk score and risk level.
    """

    # Convert iterable to list to allow multiple passes (len + sum)
    values = list(answers)

    # If no answers were provided, default to lowest risk
    if not values:
        return RiskScoreResult(risk_score=0.0, risk_level="low")

    # Compute average response value
    average_answer = sum(values) / len(values)

    # Normalize score to 0–100 range (assuming 0–5 input scale)
    # Clamp ensures score never exceeds bounds
    risk_score = max(0.0, min(100.0, average_answer * 20.0))

    # Determine categorical risk level based on thresholds
    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Round to 2 decimal places for consistency in API responses
    return RiskScoreResult(
        risk_score=round(risk_score, 2),
        risk_level=risk_level,
    )