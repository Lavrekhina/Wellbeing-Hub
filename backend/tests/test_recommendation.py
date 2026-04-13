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


def test_high_borderline_score_adds_early_action_prefix():
    recs = generate_recommendations("high", risk_score=70.0, answer_values=[4.5, 4.6, 4.4])
    assert "threshold" in recs[0]["recommendation_text"].lower()


def test_high_severe_score_adds_urgent_support_prefix():
    recs = generate_recommendations("high", risk_score=88.0, answer_values=[5.0, 5.0, 5.0])
    joined = recs[-1]["recommendation_text"].lower()
    assert "crisis" in joined or "urgent" in joined


def test_medium_low_end_adds_prevention_prefix():
    recs = generate_recommendations("medium", risk_score=40.0, answer_values=[2.5, 2.6, 2.4])
    assert "edge" in recs[0]["recommendation_text"].lower() or "medium band" in recs[0]["recommendation_text"].lower()


def test_medium_upper_end_adds_escalation_prefix():
    recs = generate_recommendations("medium", risk_score=62.0, answer_values=[3.8, 3.9, 3.7])
    assert "high band" in recs[0]["recommendation_text"].lower()


def test_low_upper_end_adds_drift_watch_prefix():
    recs = generate_recommendations("low", risk_score=34.0, answer_values=[2.0, 2.1, 1.9])
    assert "low band" in recs[0]["recommendation_text"].lower()


def test_single_answer_adds_repeat_pulse_hint():
    recs = generate_recommendations("medium", risk_score=50.0, answer_values=[3.0])
    assert "one item" in recs[-1]["recommendation_text"].lower() or "single" in recs[-1]["recommendation_text"].lower()


def test_overall_score_fallback_when_no_per_question_values():
    recs = generate_recommendations("medium", risk_score=45.0, answer_values=None, overall_score=3.0)
    assert len(recs) == 3
