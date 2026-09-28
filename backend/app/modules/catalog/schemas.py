from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubjectOut(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None = None
    icon_url: str | None = None
    display_order: int = 0
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CourseOut(BaseModel):
    id: UUID
    subject_id: UUID
    grade: int
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    display_order: int = 0
    is_published: bool

    model_config = ConfigDict(from_attributes=True)


class CourseDetailOut(CourseOut):
    subject_name: str


class LessonOut(BaseModel):
    id: UUID
    course_id: UUID
    title: str
    description: str | None = None
    lesson_number: int
    estimated_minutes: int | None = None
    difficulty: str
    is_published: bool

    model_config = ConfigDict(from_attributes=True)
