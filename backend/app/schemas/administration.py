from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.attempts import PublicContent
from app.schemas.common import Grade, StrictModel


class StudentUpdate(StrictModel):
    display_name: str = Field(min_length=1, max_length=160)
    current_grade: int = Field(ge=1, le=5)


class StatisticsResponse(BaseModel):
    students: int
    users: int
    lessons: int
    question_versions: int
    assessments: int
    attempts: int
    average_percent: float | None
    correct_answers: int


class StudentResponse(BaseModel):
    id: UUID
    username: str
    display_name: str
    is_active: bool
    current_grade: Grade


class StudentPageResponse(BaseModel):
    total: int
    page: int
    items: list[StudentResponse]


class QuestionResponse(BaseModel):
    id: UUID
    code: str
    grade: Grade
    question_type: str
    difficulty: int
    status: str
    subject_name: str
    content: PublicContent
    question_id: UUID | None = None
    version: int = 1
    reviewed_by: UUID | None = None
    minimum_plan_code: Literal["free", "vip"] | None = None


class QuestionPageResponse(BaseModel):
    total: int
    page: int
    items: list[QuestionResponse]
