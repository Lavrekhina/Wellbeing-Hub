from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.dashboard import (
    DashboardRecommendationsResponse,
    DashboardSummaryResponse,
    HrDepartmentRiskSummaryResponse,
)
from backend.app.services.dashboard_queries import (
    get_latest_risk_assessment,
    get_latest_survey_response,
    list_recommendation_texts_for_assessment,
)
from backend.app.services.hr_department_summary import build_anonymized_department_rows

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
        departments, excluded = build_anonymized_department_rows(db, min_group_size)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load HR dashboard aggregates",
        )

    return HrDepartmentRiskSummaryResponse(
        min_group_size=min_group_size,
        excluded_departments=excluded,
        departments=departments,
    )


@router.get("/{user_id}/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(user_id: int = Path(gt=0), db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    """
    Latest survey score, risk assessment, top recommendations, and last submission time.
    """
    try:
        latest_response = get_latest_survey_response(db, user_id)
        if latest_response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No survey responses found for user",
            )

        latest_assessment = get_latest_risk_assessment(db, user_id)
        top_recommendations: list[str] = []
        if latest_assessment is not None:
            top_recommendations = list_recommendation_texts_for_assessment(
                db,
                latest_assessment.assessment_id,
                limit=3,
            )

        return DashboardSummaryResponse(
            latest_score=latest_response.overall_score,
            risk_level=latest_assessment.risk_level if latest_assessment else "pending",
            risk_score=latest_assessment.risk_score if latest_assessment else None,
            top_recommendations=top_recommendations,
            last_submitted_at=latest_response.submitted_at,
        )
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard summary",
        )


@router.get("/{user_id}/recommendations", response_model=DashboardRecommendationsResponse)
def get_dashboard_recommendations(
    user_id: int = Path(gt=0),
    db: Session = Depends(get_db),
) -> DashboardRecommendationsResponse:
    """All recommendation texts for the user's latest risk assessment."""
    try:
        latest_assessment = get_latest_risk_assessment(db, user_id)
        if latest_assessment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No risk assessments found for user",
            )

        texts = list_recommendation_texts_for_assessment(
            db,
            latest_assessment.assessment_id,
            limit=None,
        )
        return DashboardRecommendationsResponse(recommendations=texts)
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load recommendations",
        )
