from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.schemas.admin import AdminOverviewResponse, AdminRecentAssessmentsResponse
from backend.app.services.admin_queries import fetch_admin_overview, fetch_recent_assessments

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _admin_key_configured() -> str:
    key = (settings.admin_api_key or "").strip()
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return key


def verify_admin(
    x_admin_key: Annotated[Optional[str], Header(alias="X-Admin-Key")] = None,
) -> None:
    expected = _admin_key_configured()
    if not x_admin_key or x_admin_key != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.get("/overview", response_model=AdminOverviewResponse)
def admin_overview(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin),
) -> AdminOverviewResponse:
    """Aggregate counts and latest-per-user risk band breakdown."""
    try:
        return fetch_admin_overview(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load admin overview",
        )


@router.get("/assessments/recent", response_model=AdminRecentAssessmentsResponse)
def admin_recent_assessments(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin),
    limit: int = Query(default=50, ge=1, le=200),
) -> AdminRecentAssessmentsResponse:
    """Most recent risk assessments across all users (newest first)."""
    try:
        return fetch_recent_assessments(db, limit)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load recent assessments",
        )
