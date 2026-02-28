from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    response_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    survey_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
