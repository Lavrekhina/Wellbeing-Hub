from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class AnswerInput(BaseModel):
    question_id: int = Field(gt=0)
    answer_value: float


class CheckinSubmitRequest(BaseModel):
    user_id: int = Field(gt=0)
    survey_id: int = Field(gt=0)
    answers: List[AnswerInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> "CheckinSubmitRequest":
        question_ids = [answer.question_id for answer in self.answers]
        if len(set(question_ids)) != len(question_ids):
            raise ValueError("answers must not contain duplicate question_id values")
        return self


class CheckinSubmitResponse(BaseModel):
    response_id: int
    risk_assessment_id: Optional[int] = None
    recommendation_ids: List[int] = Field(default_factory=list)
    risk_level: str = "pending"
