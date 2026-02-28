from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.question_response import QuestionResponse
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.checkin import CheckinSubmitRequest, CheckinSubmitResponse
from backend.app.services.recommendation import generate_recommendations
from backend.app.services.risk_scoring import calculate_risk

router = APIRouter(prefix="/api/checkins", tags=["checkins"])


@router.post("/submit", response_model=CheckinSubmitResponse, status_code=status.HTTP_201_CREATED)
def submit_checkin(payload: CheckinSubmitRequest, db: Session = Depends(get_db)) -> CheckinSubmitResponse:
    if len(payload.answers) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="answers must contain at least one item")

    overall_score = sum(answer.answer_value for answer in payload.answers) / len(payload.answers)
    risk_result = calculate_risk(answer.answer_value for answer in payload.answers)

    try:
        with db.begin():
            survey_response = SurveyResponse(
                survey_id=payload.survey_id,
                user_id=payload.user_id,
                overall_score=overall_score,
            )
            db.add(survey_response)
            db.flush()

            question_responses = [
                QuestionResponse(
                    response_id=survey_response.response_id,
                    question_id=answer.question_id,
                    answer_value=answer.answer_value,
                )
                for answer in payload.answers
            ]
            db.add_all(question_responses)

            risk_assessment = RiskAssessment(
                user_id=payload.user_id,
                risk_level=risk_result.risk_level,
                risk_score=risk_result.risk_score,
            )
            db.add(risk_assessment)
            db.flush()

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
            db.flush()

            recommendation_ids = [row.recommendation_id for row in recommendation_rows]

        return CheckinSubmitResponse(
            response_id=survey_response.response_id,
            risk_assessment_id=risk_assessment.assessment_id,
            recommendation_ids=recommendation_ids,
            risk_level=risk_assessment.risk_level,
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist check-in response",
        )
