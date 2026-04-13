"""Persist a check-in and related AI outputs in one transaction."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.app.models.consent_record import ConsentRecord
from backend.app.models.question_response import QuestionResponse
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.schemas.checkin import CheckinSubmitRequest, CheckinSubmitResponse
from backend.app.services.recommendation import generate_recommendations
from backend.app.services.risk_scoring import RiskScoreResult


def persist_checkin_submission(
    db: Session,
    payload: CheckinSubmitRequest,
    *,
    overall_score: float,
    risk_result: RiskScoreResult,
) -> CheckinSubmitResponse:
    """
    Store survey response, answers, risk assessment, recommendations, and consent.
    Caller is responsible for try/except and rollback on failure.
    """
    answer_values = [a.answer_value for a in payload.answers]

    with db.begin():
        survey_response = SurveyResponse(
            survey_id=payload.survey_id,
            user_id=payload.user_id,
            department_id=payload.department_id,
            overall_score=overall_score,
        )
        db.add(survey_response)
        db.flush()

        db.add_all(
            [
                QuestionResponse(
                    response_id=survey_response.response_id,
                    question_id=answer.question_id,
                    answer_value=answer.answer_value,
                )
                for answer in payload.answers
            ]
        )

        risk_assessment = RiskAssessment(
            user_id=payload.user_id,
            risk_level=risk_result.risk_level,
            risk_score=risk_result.risk_score,
        )
        db.add(risk_assessment)
        db.flush()

        recommendations_payload = generate_recommendations(
            risk_result.risk_level,
            risk_score=risk_result.risk_score,
            answer_values=answer_values,
            overall_score=overall_score,
        )
        if not recommendations_payload:
            recommendations_payload = [
                {
                    "category": "maintenance",
                    "recommendation_text": "Keep tracking your weekly wellbeing check-ins.",
                }
            ]

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

        db.add(
            ConsentRecord(
                user_id=payload.user_id,
                consent_type="survey_checkin",
                granted=True,
            )
        )

    return CheckinSubmitResponse(
        response_id=survey_response.response_id,
        risk_assessment_id=risk_assessment.assessment_id,
        recommendation_ids=recommendation_ids,
        risk_level=risk_assessment.risk_level,
    )
