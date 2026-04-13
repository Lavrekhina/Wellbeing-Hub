from fastapi import Depends, FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

# Import API route groups
from backend.app.api.admin import router as admin_router
from backend.app.api.checkins import router as checkins_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.ml_metrics import router as ml_metrics_router

# Import application settings (e.g., app name, environment config)
from backend.app.core.config import settings
from backend.app.core.database import get_db

from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI application instance
# Title is dynamically pulled from configuration settings
app = FastAPI(title=settings.app_name)

# Allow frontend dev server to communicate with the API
# Required for cross-origin requests from Next.js (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register feature routers with the main app
# These routers define grouped endpoints (e.g., /api/checkins, /api/dashboard)
# Keeping router registration centralized here makes integration wiring explicit.
app.include_router(checkins_router)
app.include_router(dashboard_router)
app.include_router(ml_metrics_router)
app.include_router(admin_router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    """
    Health check endpoint used for:
    - Load balancer checks
    - Container orchestration
    - Monitoring systems

    Returns:
        dict: Simple status confirmation.
    """
    # Keep payload intentionally minimal for lightweight health probes.
    return {"status": "ok"}


@app.get("/health/readiness", tags=["health"])
def readiness_check(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Readiness endpoint for demo preflight checks.
    Verifies API process and database connectivity before live presentation.
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "ready": False,
                "database": "down",
                "reason": str(exc),
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "ready": True,
            "database": "ok",
            "service": "wellbeing-backend",
        },
    )