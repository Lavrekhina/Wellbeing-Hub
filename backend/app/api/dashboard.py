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
    """
    Retrieve the latest dashboard summary for a user.

    This includes:
    - Most recent survey overall score
    - Latest risk assessment (level and score)
    - Top 3 recommendations
    - Timestamp of the latest survey submission

    Args:
        user_id (int): ID of the user
        db (Session): SQLAlchemy session injected by FastAPI

    Returns:
        DashboardSummaryResponse: Summary data for dashboard display

    Raises:
        HTTPException 404: If the user has no survey responses
    """
    # Get the most recent survey submission for the user
    latest_response = (
        db.query(SurveyResponse)
        .filter(SurveyResponse.user_id == user_id)
        .order_by(SurveyResponse.submitted_at.desc())
        .first()
    )
    if latest_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No survey responses found for user",
        )

    # Get the latest risk assessment for the user (may be None if not yet assessed)
    latest_assessment = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.user_id == user_id)
        .order_by(RiskAssessment.generated_at.desc())
        .first()
    )

    # Fetch top 3 recommendations if a risk assessment exists
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
    """
    Retrieve all recommendations for a user's latest risk assessment.

    Args:
        user_id (int): ID of the user
        db (Session): SQLAlchemy session injected by FastAPI

    Returns:
        DashboardRecommendationsResponse: List of all recommendation texts

    Raises:
        HTTPException 404: If the user has no risk assessments
    """
    # Fetch the latest risk assessment for the user
    latest_assessment = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.user_id == user_id)
        .order_by(RiskAssessment.generated_at.desc())
        .first()
    )
    if latest_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No risk assessments found for user",
        )

    # Retrieve all recommendations linked to the latest assessment
    recommendation_rows = (
        db.query(Recommendation)
        .filter(Recommendation.assessment_id == latest_assessment.assessment_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return DashboardRecommendationsResponse(
        recommendations=[item.recommendation_text for item in recommendation_rows]
    )