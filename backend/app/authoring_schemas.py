from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from app.schemas import PreviewInput
from app.schemas import StrictModel as BaseStrictModel
from app.services.grading import normalize


class StrictModel(BaseStrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Option(StrictModel):
    id: str = Field(min_length=1, max_length=30, pattern=r"^[a-zA-Z0-9_-]+$")
    text: str = Field(min_length=1, max_length=500)


class QuestionContent(StrictModel):
    prompt: str = Field(min_length=5, max_length=5000)
    options: list[Option] = Field(default_factory=list, max_length=8)


class SingleKey(StrictModel):
    correct_option_id: str


class MultipleKey(StrictModel):
    correct_option_ids: list[str] = Field(min_length=1, max_length=8)


class OrderKey(StrictModel):
    ordered_ids: list[str] = Field(min_length=2, max_length=8)


class BlankKey(StrictModel):
    accepted_answers: list[str] = Field(min_length=1, max_length=20)
    case_sensitive: bool = False


class QuestionInput(StrictModel):
    code: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]+$")
    grade: int = Field(ge=1, le=5)
    subject_id: UUID
    topic_id: UUID
    skill_ids: list[UUID] = Field(min_length=1, max_length=10)
    question_type: Literal["single_choice", "multiple_choice", "fill_blank", "ordering"]
    difficulty: int = Field(ge=1, le=5)
    content: QuestionContent
    grading: dict
    explanation: str = Field(min_length=5, max_length=5000)
    minimum_plan_code: Literal["free", "vip"] = "free"
    expected_revision: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_key(self):
        if len(set(self.skill_ids)) != len(self.skill_ids):
            raise ValueError("Kỹ năng bị lặp")
        kind = self.question_type
        model = {
            "single_choice": SingleKey,
            "multiple_choice": MultipleKey,
            "fill_blank": BlankKey,
            "ordering": OrderKey,
        }[kind]
        key = model.model_validate(self.grading).model_dump()
        ids = [option.id for option in self.content.options]
        if kind == "fill_blank":
            if ids or any(
                not value.strip() or len(value) > 500 for value in key["accepted_answers"]
            ):
                raise ValueError("Đáp án điền khuyết chưa hợp lệ")
        else:
            if (
                len(ids) < 2
                or len(set(ids)) != len(ids)
                or len({normalize(option.text) for option in self.content.options}) != len(ids)
            ):
                raise ValueError("Cần ít nhất hai lựa chọn khác nhau")
            values = (
                [key["correct_option_id"]]
                if kind == "single_choice"
                else key["correct_option_ids"]
                if kind == "multiple_choice"
                else key["ordered_ids"]
            )
            if (
                len(set(values)) != len(values)
                or not set(values) <= set(ids)
                or (kind == "ordering" and set(values) != set(ids))
            ):
                raise ValueError("Đáp án không thuộc các lựa chọn")
        self.grading = key
        return self


class ContentAction(StrictModel):
    expected_revision: int = Field(ge=1)
    reason: str = Field(min_length=5, max_length=500)


class AssessmentItemInput(StrictModel):
    question_version_id: UUID
    points: float = Field(default=1, gt=0, le=100, allow_inf_nan=False)


class AssessmentInput(StrictModel):
    code: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]+$")
    grade: int = Field(ge=1, le=5)
    subject_id: UUID
    topic_id: UUID
    lesson_id: UUID | None = None
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(default="", max_length=2000)
    assessment_type: Literal["practice", "homework", "quiz", "test"] = "practice"
    time_limit_seconds: int | None = Field(default=None, ge=60, le=7200)
    max_attempts: int = Field(default=5, ge=1, le=20)
    minimum_plan_code: Literal["free", "vip"] = "free"
    learning_level: Literal["basic", "reinforcement", "advanced"] = "basic"
    preview: PreviewInput = Field(default_factory=PreviewInput)
    items: list[AssessmentItemInput] = Field(min_length=1, max_length=50)
    expected_revision: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def unique_items(self):
        if len({item.question_version_id for item in self.items}) != len(self.items):
            raise ValueError("Không lặp câu trong cùng đề")
        return self


class CloneAssessment(StrictModel):
    code: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]+$")


class AssignmentInput(StrictModel):
    student_ids: list[UUID] = Field(min_length=1, max_length=50)
    available_at: datetime | None = None
    due_at: datetime | None = None

    @model_validator(mode="after")
    def dates(self):
        for value in (self.available_at, self.due_at):
            if value and value.tzinfo is None:
                raise ValueError("Cần múi giờ")
        if self.available_at and self.due_at and self.due_at <= self.available_at:
            raise ValueError("Hạn nộp phải sau giờ mở")
        if len(set(self.student_ids)) != len(self.student_ids):
            raise ValueError("Học sinh bị lặp")
        return self
