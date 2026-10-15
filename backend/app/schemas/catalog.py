from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import CatalogAccess, Grade


class GradeResponse(BaseModel):
    grade: Grade
    status: Literal["available", "building"]
    label: str


class SubjectResponse(BaseModel):
    id: UUID
    code: str
    name_vi: str
    description: str | None
    topic_count: int
    grade: Grade
    status: Literal["available", "building"]


class TopicResponse(BaseModel):
    id: UUID
    subject_id: UUID
    grade: Grade
    code: str
    title: str
    description: str | None
    sort_order: int


class LessonSummaryResponse(CatalogAccess):
    id: UUID
    topic_id: UUID
    code: str
    title: str
    description: str | None
    estimated_minutes: int | None
    status: Literal["draft", "published", "archived"]


class LessonResponse(LessonSummaryResponse):
    is_bookmarked: bool = False
    content: dict
    hint_access: dict[str, int] = Field(default_factory=dict)
    grade: Grade
    topic_title: str
    subject_code: str
    subject_name: str
    practice: list[dict]
    progress_status: Literal["not_started", "in_progress", "completed"] = "not_started"
    next_lessons: list[dict] = Field(default_factory=list)


class AssessmentResponse(CatalogAccess):
    id: UUID
    code: str
    title: str
    description: str | None
    grade: Grade
    status: Literal["draft", "published", "archived"]
    lesson_id: UUID | None
    topic_id: UUID | None
    max_attempts: int
    time_limit_seconds: int | None
    subject_code: str
    subject_name: str
    item_count: int
    attempt_count: int | None = None
    assessment_type: str = "practice"


class AssignmentResponse(BaseModel):
    id: UUID
    assessment_id: UUID
    status: Literal["assigned", "in_progress", "completed", "cancelled", "expired"]
    assignment_source: Literal["self", "system", "teacher", "guardian"]
    available_at: datetime
    due_at: datetime | None
    title: str | None = None
