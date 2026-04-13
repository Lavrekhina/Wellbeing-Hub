from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class SurveyResponse(Base):
    """
    ORM model representing a submitted survey.

    Each survey response:
    - Belongs to a specific user
    - References a survey template (survey_id)
    - Tracks submission time
    - Optionally stores a computed overall score
    """

    __tablename__ = "survey_responses"

    __table_args__ = (
        CheckConstraint("user_id > 0", name="ck_survey_responses_user_id_positive"),
        CheckConstraint("survey_id > 0", name="ck_survey_responses_survey_id_positive"),
        CheckConstraint(
            "department_id IS NULL OR department_id > 0",
            name="ck_survey_responses_department_id_positive",
        ),
        CheckConstraint(
            "overall_score IS NULL OR (overall_score >= 0 AND overall_score <= 5)",
            name="ck_survey_responses_overall_score_range",
        ),
    )

    # Primary key identifier for the survey submission
    response_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Identifier of the survey template being completed
    survey_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Identifier of the user who submitted the survey
    # Indexed for fast retrieval of a user's submission history
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Department identifier used for HR-level aggregation.
    # Kept numeric and anonymized in HR endpoints.
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )

    # Timestamp when the survey was submitted
    # Stored with timezone awareness for consistency across environments
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    # Optional overall score calculated from the submitted answers
    # Nullable in case scoring occurs asynchronously
    overall_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )