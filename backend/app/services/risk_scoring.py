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

    # Normalize all incoming answers to a bounded 0-5 scale.
    # This keeps scoring resilient if any upstream client bypasses validation.
    values = [max(0.0, min(5.0, float(answer))) for answer in answers]

    # If no answers were provided, default to lowest risk
    if not values:
        return RiskScoreResult(risk_score=0.0, risk_level="low")

    # Compute average response value and intensity indicators.
    average_answer = sum(values) / len(values)
    max_answer = max(values)
    min_answer = min(values)
    spread = max_answer - min_answer

    # Basic tuning:
    # - Average carries most weight.
    # - Peak stress pushes score up.
    # - Large spread indicates unstable wellbeing pattern.
    normalized_average = (average_answer / 5.0) * 100.0
    normalized_peak = (max_answer / 5.0) * 100.0
    normalized_spread = (spread / 5.0) * 100.0

    risk_score = (normalized_average * 0.7) + (normalized_peak * 0.2) + (normalized_spread * 0.1)
    risk_score = max(0.0, min(100.0, risk_score))

    # Determine categorical risk level based on thresholds
    if risk_score >= 68:
        risk_level = "high"
    elif risk_score >= 38:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Round to 2 decimal places for consistency in API responses
    return RiskScoreResult(
        risk_score=round(risk_score, 2),
        risk_level=risk_level,
    )