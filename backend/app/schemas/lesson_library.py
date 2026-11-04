from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import CatalogAccess, Grade


class LessonLibraryItem(CatalogAccess):
    id: UUID
    title: str
    estimated_minutes: int | None
    topic_title: str
    subject_code: str
    subject_name: str
    progress_status: Literal["not_started", "in_progress", "completed"]
    category: str
    is_bookmarked: bool


class LibrarySummary(BaseModel):
    total: int
    completed: int
    in_progress: int
    free: int
    vip: int
    bookmarked: int


class LessonLibraryResponse(BaseModel):
    grade: Grade
    page: int
    page_size: int
    summary: LibrarySummary
    releases: list[dict[str, str]] = Field(default_factory=list)
    items: list[LessonLibraryItem]
