from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    latest_score: Optional[float]
    risk_level: str
    risk_score: Optional[float]
    top_recommendations: List[str]
    last_submitted_at: Optional[datetime]


class DashboardRecommendationsResponse(BaseModel):
    recommendations: List[str]
