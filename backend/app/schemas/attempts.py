from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import StrictModel


class StartInput(StrictModel):
    assignment_id: UUID


class ChoiceAnswer(StrictModel):
    option_id: str = Field(max_length=100)


class MultipleAnswer(StrictModel):
    option_ids: list[str] = Field(max_length=30)


class BlankAnswer(StrictModel):
    text: str = Field(max_length=500)


class OrderAnswer(StrictModel):
    ordered_ids: list[str] = Field(max_length=30)


class TextAnswer(StrictModel):
    text: str = Field(max_length=5000)


class AnswerInput(StrictModel):
    answer: dict
    response_time_ms: int | None = Field(default=None, ge=0, le=86400000)


class PublicContent(BaseModel):
    prompt: str
    options: list[dict[str, str]] = Field(default_factory=list)


class AttemptItem(BaseModel):
    id: UUID
    question_version_id: UUID
    position: int
    points: float
    question_type: str
    content: PublicContent
    answer: dict | None = None


class AttemptResponse(BaseModel):
    id: UUID
    assignment_id: UUID
    assessment_id: UUID
    title: str
    grade: int = Field(ge=1, le=5)
    status: Literal["in_progress", "submitted", "graded", "abandoned"]
    started_at: str
    deadline: str | None
    server_time: str
    items: list[AttemptItem]


class ResultItem(BaseModel):
    id: UUID
    position: int
    content: PublicContent
    question_type: str
    student_answer: dict
    is_correct: bool | None
    score: float
    points: float
    explanation: dict
    grading: dict


class ResultResponse(BaseModel):
    id: UUID
    grade: int = Field(ge=1, le=5)
    total_score: float
    max_score: float
    correct_count: int
    answered_count: int
    graded_at: datetime
    items: list[ResultItem]


class StartResponse(BaseModel):
    id: UUID
    resumed: bool
