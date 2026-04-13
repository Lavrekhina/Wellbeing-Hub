from backend.app.services.recommendation import generate_recommendations


def test_unknown_risk_level_uses_score_buckets():
    recs = generate_recommendations("pending", risk_score=72.0, answer_values=[3.0])
    assert len(recs) == 3
    assert any("manager" in r["recommendation_text"].lower() for r in recs)


def test_high_concentrated_spike_uses_targeted_copy():
    # High max, lower average → concentrated distress branch
    values = [5.0, 5.0, 1.0, 1.0, 1.0]
    recs = generate_recommendations("high", risk_score=80.0, answer_values=values)
    texts = " ".join(r["recommendation_text"] for r in recs).lower()
    assert "highest" in texts or "scores were" in texts


def test_high_broad_elevation_uses_load_focused_copy():
    values = [4.2, 4.0, 4.1, 4.3]
    recs = generate_recommendations("high", risk_score=85.0, answer_values=values)
    joined = " ".join(r["recommendation_text"] for r in recs).lower()
    assert "load" in joined


def test_medium_without_context_matches_baseline_shape():
    recs = generate_recommendations("medium", answer_values=None)
    assert len(recs) == 3
    categories = {r["category"] for r in recs}
    assert "routine" in categories


def test_low_watch_one_area_when_mixed_profile():
    values = [1.0, 1.0, 1.0, 4.0]
    recs = generate_recommendations("low", risk_score=20.0, answer_values=values)
    joined = " ".join(r["recommendation_text"] for r in recs).lower()
    assert "warmer" in joined or "steady" in joined
