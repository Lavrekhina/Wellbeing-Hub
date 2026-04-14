"""Read models for admin / operational endpoints."""

from __future__ import annotations

from sqlalchemy import case, func, select
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


def fetch_admin_overview(db: Session) -> AdminOverviewResponse:
    total_surveys = int(db.query(func.count(SurveyResponse.response_id)).scalar() or 0)
    total_assessments = int(db.query(func.count(RiskAssessment.assessment_id)).scalar() or 0)
    total_recs = int(db.query(func.count(Recommendation.recommendation_id)).scalar() or 0)

    latest = (
        select(
            RiskAssessment.user_id.label("user_id"),
            RiskAssessment.risk_level.label("risk_level"),
            func.row_number()
            .over(
                partition_by=RiskAssessment.user_id,
                order_by=RiskAssessment.generated_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )

    breakdown_row = (
        db.execute(
            select(
                func.count(latest.c.user_id).label("users_with_latest_assessment"),
                func.sum(case((latest.c.risk_level == "high", 1), else_=0)).label("high"),
                func.sum(case((latest.c.risk_level == "medium", 1), else_=0)).label("medium"),
                func.sum(case((latest.c.risk_level == "low", 1), else_=0)).label("low"),
            ).where(latest.c.rn == 1)
        )
        .mappings()
        .one()
    )

    breakdown = AdminRiskBreakdown(
        high=int(breakdown_row["high"] or 0),
        medium=int(breakdown_row["medium"] or 0),
        low=int(breakdown_row["low"] or 0),
    )
    users_with_latest = int(breakdown_row["users_with_latest_assessment"] or 0)

    return AdminOverviewResponse(
        total_survey_responses=total_surveys,
        total_risk_assessments=total_assessments,
        total_recommendations=total_recs,
        users_with_latest_assessment=users_with_latest,
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
