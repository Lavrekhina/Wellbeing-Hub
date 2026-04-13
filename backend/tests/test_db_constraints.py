import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.models.question_response import QuestionResponse
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse


def test_rejects_question_answer_outside_scale(db_session):
    survey = SurveyResponse(
        survey_id=1,
        user_id=1,
        department_id=1,
        overall_score=3.0,
    )
    db_session.add(survey)
    db_session.flush()
    db_session.add(
        QuestionResponse(
            response_id=survey.response_id,
            question_id=1,
            answer_value=5.01,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_rejects_duplicate_question_on_same_survey_response(db_session):
    survey = SurveyResponse(
        survey_id=1,
        user_id=1,
        department_id=1,
        overall_score=2.0,
    )
    db_session.add(survey)
    db_session.flush()
    db_session.add(
        QuestionResponse(response_id=survey.response_id, question_id=7, answer_value=2.0)
    )
    db_session.add(
        QuestionResponse(response_id=survey.response_id, question_id=7, answer_value=3.0)
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_rejects_invalid_risk_level(db_session):
    db_session.add(
        RiskAssessment(
            user_id=1,
            risk_level="critical",
            risk_score=50.0,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_rejects_risk_score_out_of_range(db_session):
    db_session.add(
        RiskAssessment(
            user_id=1,
            risk_level="low",
            risk_score=100.01,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
