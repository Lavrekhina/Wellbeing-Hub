"""HR-facing aggregates with k-anonymity style department thresholds."""

from __future__ import annotations

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse


def build_anonymized_department_rows(
    db: Session,
    min_group_size: int,
) -> tuple[list[dict], int]:
    """
    Build anonymized department aggregates from each user's latest survey + latest assessment.
    Returns (included_department_payloads, excluded_department_count).
    """
    latest_survey = (
        select(
            SurveyResponse.user_id.label("user_id"),
            SurveyResponse.department_id.label("department_id"),
            func.row_number()
            .over(
                partition_by=SurveyResponse.user_id,
                order_by=SurveyResponse.submitted_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )
    latest_assessment = (
        select(
            RiskAssessment.user_id.label("user_id"),
            RiskAssessment.risk_level.label("risk_level"),
            RiskAssessment.risk_score.label("risk_score"),
            func.row_number()
            .over(
                partition_by=RiskAssessment.user_id,
                order_by=RiskAssessment.generated_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )

    high = func.sum(case((latest_assessment.c.risk_level == "high", 1), else_=0)).label("high_count")
    medium = func.sum(case((latest_assessment.c.risk_level == "medium", 1), else_=0)).label(
        "medium_count"
    )
    low = func.sum(case((latest_assessment.c.risk_level == "low", 1), else_=0)).label("low_count")
    response_count = func.count(latest_assessment.c.user_id).label("response_count")
    avg_risk = func.avg(latest_assessment.c.risk_score).label("avg_risk_score")

    rows = (
        db.execute(
            select(
                latest_survey.c.department_id,
                response_count,
                avg_risk,
                high,
                medium,
                low,
            )
            .select_from(latest_survey)
            .join(
                latest_assessment,
                latest_assessment.c.user_id == latest_survey.c.user_id,
            )
            .where(latest_survey.c.rn == 1)
            .where(latest_assessment.c.rn == 1)
            .where(latest_survey.c.department_id.is_not(None))
            .group_by(latest_survey.c.department_id)
            .order_by(latest_survey.c.department_id.asc())
        )
        .mappings()
        .all()
    )

    included: list[dict] = []
    excluded_count = 0
    display_index = 1

    for row in rows:
        if int(row["response_count"]) < min_group_size:
            excluded_count += 1
            continue

        high_count = int(row["high_count"] or 0)
        medium_count = int(row["medium_count"] or 0)
        low_count = int(row["low_count"] or 0)
        rc = int(row["response_count"])
        avg_score = float(row["avg_risk_score"] or 0.0)

        included.append(
            {
                "department_label": f"group_{display_index}",
                "response_count": rc,
                "avg_risk_score": round(avg_score, 2),
                "high_risk_ratio": round(high_count / rc, 3),
                "risk_level_breakdown": {
                    "high": high_count,
                    "medium": medium_count,
                    "low": low_count,
                },
            }
        )
        display_index += 1

    return included, excluded_count
