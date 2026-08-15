from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubjectOut(BaseModel):
    id: UUID
    code: str
    name: str
    color: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CourseOut(BaseModel):
    id: UUID
    subject_id: UUID
    grade_id: UUID
    title: str
    status: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class LessonOut(BaseModel):
    id: UUID
    course_id: UUID
    title: str
    description: str | None = None
    status: str
    position: int

    model_config = ConfigDict(from_attributes=True)
