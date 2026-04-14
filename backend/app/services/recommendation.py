from __future__ import annotations

from typing import List, Optional, Sequence


def _rec(category: str, text: str) -> dict:
    return {"category": category, "recommendation_text": text}


def _coerce_risk_level(risk_level: str, risk_score: Optional[float]) -> str:
    label = (risk_level or "").strip().lower()
    if label in {"low", "medium", "high"}:
        return label
    if risk_score is not None:
        if risk_score >= 68:
            return "high"
        if risk_score >= 38:
            return "medium"
    return "low"


def _signals(
    answer_values: Optional[Sequence[float]],
    overall_score: Optional[float],
) -> tuple[float, float, float, float, int]:
    if answer_values:
        vals = [max(0.0, min(5.0, float(v))) for v in answer_values]
        n = len(vals)
        avg = sum(vals) / n
        hi = max(vals)
        lo = min(vals)
        return avg, hi, lo, hi - lo, n
    if overall_score is not None:
        v = max(0.0, min(5.0, float(overall_score)))
        return v, v, v, 0.0, 0
    return 0.0, 0.0, 0.0, 0.0, 0


def generate_recommendations(
    risk_level: str,
    *,
    risk_score: Optional[float] = None,
    answer_values: Optional[Sequence[float]] = None,
    overall_score: Optional[float] = None,
) -> List[dict]:
    """
    Build actionable recommendations from risk band, numeric score position, and
    optional answer / aggregate context.
    """
    level = _coerce_risk_level(risk_level, risk_score)
    avg, hi, _, spread, n = _signals(answer_values, overall_score)

    if level == "high":
        recs = _recommendations_high(avg, hi, spread, n)
    elif level == "medium":
        recs = _recommendations_medium(avg, hi, spread, n)
    else:
        recs = _recommendations_low(avg, hi, spread, n)

    return _finalize_recommendations(level, risk_score, n, recs)


def _finalize_recommendations(
    level: str,
    risk_score: Optional[float],
    n: int,
    recs: List[dict],
) -> List[dict]:
    """Score-band nuance and very short check-ins without changing category mix."""
    if not recs:
        return recs

    out = [{**r} for r in recs]

    if n == 1:
        out[-1] = _rec(
            out[-1]["category"],
            (
                "This pulse only covers one item - add another short check-in in a few days "
                "so guidance reflects more than a single snapshot."
            ),
        )

    if risk_score is None:
        return out

    if level == "high":
        if risk_score < 74:
            t = out[0]["recommendation_text"]
            out[0] = _rec(
                out[0]["category"],
                (
                    "You are just above the high-risk threshold - act early while workload "
                    f"and support options are easier to adjust. {t}"
                ),
            )
        elif risk_score >= 86:
            t = out[-1]["recommendation_text"]
            out[-1] = _rec(
                out[-1]["category"],
                (
                    "If stress feels overwhelming or unsafe, use your organisation's urgent "
                    f"support or crisis routes now - do not wait for the next survey. {t}"
                ),
            )

    elif level == "medium":
        if risk_score < 42:
            t = out[0]["recommendation_text"]
            out[0] = _rec(
                out[0]["category"],
                (
                    "You are close to the lower edge of the medium band - small, consistent "
                    f"changes now often prevent larger dips. {t}"
                ),
            )
        elif risk_score > 58:
            t = out[0]["recommendation_text"]
            out[0] = _rec(
                out[0]["category"],
                (
                    "Scores are trending toward the high band - tighten boundaries on new work "
                    f"and book support before intensity climbs. {t}"
                ),
            )

    elif level == "low" and risk_score > 30:
        t = out[0]["recommendation_text"]
        out[0] = _rec(
            out[0]["category"],
            (
                "You are still in the low band but not far from medium - keep monitoring weekly "
                f"so a slow drift does not go unnoticed. {t}"
            ),
        )

    return out


