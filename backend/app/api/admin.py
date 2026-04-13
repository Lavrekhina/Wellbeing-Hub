from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.admin import (
    AdminOverviewResponse,
    AdminRecentAssessmentItem,
    AdminRecentAssessmentsResponse,
    AdminRiskBreakdown,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _admin_key_configured() -> str:
    key = (settings.admin_api_key or "").strip()
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return key


def verify_admin(
    x_admin_key: Annotated[str | None, Header(alias="X-Admin-Key")] = None,
) -> None:
    expected = _admin_key_configured()
    if not x_admin_key or x_admin_key != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def _latest_assessment_per_user(assessments: list[RiskAssessment]) -> dict[int, RiskAssessment]:
    latest: dict[int, RiskAssessment] = {}
    for row in assessments:
        if row.user_id not in latest:
            latest[row.user_id] = row
    return latest


@router.get("/overview", response_model=AdminOverviewResponse)
def admin_overview(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin),
) -> AdminOverviewResponse:
    """
    Aggregate counts and latest-per-user risk band breakdown (operational / support use).
    """
    try:
        total_surveys = int(db.query(func.count(SurveyResponse.response_id)).scalar() or 0)
        total_assessments = int(db.query(func.count(RiskAssessment.assessment_id)).scalar() or 0)
        total_recs = int(db.query(func.count(Recommendation.recommendation_id)).scalar() or 0)

        ordered = (
            db.query(RiskAssessment)
            .order_by(RiskAssessment.user_id.asc(), RiskAssessment.generated_at.desc())
            .all()
        )
        latest_by_user = _latest_assessment_per_user(ordered)
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load admin overview",
        )


@router.get("/assessments/recent", response_model=AdminRecentAssessmentsResponse)
def admin_recent_assessments(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin),
    limit: int = Query(default=50, ge=1, le=200),
) -> AdminRecentAssessmentsResponse:
    """Most recent risk assessments across all users (newest first)."""
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load recent assessments",
        )
