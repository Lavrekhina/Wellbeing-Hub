from typing import Dict

from pydantic import BaseModel, Field


class PerClassMetric(BaseModel):
    precision: float
    recall: float
    f1: float
    support: int


class RiskClassifierMetricsResponse(BaseModel):
    n_total: int
    n_train: int
    n_test: int
    test_size: float = Field(description="Fraction held out for testing")
    random_state: int
    accuracy: float
    macro_f1: float
    weighted_f1: float
    per_class: Dict[str, PerClassMetric]
