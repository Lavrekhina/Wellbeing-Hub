from fastapi import FastAPI

from backend.app.api.checkins import router as checkins_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(checkins_router)
app.include_router(dashboard_router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
