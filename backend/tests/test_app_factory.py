from backend.app.main import app, create_app


def test_module_app_is_fastapi_instance():
    assert app.title


def test_create_app_returns_distinct_instances():
    first = create_app()
    second = create_app()
    assert first is not second
    assert first.title == second.title
    route_paths = {r.path for r in first.routes if hasattr(r, "path")}
    assert "/health" in route_paths
    assert "/api/checkins/submit" in route_paths
