from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.dashboard import DashboardRecommendationsResponse, DashboardSummaryResponse

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/{user_id}/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(user_id: int, db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    latest_response = (
        db.query(SurveyResponse)
        .filter(SurveyResponse.user_id == user_id)
        .order_by(SurveyResponse.submitted_at.desc())
        .first()
    )
    if latest_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No survey responses found for user")

    latest_assessment = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.user_id == user_id)
        .order_by(RiskAssessment.generated_at.desc())
        .first()
    )

    top_recommendations = []
    if latest_assessment is not None:
        recommendation_rows = (
            db.query(Recommendation)
            .filter(Recommendation.assessment_id == latest_assessment.assessment_id)
            .order_by(Recommendation.created_at.desc())
            .limit(3)
            .all()
        )
        top_recommendations = [item.recommendation_text for item in recommendation_rows]

    return DashboardSummaryResponse(
        latest_score=latest_response.overall_score,
        risk_level=latest_assessment.risk_level if latest_assessment else "pending",
        risk_score=latest_assessment.risk_score if latest_assessment else None,
        top_recommendations=top_recommendations,
        last_submitted_at=latest_response.submitted_at,
    )


@router.get("/{user_id}/recommendations", response_model=DashboardRecommendationsResponse)
def get_dashboard_recommendations(user_id: int, db: Session = Depends(get_db)) -> DashboardRecommendationsResponse:
    latest_assessment = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.user_id == user_id)
        .order_by(RiskAssessment.generated_at.desc())
        .first()
    )
    if latest_assessment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No risk assessments found for user")

    recommendation_rows = (
        db.query(Recommendation)
        .filter(Recommendation.assessment_id == latest_assessment.assessment_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    return DashboardRecommendationsResponse(
        recommendations=[item.recommendation_text for item in recommendation_rows]
    )
