from backend.app.core.config import Settings


def test_resolved_cors_origins_splits_and_trims():
    s = Settings(cors_allow_origins=" http://a.example ,http://b.example ")
    assert s.resolved_cors_origins() == ["http://a.example", "http://b.example"]


def test_resolved_cors_origins_empty_falls_back_to_default():
    s = Settings(cors_allow_origins=" , , ")
    assert s.resolved_cors_origins() == ["http://localhost:3000"]
