"""Read models for admin / operational endpoints."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.admin import (
    AdminOverviewResponse,
    AdminRecentAssessmentItem,
    AdminRecentAssessmentsResponse,
    AdminRiskBreakdown,
)
from backend.app.services.risk_assessment_utils import latest_assessment_per_user


def fetch_admin_overview(db: Session) -> AdminOverviewResponse:
    total_surveys = int(db.query(func.count(SurveyResponse.response_id)).scalar() or 0)
    total_assessments = int(db.query(func.count(RiskAssessment.assessment_id)).scalar() or 0)
    total_recs = int(db.query(func.count(Recommendation.recommendation_id)).scalar() or 0)

    ordered = (
        db.query(RiskAssessment)
        .order_by(RiskAssessment.user_id.asc(), RiskAssessment.generated_at.desc())
        .all()
    )
    latest_by_user = latest_assessment_per_user(ordered)
    breakdown = AdminRiskBreakdown()
    for a in latest_by_user.values():
        if a.risk_level == "high":
            breakdown.high += 1
        elif a.risk_level == "medium":
            breakdown.medium += 1
        else:
            breakdown.low += 1

    return AdminOverviewResponse(
        total_survey_responses=total_surveys,
        total_risk_assessments=total_assessments,
        total_recommendations=total_recs,
        users_with_latest_assessment=len(latest_by_user),
        latest_assessment_risk_breakdown=breakdown,
    )


def fetch_recent_assessments(db: Session, limit: int) -> AdminRecentAssessmentsResponse:
    rows = (
        db.query(RiskAssessment)
        .order_by(RiskAssessment.generated_at.desc())
        .limit(limit)
        .all()
    )
    items = [
        AdminRecentAssessmentItem(
            assessment_id=r.assessment_id,
            user_id=r.user_id,
            risk_level=r.risk_level,
            risk_score=r.risk_score,
            generated_at=r.generated_at,
        )
        for r in rows
    ]
    return AdminRecentAssessmentsResponse(items=items, limit=limit)
