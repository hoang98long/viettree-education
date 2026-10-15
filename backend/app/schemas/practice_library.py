from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import CatalogAccess, Grade


class PracticeLibraryItem(CatalogAccess):
    id: UUID
    title: str
    lesson_id: UUID | None
    time_limit_seconds: int | None
    assessment_type: str
    subject_code: str
    subject_name: str
    topic_title: str | None
    item_count: int
    graded_count: int
    best_percent: float | None
    latest_percent: float | None
    progress_status: Literal["not_started", "review", "mastered"]


class PracticeLibrarySummary(BaseModel):
    total: int
    review: int
    mastered: int
    not_started: int


class PracticeLibraryResponse(BaseModel):
    grade: Grade
    page: int
    page_size: int
    summary: PracticeLibrarySummary
    items: list[PracticeLibraryItem]