def _recommendations_high(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    if hi >= 4.0 and avg < 3.0 and n >= 2:
        return [
            _rec(
                "support",
                (
                    "Book a confidential conversation with your manager or HR this week "
                    "to unpack the areas where scores were highest."
                ),
            ),
            _rec(
                "workload",
                (
                    "Identify one concrete task or deadline you can pause, delegate, or "
                    "renegotiate so pressure is not concentrated on a single theme."
                ),
            ),
            _rec(
                "wellbeing",
                (
                    "Use a short daily grounding practice (breathing or a walk) right "
                    "after the part of the day that tends to spike your stress."
                ),
            ),
        ]

    if spread <= 1.25 and avg >= 3.5:
        return [
            _rec(
                "workload",
                (
                    "Treat overall load as the main lever: cap new commitments for two "
                    "weeks and protect two focus blocks per day."
                ),
            ),
            _rec(
                "support",
                (
                    "Tell your team you are running hot so they can help reprioritise "
                    "or cover non-urgent work."
                ),
            ),
            _rec(
                "wellbeing",
                (
                    "Schedule recovery time the same way you schedule meetings - non-negotiable "
                    "slots for sleep, movement, or offline time."
                ),
            ),
        ]

    return [
        _rec(
            "support",
            "Schedule a 1:1 wellbeing check-in with your manager this week.",
        ),
        _rec(
            "workload",
            "Review and reduce high-priority workload for the next sprint.",
        ),
        _rec(
            "wellbeing",
            "Use guided stress management resources for 15 minutes daily.",
        ),
    ]


def _recommendations_medium(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    if hi >= 4.0 and avg < 3.2 and n >= 2:
        return [
            _rec(
                "routine",
                (
                    "Before your hardest part of the day, add a 10-minute buffer to "
                    "transition and reset - this often lowers outlier scores over time."
                ),
            ),
            _rec(
                "wellbeing",
                (
                    "Pick one recurring stressor and experiment with a small change "
                    "(timing, environment, or expectations) for one week."
                ),
            ),
            _rec(
                "support",
                (
                    "Share one specific friction point with a trusted colleague or manager "
                    "so it does not stay invisible."
                ),
            ),
        ]

    if spread <= 1.5 and avg >= 2.8:
        return [
            _rec(
                "routine",
                (
                    "Your scores are fairly even - focus on steady habits: consistent "
                    "start/stop times and visible progress on one priority."
                ),
            ),
            _rec(
                "wellbeing",
                "Try one mindfulness or breathing exercise mid-day, three times this week.",
            ),
            _rec(
                "support",
                (
                    "Use your next manager check-in to align on what 'good enough' looks "
                    "like for the current sprint."
                ),
            ),
        ]

    return [
        _rec("routine", "Plan short recovery breaks between focused work sessions."),
        _rec("wellbeing", "Try one mindfulness exercise during your workday."),
        _rec("support", "Discuss current stressors in your next manager check-in."),
    ]


def _recommendations_low(avg: float, hi: float, spread: float, n: int) -> List[dict]:
    if n >= 4 and hi >= 3.5 and avg < 2.5:
        return [
            _rec(
                "maintenance",
                (
                    "Overall you are steady, but one area runs warmer - keep an eye on that "
                    "theme so it does not become a trend."
                ),
            ),
            _rec(
                "wellbeing",
                (
                    "Continue weekly check-ins to catch drift early; small fixes beat big recoveries."
                ),
            ),
            _rec(
                "routine",
                (
                    "Keep one optional wellbeing habit (movement, sleep wind-down, or social time) "
                    "on the calendar as a default, not a reward."
                ),
            ),
        ]

    return [
        _rec("maintenance", "Keep your current work routine and wellbeing habits."),
        _rec("wellbeing", "Continue weekly check-ins to track trend changes early."),
        _rec("routine", "Note one small win each week - momentum matters as much as intensity."),
    ]
