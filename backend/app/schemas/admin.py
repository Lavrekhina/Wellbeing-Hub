from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class AdminRiskBreakdown(BaseModel):
    high: int = 0
    medium: int = 0
    low: int = 0


class AdminOverviewResponse(BaseModel):
    total_survey_responses: int
    total_risk_assessments: int
    total_recommendations: int
    users_with_latest_assessment: int
    latest_assessment_risk_breakdown: AdminRiskBreakdown


class AdminRecentAssessmentItem(BaseModel):
    assessment_id: int
    user_id: int
    risk_level: str
    risk_score: float
    generated_at: datetime


class AdminRecentAssessmentsResponse(BaseModel):
    items: List[AdminRecentAssessmentItem]
    limit: int = Field(description="Maximum rows requested")
