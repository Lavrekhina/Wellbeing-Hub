import pytest
from fastapi.testclient import TestClient

from backend.app.core import config
from backend.app.main import app
from backend.app.services import risk_ml
from backend.app.services.risk_ml_metrics import evaluate_synthetic_holdout


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_evaluate_synthetic_holdout_matches_rule_labels_well():
    report = evaluate_synthetic_holdout(n_samples=3500, test_size=0.25, random_state=11)
    assert report["n_test"] > 0
    assert report["accuracy"] >= 0.82
    assert report["macro_f1"] >= 0.75
    assert set(report["per_class"].keys()) == {"low", "medium", "high"}


def test_metrics_endpoint_hidden_by_default():
    with TestClient(app) as client:
        r = client.get("/api/metrics/risk-classifier")
    assert r.status_code == 404


@pytest.mark.skipif(not risk_ml.is_available(), reason="scikit-learn not installed")
def test_metrics_endpoint_returns_report_when_enabled(monkeypatch):
    monkeypatch.setattr(config.settings, "expose_ml_risk_metrics", True)
    with TestClient(app) as client:
        r = client.get("/api/metrics/risk-classifier")
    assert r.status_code == 200
    body = r.json()
    assert "accuracy" in body
    assert body["macro_f1"] >= 0.75
    assert body["per_class"]["low"]["support"] >= 0
