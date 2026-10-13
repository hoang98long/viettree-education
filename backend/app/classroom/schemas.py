from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from app.schemas.accounts import AdminAction
from app.schemas.common import StrictModel

Category = Literal["MATH", "VIETNAMESE", "ENGLISH", "AI", "AI_PROJECT"]


class ClassInput(StrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=3, max_length=160)
    grade: int = Field(ge=1, le=5)
    teacher_id: UUID | None = None
    school_id: UUID | None = None
    academic_year: str = Field(default="2026-2027", pattern=r"^20\d{2}-20\d{2}$")
    is_active: bool = True
    recognition_enabled: bool = True
    revision: int | None = Field(default=None, ge=1)


class EnrollmentInput(StrictModel):
    student_id: UUID
    enrolled: bool = True


class AssignmentInput(StrictModel):
    kind: Literal["lesson", "assessment", "ai_lesson"]
    resource_id: UUID
    class_id: UUID | None = None
    student_ids: list[UUID] = Field(default_factory=list, max_length=50)
    due_at: datetime | None = None
    idempotency_key: UUID

    @model_validator(mode="after")
    def target(self):
        if bool(self.class_id) == bool(self.student_ids):
            raise ValueError("Chọn cả lớp hoặc học sinh riêng")
        if len(set(self.student_ids)) != len(self.student_ids):
            raise ValueError("Học sinh bị lặp")
        if self.due_at and self.due_at.tzinfo is None:
            raise ValueError("Hạn nộp cần múi giờ")
        return self


class RecognitionInput(StrictModel):
    category: Category
    period: Literal["week", "month"] = "month"
    resource_id: UUID | None = None


class PriceInput(AdminAction):
    label: str = Field(min_length=3, max_length=100)
    reference_price_vnd: int = Field(ge=1000, le=10000000)
    is_active: bool
    revision: int = Field(ge=1)


class PromotionInput(AdminAction):
    code: str = Field(pattern=r"^[a-z0-9-]{3,50}$")
    price_code: str = Field(pattern=r"^vip-(30|90|365)$")
    label: str = Field(min_length=3, max_length=120)
    sale_price_vnd: int = Field(ge=1000, le=10000000)
    starts_at: datetime
    ends_at: datetime
    is_active: bool = True
    revision: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def dates(self):
        if not self.starts_at.tzinfo or not self.ends_at.tzinfo or self.ends_at <= self.starts_at:
            raise ValueError("Cần thời gian có múi giờ và ngày kết thúc sau bắt đầu")
        return self
