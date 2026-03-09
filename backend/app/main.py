from fastapi import FastAPI

# Import API route groups
from backend.app.api.checkins import router as checkins_router
from backend.app.api.dashboard import router as dashboard_router

# Import application settings (e.g., app name, environment config)
from backend.app.core.config import settings

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