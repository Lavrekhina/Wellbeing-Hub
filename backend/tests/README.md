# Integration Test Plan

This folder contains backend integration tests for the check-in to dashboard flow.

## Covered scenarios

1. `POST /api/checkins/submit` stores:
   - survey response
   - question responses
   - risk assessment
   - recommendations
2. `GET /api/dashboard/{user_id}/summary` returns expected summary fields after a check-in.
3. Duplicate question IDs in check-in payload are rejected with `422`.
4. Summary endpoint returns `404` for unknown users with no survey history.
5. Check-in submission is blocked when consent is not granted.
6. HR department risk summary excludes low-sample departments and returns anonymized groups.

## Test environment

- Uses in-memory SQLite (`sqlite+pysqlite:///:memory:`) for fast isolated tests.
- Overrides FastAPI `get_db` dependency per test.
- Recreates schema before each test via SQLAlchemy metadata.

## Run tests

From repository root:

1. Install dependencies:
   - `pip install -r backend/requirements.txt`
   - `pip install -r backend/requirements-dev.txt`
2. Run:
   - `pytest backend/tests -q`
