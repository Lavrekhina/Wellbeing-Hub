"""Shared helpers for working with risk assessment rows."""

from __future__ import annotations

from collections.abc import Iterable

from backend.app.models.risk_assessment import RiskAssessment


def latest_assessment_per_user(assessments: Iterable[RiskAssessment]) -> dict[int, RiskAssessment]:
    """
    Given rows ordered by user_id ascending then generated_at descending,
    return each user's most recent assessment.
    """
    latest: dict[int, RiskAssessment] = {}
    for row in assessments:
        if row.user_id not in latest:
            latest[row.user_id] = row
    return latest
