from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class RiskAssessment(Base):
    """
    ORM model representing an AI-generated risk assessment.

    Each assessment:
    - Is associated with a user
    - Stores the computed numeric risk score
    - Stores the categorized risk level (low / medium / high)
    - Tracks when the assessment was generated
    """

    __tablename__ = "ai_risk_assessments"

    # Primary key identifier for the assessment
    assessment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Identifier of the user this assessment belongs to
    # Indexed for fast retrieval of a user's assessment history
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Categorical risk level derived from the computed score
    # Expected values: "low", "medium", "high"
    risk_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Numeric risk score (typically normalized between 0–100)
    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Timestamp when the assessment was generated
    # Stored with timezone awareness for consistency across environments
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )