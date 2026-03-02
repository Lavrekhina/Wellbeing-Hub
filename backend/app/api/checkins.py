from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.consent_record import ConsentRecord
from backend.app.models.question_response import QuestionResponse
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.checkin import (
    CheckinSubmitRequest,
    CheckinSubmitResponse,
    ConsentStatusResponse,
)
from backend.app.services.recommendation import generate_recommendations
from backend.app.services.risk_scoring import calculate_risk

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

    Args:
        payload (CheckinSubmitRequest): The user's check-in data.
        db (Session, optional): SQLAlchemy session injected by FastAPI.

    Returns:
        CheckinSubmitResponse: Contains survey response ID, risk assessment ID, recommendations, and risk level.

    Raises:
        HTTPException 400: If no answers are provided.
        HTTPException 500: If database persistence fails.
    """
    # Guard clause: require at least one answer
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

    # Calculate the overall average score for the survey
    overall_score = sum(answer.answer_value for answer in payload.answers) / len(payload.answers)

    # Compute risk score and risk level using the service
    risk_result = calculate_risk(answer.answer_value for answer in payload.answers)

    try:
        # Begin a transaction block to ensure atomic persistence
        with db.begin():
            # Persist main survey response
            survey_response = SurveyResponse(
                survey_id=payload.survey_id,
                user_id=payload.user_id,
                department_id=payload.department_id,
                overall_score=overall_score,
            )
            db.add(survey_response)
            db.flush()  # Flush to get survey_response.response_id

            # Persist individual question responses
            question_responses = [
                QuestionResponse(
                    response_id=survey_response.response_id,
                    question_id=answer.question_id,
                    answer_value=answer.answer_value,
                )
                for answer in payload.answers
            ]
            db.add_all(question_responses)

            # Persist risk assessment
            risk_assessment = RiskAssessment(
                user_id=payload.user_id,
                risk_level=risk_result.risk_level,
                risk_score=risk_result.risk_score,
            )
            db.add(risk_assessment)
            db.flush()  # Flush to get risk_assessment.assessment_id

            # Generate and persist recommendations based on risk level
            recommendations_payload = generate_recommendations(risk_result.risk_level)
            recommendation_rows = [
                Recommendation(
                    assessment_id=risk_assessment.assessment_id,
                    recommendation_text=item["recommendation_text"],
                    category=item["category"],
                )
                for item in recommendations_payload
            ]
            db.add_all(recommendation_rows)
            db.flush()  # Flush to get recommendation_ids

            # Collect IDs for API response
            recommendation_ids = [row.recommendation_id for row in recommendation_rows]

            consent_record = ConsentRecord(
                user_id=payload.user_id,
                consent_type="survey_checkin",
                granted=True,
            )
            db.add(consent_record)

        # Return structured response
        return CheckinSubmitResponse(
            response_id=survey_response.response_id,
            risk_assessment_id=risk_assessment.assessment_id,
            recommendation_ids=recommendation_ids,
            risk_level=risk_assessment.risk_level,
        )

    except SQLAlchemyError:
        # Rollback transaction on any database error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist check-in response",
        )


@router.get(
    "/consent/{user_id}/latest",
    response_model=ConsentStatusResponse,
)
def get_latest_consent(user_id: int, db: Session = Depends(get_db)) -> ConsentStatusResponse:
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