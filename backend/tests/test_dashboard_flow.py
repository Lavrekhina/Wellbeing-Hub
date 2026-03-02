from backend.app.models.question_response import QuestionResponse
from backend.app.models.recommendation import Recommendation
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.survey_response import SurveyResponse
from backend.app.models.consent_record import ConsentRecord


def test_submit_checkin_persists_records_and_returns_ai_output(client, db_session):
    # Arrange: create a valid check-in payload with 3 answers
    payload = {
        "user_id": 101,
        "survey_id": 1,
        "department_id": 7,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 4.0},
            {"question_id": 2, "answer_value": 5.0},
            {"question_id": 3, "answer_value": 4.0},
        ],
    }

    # Act: submit the check-in
    response = client.post("/api/checkins/submit", json=payload)
    body = response.json()

    # Assert: API returns successful creation response
    assert response.status_code == 201

    # Assert: response contains generated identifiers and computed risk info
    assert body["response_id"] > 0
    assert body["risk_assessment_id"] > 0
    assert body["risk_level"] in {"low", "medium", "high"}
    assert len(body["recommendation_ids"]) >= 1

    # Assert: database records were persisted correctly
    assert db_session.query(SurveyResponse).count() == 1
    assert db_session.query(QuestionResponse).count() == 3
    assert db_session.query(RiskAssessment).count() == 1
    assert db_session.query(Recommendation).count() >= 1
    assert db_session.query(ConsentRecord).count() == 1


def test_dashboard_summary_returns_latest_values(client):
    # Arrange: submit a check-in so dashboard has data
    submit_payload = {
        "user_id": 222,
        "survey_id": 10,
        "department_id": 3,
        "consent_granted": True,
        "answers": [
            {"question_id": 11, "answer_value": 3.0},
            {"question_id": 12, "answer_value": 4.0},
            {"question_id": 13, "answer_value": 3.0},
        ],
    }
    client.post("/api/checkins/submit", json=submit_payload)

    # Act: request dashboard summary for the user
    response = client.get("/api/dashboard/222/summary")
    body = response.json()

    # Assert: endpoint responds successfully
    assert response.status_code == 200

    # Assert: summary contains expected fields and valid values
    assert body["latest_score"] is not None
    assert body["risk_level"] in {"low", "medium", "high", "pending"}
    assert isinstance(body["top_recommendations"], list)
    assert body["last_submitted_at"] is not None


def test_submit_checkin_rejects_duplicate_question_ids(client):
    # Arrange: create payload with duplicate question IDs
    payload = {
        "user_id": 333,
        "survey_id": 20,
        "department_id": 3,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 2.0},
            {"question_id": 1, "answer_value": 4.0},
        ],
    }

    # Act: submit invalid check-in
    response = client.post("/api/checkins/submit", json=payload)
    # Assert: validation error is returned
    assert response.status_code == 422


def test_dashboard_summary_returns_404_when_user_has_no_data(client):
    # Act: request dashboard summary for user with no submissions
    response = client.get("/api/dashboard/9999/summary")

    # Assert: endpoint returns 404 with appropriate error message
    assert response.status_code == 404
    assert response.json()["detail"] == "No survey responses found for user"


def test_submit_checkin_requires_consent(client):
    payload = {
        "user_id": 444,
        "survey_id": 2,
        "department_id": 4,
        "consent_granted": False,
        "answers": [
            {"question_id": 1, "answer_value": 3.0},
        ],
    }

    response = client.post("/api/checkins/submit", json=payload)
    assert response.status_code == 403


def test_latest_consent_returns_record_after_submission(client):
    payload = {
        "user_id": 555,
        "survey_id": 1,
        "department_id": 4,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 3.0},
            {"question_id": 2, "answer_value": 3.5},
        ],
    }
    assert client.post("/api/checkins/submit", json=payload).status_code == 201

    response = client.get("/api/checkins/consent/555/latest")
    body = response.json()

    assert response.status_code == 200
    assert body["user_id"] == 555
    assert body["consent_type"] == "survey_checkin"
    assert body["granted"] is True
    assert body["captured_at"] is not None


def test_latest_consent_returns_404_for_unknown_user(client):
    response = client.get("/api/checkins/consent/98765/latest")
    assert response.status_code == 404
    assert response.json()["detail"] == "No consent record found for user"


def test_latest_consent_rejects_invalid_user_id(client):
    response = client.get("/api/checkins/consent/0/latest")
    assert response.status_code == 422


def test_hr_department_risk_summary_anonymizes_small_groups(client):
    base_payload = {
        "survey_id": 99,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 4.0},
            {"question_id": 2, "answer_value": 4.0},
            {"question_id": 3, "answer_value": 5.0},
        ],
    }

    for user_id in [1001, 1002, 1003]:
        payload = dict(base_payload, user_id=user_id, department_id=10)
        assert client.post("/api/checkins/submit", json=payload).status_code == 201

    for user_id in [2001, 2002]:
        payload = dict(base_payload, user_id=user_id, department_id=20)
        assert client.post("/api/checkins/submit", json=payload).status_code == 201

    response = client.get("/api/dashboard/hr/department-risk-summary?min_group_size=3")
    body = response.json()

    assert response.status_code == 200
    assert body["excluded_departments"] == 1
    assert len(body["departments"]) == 1
    assert body["departments"][0]["department_label"].startswith("group_")
