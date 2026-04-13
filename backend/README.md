# Wellbeing Hub Backend

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update values.
   - Optional: set `USE_ML_RISK_SCORING=true` to use the sklearn classifier (trained on synthetic rule-labelled data); default is rule-based only.
   - Optional: set `EXPOSE_ML_RISK_METRICS=true` to enable `GET /api/metrics/risk-classifier` (hold-out accuracy / F1 on synthetic rule-labelled data).
4. Run migrations:
   - `alembic upgrade head`
5. Start API:
   - `uvicorn app.main:app --reload`

## Demo preflight

Before presenting, run:

- `python backend/scripts/demo_preflight.py`

If your API runs on a different URL/port:

- `python backend/scripts/demo_preflight.py http://localhost:8001`
