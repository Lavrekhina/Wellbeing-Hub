from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class AnswerInput(BaseModel):
    """
    Represents a single answer submitted as part of a check-in.
    """

    # Unique identifier of the question being answered (must be positive)
    question_id: int = Field(gt=0)

    # Numeric value representing the user's response on a 0-5 scale.
    answer_value: float = Field(ge=0, le=5)


class CheckinSubmitRequest(BaseModel):
    """
    Request payload for submitting a survey check-in.

    Contains:
    - user_id: ID of the user submitting the survey
    - survey_id: ID of the survey being completed
    - answers: List of question responses (must not be empty)
    """

    # User submitting the survey (must be positive)
    user_id: int = Field(gt=0)

    # Survey being answered (must be positive)
    survey_id: int = Field(gt=0)

    # Department id captured for HR aggregate metrics.
    department_id: int = Field(gt=0)

    # Explicit consent gate for storing wellbeing check-in data.
    consent_granted: bool

    # At least one answer is required
    answers: List[AnswerInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> "CheckinSubmitRequest":
        """
        Ensures that each question_id appears only once in the submission.
        Prevents accidental duplicate answers for the same question.
        """
        question_ids = [answer.question_id for answer in self.answers]

        # Check for duplicates by comparing length of set vs original list
        if len(set(question_ids)) != len(question_ids):
            raise ValueError("answers must not contain duplicate question_id values")

        return self


class CheckinSubmitResponse(BaseModel):
    """
    Response returned after successful check-in submission.

    Fields:
    - response_id: ID of the stored survey response
    - risk_assessment_id: ID of associated risk assessment (if generated)
    - recommendation_ids: List of created recommendation record IDs
    - risk_level: Computed risk level (defaults to 'pending' if not yet processed)
    """

    response_id: int

    # Risk assessment may not exist immediately (e.g., async processing)
    risk_assessment_id: Optional[int] = None

    # List of generated recommendation IDs (empty if none created)
    recommendation_ids: List[int] = Field(default_factory=list)

    # Default state before risk processing completes
    risk_level: str = "pending"


class ConsentStatusResponse(BaseModel):
    user_id: int
    consent_type: str
    granted: bool
    captured_at: str