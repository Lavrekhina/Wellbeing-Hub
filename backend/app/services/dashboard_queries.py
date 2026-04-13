"""Read paths for employee dashboard data."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse


def get_latest_survey_response(db: Session, user_id: int) -> SurveyResponse | None:
    return (
        db.query(SurveyResponse)
        .filter(SurveyResponse.user_id == user_id)
        .order_by(SurveyResponse.submitted_at.desc())
        .first()
    )


def get_latest_risk_assessment(db: Session, user_id: int) -> RiskAssessment | None:
    return (
        db.query(RiskAssessment)
        .filter(RiskAssessment.user_id == user_id)
        .order_by(RiskAssessment.generated_at.desc())
        .first()
    )


def list_recommendation_texts_for_assessment(
    db: Session,
    assessment_id: int,
    *,
    limit: int | None = None,
) -> list[str]:
    q = (
        db.query(Recommendation)
        .filter(Recommendation.assessment_id == assessment_id)
        .order_by(Recommendation.recommendation_id.desc())
    )
    if limit is not None:
        q = q.limit(limit)
    return [row.recommendation_text for row in q.all()]
