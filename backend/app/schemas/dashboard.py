from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    latest_score: Optional[float]
    risk_level: str
    risk_score: Optional[float]
    top_recommendations: List[str]
    last_submitted_at: Optional[datetime]


class DashboardRecommendationsResponse(BaseModel):
    recommendations: List[str]


class DepartmentRiskAggregate(BaseModel):
    department_label: str
    response_count: int
    avg_risk_score: float
    high_risk_ratio: float
    risk_level_breakdown: Dict[str, int]


class HrDepartmentRiskSummaryResponse(BaseModel):
    min_group_size: int
    excluded_departments: int
    departments: List[DepartmentRiskAggregate]
