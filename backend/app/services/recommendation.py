from __future__ import annotations

from typing import List, Sequence


def _coerce_risk_level(risk_level: str, risk_score: float | None) -> str:
    label = (risk_level or "").strip().lower()
    if label in {"low", "medium", "high"}:
        return label
    if risk_score is not None:
        if risk_score >= 68:
            return "high"
        if risk_score >= 38:
            return "medium"
    return "low"


def _signals(answer_values: Sequence[float] | None) -> tuple[float, float, float, float, int]:
    if not answer_values:
        return 0.0, 0.0, 0.0, 0.0, 0
    vals = [max(0.0, min(5.0, float(v))) for v in answer_values]
    n = len(vals)
    avg = sum(vals) / n
    hi = max(vals)
    lo = min(vals)
    return avg, hi, lo, hi - lo, n


def generate_recommendations(
    risk_level: str,
    *,
    risk_score: float | None = None,
    answer_values: Sequence[float] | None = None,
) -> List[dict]:
    """
    Build actionable recommendations from risk band and optional answer context.

    When answer_values are provided, copy is adjusted for common shapes such as
    a few very high scores versus broadly elevated responses.
    """
    level = _coerce_risk_level(risk_level, risk_score)
    avg, hi, lo, spread, n = _signals(answer_values)

    if level == "high":
        return _recommendations_high(avg, hi, spread, n)
    if level == "medium":
        return _recommendations_medium(avg, hi, spread, n)
    return _recommendations_low(avg, hi, spread, n)


def _recommendations_high(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    # Concentrated distress: a few items drive risk while the rest look healthier.
    if hi >= 4.0 and avg < 3.0 and n >= 2:
        return [
            {
                "category": "support",
                "recommendation_text": (
                    "Book a confidential conversation with your manager or HR this week "
                    "to unpack the areas where scores were highest."
                ),
            },
            {
                "category": "workload",
                "recommendation_text": (
                    "Identify one concrete task or deadline you can pause, delegate, or "
                    "renegotiate so pressure is not concentrated on a single theme."
                ),
            },
            {
                "category": "wellbeing",
                "recommendation_text": (
                    "Use a short daily grounding practice (breathing or a walk) right "
                    "after the part of the day that tends to spike your stress."
                ),
            },
        ]

    # Broadly high: most items elevated together.
    if spread <= 1.25 and avg >= 3.5:
        return [
            {
                "category": "workload",
                "recommendation_text": (
                    "Treat overall load as the main lever: cap new commitments for two "
                    "weeks and protect two focus blocks per day."
                ),
            },
            {
                "category": "support",
                "recommendation_text": (
                    "Tell your team you are running hot so they can help reprioritise "
                    "or cover non-urgent work."
                ),
            },
            {
                "category": "wellbeing",
                "recommendation_text": (
                    "Schedule recovery time the same way you schedule meetings - non-negotiable "
                    "slots for sleep, movement, or offline time."
                ),
            },
        ]

    return [
        {
            "category": "support",
            "recommendation_text": (
                "Schedule a 1:1 wellbeing check-in with your manager this week."
            ),
        },
        {
            "category": "workload",
            "recommendation_text": (
                "Review and reduce high-priority workload for the next sprint."
            ),
        },
        {
            "category": "wellbeing",
            "recommendation_text": (
                "Use guided stress management resources for 15 minutes daily."
            ),
        },
    ]


def _recommendations_medium(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    if hi >= 4.0 and avg < 3.2 and n >= 2:
        return [
            {
                "category": "routine",
                "recommendation_text": (
                    "Before your hardest part of the day, add a 10-minute buffer to "
                    "transition and reset - this often lowers outlier scores over time."
                ),
            },
            {
                "category": "wellbeing",
                "recommendation_text": (
                    "Pick one recurring stressor and experiment with a small change "
                    "(timing, environment, or expectations) for one week."
                ),
            },
            {
                "category": "support",
                "recommendation_text": (
                    "Share one specific friction point with a trusted colleague or manager "
                    "so it does not stay invisible."
                ),
            },
        ]

    if spread <= 1.5 and avg >= 2.8:
        return [
            {
                "category": "routine",
                "recommendation_text": (
                    "Your scores are fairly even - focus on steady habits: consistent "
                    "start/stop times and visible progress on one priority."
                ),
            },
            {
                "category": "wellbeing",
                "recommendation_text": (
                    "Try one mindfulness or breathing exercise mid-day, three times this week."
                ),
            },
            {
                "category": "support",
                "recommendation_text": (
                    "Use your next manager check-in to align on what 'good enough' looks "
                    "like for the current sprint."
                ),
            },
        ]

    return [
        {
            "category": "routine",
            "recommendation_text": (
                "Plan short recovery breaks between focused work sessions."
            ),
        },
        {
            "category": "wellbeing",
            "recommendation_text": (
                "Try one mindfulness exercise during your workday."
            ),
        },
        {
            "category": "support",
            "recommendation_text": (
                "Discuss current stressors in your next manager check-in."
            ),
        },
    ]


def _recommendations_low(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    if n >= 4 and hi >= 3.5 and avg < 2.5:
        return [
            {
                "category": "maintenance",
                "recommendation_text": (
                    "Overall you are steady, but one area runs warmer - keep an eye on that "
                    "theme so it does not become a trend."
                ),
            },
            {
                "category": "wellbeing",
                "recommendation_text": (
                    "Continue weekly check-ins to catch drift early; small fixes beat big recoveries."
                ),
            },
            {
                "category": "routine",
                "recommendation_text": (
                    "Keep one optional wellbeing habit (movement, sleep wind-down, or social time) "
                    "on the calendar as a default, not a reward."
                ),
            },
        ]

    return [
        {
            "category": "maintenance",
            "recommendation_text": (
                "Keep your current work routine and wellbeing habits."
            ),
        },
        {
            "category": "wellbeing",
            "recommendation_text": (
                "Continue weekly check-ins to track trend changes early."
            ),
        },
        {
            "category": "routine",
            "recommendation_text": (
                "Note one small win each week - momentum matters as much as intensity."
            ),
        },
    ]
