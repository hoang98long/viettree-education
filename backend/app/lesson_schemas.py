from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from app.authoring_schemas import StrictModel
from app.schemas import PreviewInput


class Illustration(StrictModel):
    kind: Literal["fraction", "garden", "reading", "clock", "bars", "angles"]
    caption: str = Field(min_length=5, max_length=400)
    numerator: int = Field(default=3, ge=0, le=12)
    denominator: int = Field(default=8, ge=1, le=12)
    rows: int = Field(default=3, ge=1, le=6)
    columns: int = Field(default=4, ge=1, le=8)
    hour: int = Field(default=8, ge=0, le=23)
    minute: int = Field(default=0, ge=0, le=59)
    angle: int = Field(default=60, ge=1, le=180)
    tick: int = Field(default=4, ge=1, le=20)
    labels: list[str] = Field(
        default_factory=lambda: ["Tổ 1", "Tổ 2", "Tổ 3"], min_length=1, max_length=6
    )
    values: list[int] = Field(default_factory=lambda: [12, 16, 20], min_length=1, max_length=6)

    @model_validator(mode="after")
    def fraction_bounds(self):
        if self.kind == "fraction" and self.numerator > self.denominator:
            raise ValueError("Số phần tô màu không vượt tổng số phần")
        if self.kind == "bars" and (
            len(self.labels) != len(self.values)
            or any(not label.strip() or len(label) > 18 for label in self.labels)
            or any(value < 0 or value > 100 for value in self.values)
        ):
            raise ValueError("Biểu đồ cần 1–6 nhãn tương ứng, mỗi giá trị từ 0 đến 100")
        return self


class LessonBlock(StrictModel):
    type: Literal["text", "example", "remember", "practice"]
    title: str = Field(min_length=2, max_length=160)
    text: str = Field(min_length=5, max_length=6000)


class LessonContent(StrictModel):
    category: Literal["core", "thinking"] = "core"
    blocks: list[LessonBlock] = Field(min_length=3, max_length=12)
    goals: list[str] = Field(min_length=1, max_length=5)
    hints: list[str] = Field(default_factory=list, max_length=5)
    free_hint_count: int | None = Field(default=None, ge=1, le=5)
    reflection: list[str] = Field(default_factory=list, max_length=3)
    illustration: Illustration | None = None

    @model_validator(mode="after")
    def text_lists(self):
        if self.free_hint_count is not None and self.free_hint_count > len(self.hints):
            raise ValueError("Số gợi ý miễn phí không vượt tổng gợi ý và phải có ít nhất một")
        for values in (self.goals, self.hints, self.reflection):
            if any(not value.strip() or len(value) > 600 for value in values):
                raise ValueError("Mỗi gợi ý/mục tiêu cần 1–600 ký tự")
        if not any(block.type == "example" for block in self.blocks):
            raise ValueError("Bài học cần ít nhất một ví dụ")
        return self


class LessonInput(StrictModel):
    code: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]+$")
    grade: int = Field(ge=1, le=5)
    subject_id: UUID
    topic_id: UUID
    skill_ids: list[UUID] = Field(min_length=1, max_length=10)
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(default="", max_length=2000)
    estimated_minutes: int = Field(default=15, ge=1, le=60)
    sort_order: int = Field(default=100, ge=0, le=999)
    minimum_plan_code: Literal["free", "vip"] = "free"
    learning_level: Literal["basic", "reinforcement", "advanced"] = "basic"
    preview: PreviewInput = Field(default_factory=PreviewInput)
    content: LessonContent
    expected_revision: int = Field(default=0, ge=0)
    source_fingerprint: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def distinct_skills(self):
        if len(set(self.skill_ids)) != len(self.skill_ids):
            raise ValueError("Kỹ năng bị lặp")
        return self
