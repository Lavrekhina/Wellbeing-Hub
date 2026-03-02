from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class QuestionResponse(Base):
    """
    ORM model representing an individual answer to a survey question.

    Each record belongs to a SurveyResponse and stores:
    - The question identifier
    - The numeric answer value
    - A timestamp for audit/history tracking
    """

    __tablename__ = "question_responses"

    # Primary key for this table
    question_response_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Foreign key linking to the parent survey response
    # CASCADE ensures answers are deleted if the parent response is deleted
    response_id: Mapped[int] = mapped_column(
        ForeignKey("survey_responses.response_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Identifier of the survey question being answered
    question_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Numeric answer value provided by the user
    answer_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Timestamp when the answer record was created
    # Stored with timezone awareness for consistency across environments
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )