# Wellbeing Hub Backend

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update values.
4. Run migrations:
   - `alembic upgrade head`
5. Start API:
   - `uvicorn app.main:app --reload`

## Demo preflight

Before presenting, run:

- `python backend/scripts/demo_preflight.py`

If your API runs on a different URL/port:

- `python backend/scripts/demo_preflight.py http://localhost:8001`
