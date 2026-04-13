from backend.app.core import config


def test_admin_overview_hidden_when_no_api_key_configured(client):
    r = client.get("/api/admin/overview")
    assert r.status_code == 404


def test_admin_forbidden_without_header_when_key_set(client, monkeypatch):
    monkeypatch.setattr(config.settings, "admin_api_key", "test-admin-secret")
    r = client.get("/api/admin/overview")
    assert r.status_code == 403


def test_admin_forbidden_with_wrong_key(client, monkeypatch):
    monkeypatch.setattr(config.settings, "admin_api_key", "test-admin-secret")
    r = client.get("/api/admin/overview", headers={"X-Admin-Key": "wrong"})
    assert r.status_code == 403


def test_admin_overview_ok_with_valid_key_empty_db(client, monkeypatch):
    monkeypatch.setattr(config.settings, "admin_api_key", "test-admin-secret")
    r = client.get("/api/admin/overview", headers={"X-Admin-Key": "test-admin-secret"})
    assert r.status_code == 200
    body = r.json()
    assert body["total_survey_responses"] == 0
    assert body["total_risk_assessments"] == 0
    assert body["users_with_latest_assessment"] == 0
    assert body["latest_assessment_risk_breakdown"]["high"] == 0


def test_admin_overview_and_recent_after_checkin(client, monkeypatch):
    monkeypatch.setattr(config.settings, "admin_api_key", "test-admin-secret")
    payload = {
        "user_id": 501,
        "survey_id": 1,
        "department_id": 2,
        "consent_granted": True,
        "answers": [
            {"question_id": 1, "answer_value": 5.0},
            {"question_id": 2, "answer_value": 5.0},
            {"question_id": 3, "answer_value": 5.0},
        ],
    }
    assert client.post("/api/checkins/submit", json=payload).status_code == 201

    headers = {"X-Admin-Key": "test-admin-secret"}
    overview = client.get("/api/admin/overview", headers=headers).json()
    assert overview["total_survey_responses"] == 1
    assert overview["total_risk_assessments"] == 1
    assert overview["total_recommendations"] >= 1
    assert overview["users_with_latest_assessment"] == 1

    recent = client.get("/api/admin/assessments/recent?limit=10", headers=headers)
    assert recent.status_code == 200
    items = recent.json()["items"]
    assert len(items) == 1
    assert items[0]["user_id"] == 501
    assert items[0]["risk_level"] in {"low", "medium", "high"}


def test_whitespace_only_admin_key_treated_as_disabled(client, monkeypatch):
    monkeypatch.setattr(config.settings, "admin_api_key", "   ")
    r = client.get("/api/admin/overview", headers={"X-Admin-Key": "   "})
    assert r.status_code == 404
