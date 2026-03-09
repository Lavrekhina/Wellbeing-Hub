"""
Demo smoke tests that validate all public MVP endpoints.
These checks are intentionally lightweight and focus on endpoint availability
and expected status/response shapes for the presentation flow.
"""


def _seed_checkin(client, user_id: int = 7001, department_id: int = 11) -> dict:
    payload = {
        "user_id": user_id,
        "survey_id": 101,
        "department_id": department_id,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 4.0},
            {"question_id": 2, "answer_value": 3.0},
            {"question_id": 3, "answer_value": 5.0},
        ],
    }
    response = client.post("/api/checkins/submit", json=payload)
    assert response.status_code == 201
    return response.json()


def test_health_endpoint_smoke(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_checkin_submit_endpoint_smoke(client):
    body = _seed_checkin(client, user_id=7002, department_id=12)
    assert body["response_id"] > 0
    assert body["risk_assessment_id"] > 0
    assert body["risk_level"] in {"low", "medium", "high"}
    assert len(body["recommendation_ids"]) >= 1


def test_consent_latest_endpoint_smoke(client):
    _seed_checkin(client, user_id=7003, department_id=13)
    response = client.get("/api/checkins/consent/7003/latest")
    assert response.status_code == 200
    consent = response.json()
    assert consent["user_id"] == 7003
    assert consent["granted"] is True


def test_dashboard_summary_and_recommendations_endpoints_smoke(client):
    _seed_checkin(client, user_id=7004, department_id=14)

    summary_response = client.get("/api/dashboard/7004/summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["latest_score"] is not None
    assert summary["risk_level"] in {"low", "medium", "high", "pending"}
    assert isinstance(summary["top_recommendations"], list)

    recommendations_response = client.get("/api/dashboard/7004/recommendations")
    assert recommendations_response.status_code == 200
    recs = recommendations_response.json()["recommendations"]
    assert isinstance(recs, list)
    assert len(recs) >= 1


def test_hr_aggregate_endpoint_smoke(client):
    for uid in [7101, 7102, 7103]:
        _seed_checkin(client, user_id=uid, department_id=21)

    response = client.get("/api/dashboard/hr/department-risk-summary?min_group_size=3")
    assert response.status_code == 200
    data = response.json()
    assert "departments" in data
    assert "excluded_departments" in data
