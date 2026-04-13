from fastapi import Depends, FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.api.admin import router as admin_router
from backend.app.api.checkins import router as checkins_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.ml_metrics import router as ml_metrics_router
from backend.app.core.config import settings
from backend.app.core.database import get_db

from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """
    Build and wire the FastAPI application (middleware, routers, health routes).

    Tests and scripts can call this to obtain an isolated app instance; production
    uses the module-level `app` singleton for uvicorn.
    """
    application = FastAPI(title=settings.app_name)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(checkins_router)
    application.include_router(dashboard_router)
    application.include_router(ml_metrics_router)
    application.include_router(admin_router)

    @application.get("/health", tags=["health"])
    def healthcheck() -> dict[str, str]:
        """Minimal probe for load balancers and orchestration."""
        return {"status": "ok"}

    @application.get("/health/readiness", tags=["health"])
    def readiness_check(db: Session = Depends(get_db)) -> JSONResponse:
        """Verify database connectivity (uses the same DB dependency as routes)."""
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

    return application


app = create_app()
