from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.dashboard import (
    DashboardRecommendationsResponse,
    DashboardSummaryResponse,
    HrDepartmentRiskSummaryResponse,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/hr/department-risk-summary", response_model=HrDepartmentRiskSummaryResponse)
def get_hr_department_risk_summary(
    min_group_size: int = Query(default=3, ge=2, le=50),
    db: Session = Depends(get_db),
) -> HrDepartmentRiskSummaryResponse:
    """
    HR-level endpoint that returns department risk aggregates with anonymization.
    Departments with fewer than min_group_size employees are excluded.
    """
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load HR dashboard aggregates",
        )

    latest_department_by_user = {}
    for survey in latest_surveys:
        if survey.user_id not in latest_department_by_user:
            latest_department_by_user[survey.user_id] = survey.department_id

    latest_assessment_by_user = {}
    for assessment in latest_assessments:
        if assessment.user_id not in latest_assessment_by_user:
            latest_assessment_by_user[assessment.user_id] = assessment

    grouped = defaultdict(list)
    for user_id, department_id in latest_department_by_user.items():
        if department_id is None:
            continue
        assessment = latest_assessment_by_user.get(user_id)
        if assessment is None:
            continue
        grouped[department_id].append(assessment)

    included_departments = []
    excluded_count = 0
    display_index = 1

    for department_id in sorted(grouped.keys()):
        assessments = grouped[department_id]
        if len(assessments) < min_group_size:
            excluded_count += 1
            continue

        response_count = len(assessments)
        high_count = sum(1 for item in assessments if item.risk_level == "high")
        medium_count = sum(1 for item in assessments if item.risk_level == "medium")
        low_count = sum(1 for item in assessments if item.risk_level == "low")
        avg_risk_score = sum(item.risk_score for item in assessments) / response_count

        included_departments.append(
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

    return HrDepartmentRiskSummaryResponse(
        min_group_size=min_group_size,
        excluded_departments=excluded_count,
        departments=included_departments,
    )


@router.get("/{user_id}/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(user_id: int = Path(gt=0), db: Session = Depends(get_db)) -> DashboardSummaryResponse:
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
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard summary",
        )


@router.get("/{user_id}/recommendations", response_model=DashboardRecommendationsResponse)
def get_dashboard_recommendations(user_id: int = Path(gt=0), db: Session = Depends(get_db)) -> DashboardRecommendationsResponse:
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
    try:
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

        recommendation_rows = (
            db.query(Recommendation)
            .filter(Recommendation.assessment_id == latest_assessment.assessment_id)
            .order_by(Recommendation.created_at.desc())
            .all()
        )
        return DashboardRecommendationsResponse(
            recommendations=[item.recommendation_text for item in recommendation_rows]
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load recommendations",
        )