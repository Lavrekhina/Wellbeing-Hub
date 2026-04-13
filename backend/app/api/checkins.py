from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.consent_record import ConsentRecord
from backend.app.schemas.checkin import (
    CheckinSubmitRequest,
    CheckinSubmitResponse,
    ConsentStatusResponse,
)
from backend.app.services.checkin_persistence import persist_checkin_submission
from backend.app.services.risk_engine import compute_risk_for_checkin

router = APIRouter(prefix="/api/checkins", tags=["checkins"])


@router.post(
    "/submit",
    response_model=CheckinSubmitResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_checkin(
    payload: CheckinSubmitRequest,
    db: Session = Depends(get_db),
) -> CheckinSubmitResponse:
    """
    Submit a survey check-in.

    Steps:
    1. Validate answers are provided.
    2. Calculate overall survey score and risk assessment.
    3. Persist SurveyResponse, QuestionResponse, RiskAssessment, and Recommendations.
    4. Return IDs and risk info for API response.
    """
    if len(payload.answers) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="answers must contain at least one item",
        )

    if not payload.consent_granted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="consent is required before submitting a check-in",
        )

    overall_score = sum(answer.answer_value for answer in payload.answers) / len(payload.answers)
    risk_result = compute_risk_for_checkin([answer.answer_value for answer in payload.answers])

    try:
        return persist_checkin_submission(
            db,
            payload,
            overall_score=overall_score,
            risk_result=risk_result,
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist check-in response",
        )


@router.get(
    "/consent/{user_id}/latest",
    response_model=ConsentStatusResponse,
)
def get_latest_consent(user_id: int = Path(gt=0), db: Session = Depends(get_db)) -> ConsentStatusResponse:
    try:
        record = (
            db.query(ConsentRecord)
            .filter(ConsentRecord.user_id == user_id)
            .order_by(ConsentRecord.timestamp.desc())
            .first()
        )
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No consent record found for user",
            )

        return ConsentStatusResponse(
            user_id=record.user_id,
            consent_type=record.consent_type,
            granted=record.granted,
            captured_at=record.timestamp.isoformat(),
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load consent status",
        )
