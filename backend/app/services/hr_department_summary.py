"""HR-facing aggregates with k-anonymity style department thresholds."""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy.orm import Session

from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse


def build_anonymized_department_rows(
    db: Session,
    min_group_size: int,
) -> tuple[list[dict], int]:
    """
    Load latest survey (department) and latest assessment per user, group by department,
    and return (included_department_payloads, excluded_department_count).
    """
    latest_surveys = (
        db.query(SurveyResponse)
        .order_by(SurveyResponse.user_id.asc(), SurveyResponse.submitted_at.desc())
        .all()
    )
    latest_assessments = (
        db.query(RiskAssessment)
        .order_by(RiskAssessment.user_id.asc(), RiskAssessment.generated_at.desc())
        .all()
    )

    latest_department_by_user: dict[int, int | None] = {}
    for survey in latest_surveys:
        if survey.user_id not in latest_department_by_user:
            latest_department_by_user[survey.user_id] = survey.department_id

    latest_assessment_by_user: dict[int, RiskAssessment] = {}
    for assessment in latest_assessments:
        if assessment.user_id not in latest_assessment_by_user:
            latest_assessment_by_user[assessment.user_id] = assessment

    grouped: dict[int, list[RiskAssessment]] = defaultdict(list)
    for user_id, department_id in latest_department_by_user.items():
        if department_id is None:
            continue
        assessment = latest_assessment_by_user.get(user_id)
        if assessment is None:
            continue
        grouped[department_id].append(assessment)

    included: list[dict] = []
    excluded_count = 0
    display_index = 1

    for dept_key in sorted(grouped.keys()):
        assessments = grouped[dept_key]
        if len(assessments) < min_group_size:
            excluded_count += 1
            continue

        response_count = len(assessments)
        high_count = sum(1 for item in assessments if item.risk_level == "high")
        medium_count = sum(1 for item in assessments if item.risk_level == "medium")
        low_count = sum(1 for item in assessments if item.risk_level == "low")
        avg_risk_score = sum(item.risk_score for item in assessments) / response_count

        included.append(
            {
                "department_label": f"group_{display_index}",
                "response_count": response_count,
                "avg_risk_score": round(avg_risk_score, 2),
                "high_risk_ratio": round(high_count / response_count, 3),
                "risk_level_breakdown": {
                    "high": high_count,
                    "medium": medium_count,
                    "low": low_count,
                },
            }
        )
        display_index += 1

    return included, excluded_count
