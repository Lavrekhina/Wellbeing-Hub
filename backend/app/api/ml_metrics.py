from fastapi import APIRouter, HTTPException, status

from backend.app.core.config import settings
from backend.app.schemas.ml_metrics import RiskClassifierMetricsResponse
from backend.app.services import risk_ml
from backend.app.services.risk_ml_metrics import evaluate_synthetic_holdout

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get(
    "/risk-classifier",
    response_model=RiskClassifierMetricsResponse,
    summary="Synthetic hold-out metrics for the ML risk classifier",
)
def get_risk_classifier_metrics() -> RiskClassifierMetricsResponse:
    if not settings.expose_ml_risk_metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if not risk_ml.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="scikit-learn is not installed",
        )
    try:
        payload = evaluate_synthetic_holdout()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    return RiskClassifierMetricsResponse.model_validate(payload)
