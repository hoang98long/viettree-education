from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common import StrictModel

GAME_KINDS = [
    "classify",
    "match",
    "sequence",
    "train",
    "bias",
    "prompt",
    "fact_check",
    "hint_ladder",
    "comic",
    "roleplay",
]
AssetCode = Annotated[str, Field(pattern=r"^[A-Za-z0-9_-]{1,120}$")]


class Item(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9_-]{1,60}$")
    text: str = Field(min_length=1, max_length=500)
    answer: str = Field(min_length=1, max_length=100)
    asset: AssetCode | None = None


class Activity(StrictModel):
    kind: Literal[
        "classify",
        "match",
        "sequence",
        "train",
        "bias",
        "prompt",
        "fact_check",
        "hint_ladder",
        "comic",
        "roleplay",
    ]
    instruction: str = Field(min_length=10, max_length=1000)
    items: list[Item] = Field(min_length=2, max_length=20)
    choices: list[str] = Field(min_length=2, max_length=20)
    explanation: str = Field(min_length=10, max_length=2000)
    hints: list[str] = Field(default_factory=list, max_length=3)

    @model_validator(mode="after")
    def unique_ids(self):
        if len({item.id for item in self.items}) != len(self.items):
            raise ValueError("ID hoạt động phải khác nhau")
        if len(set(self.choices)) != len(self.choices) or any(
            item.answer not in self.choices for item in self.items
        ):
            raise ValueError("Đáp án phải nằm trong lựa chọn và không trùng lựa chọn")
        return self


class Question(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9_-]{1,60}$")
    prompt: str = Field(min_length=10, max_length=1000)
    options: list[str] = Field(min_length=2, max_length=6)
    answer: int = Field(ge=0, le=5)
    explanation: str = Field(min_length=10, max_length=1500)

    @model_validator(mode="after")
    def valid_answer(self):
        if self.answer >= len(self.options) or len(set(self.options)) != len(self.options):
            raise ValueError("Đáp án/lựa chọn câu hỏi không hợp lệ")
        return self


class Step(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9_-]{1,60}$")
    kind: Literal[
        "story",
        "illustrated_explanation",
        "flip_card",
        "interactive_diagram",
        "activity",
        "quiz",
        "reflection",
        "project_task",
        "audio",
    ]
    title: str = Field(min_length=1, max_length=160)
    text: str = Field(min_length=10, max_length=4000)
    details_text: str | None = Field(default=None, max_length=4000)
    media: list[AssetCode] = Field(default_factory=list, max_length=12)
    activity: Activity | None = None
    questions: list[Question] = Field(default_factory=list, max_length=6)

    @model_validator(mode="after")
    def matching_content(self):
        if len({question.id for question in self.questions}) != len(self.questions):
            raise ValueError("ID câu hỏi trong một bước phải khác nhau")
        if self.kind == "activity" and self.activity is None:
            raise ValueError("Bước thực hành phải có hoạt động")
        if self.kind == "quiz" and not self.questions:
            raise ValueError("Checkpoint phải có câu hỏi")
        return self


class HintInput(StrictModel):
    step_id: str = Field(pattern=r"^[a-z0-9_-]{1,60}$")
    level: int = Field(default=1, ge=1, le=3)


class LessonContent(StrictModel):
    title_override: str | None = Field(default=None, max_length=180)
    position_override: int | None = Field(default=None, ge=1, le=200)
    objectives: list[str] = Field(min_length=3, max_length=6)
    prerequisites: list[str] = Field(default_factory=list, max_length=12)
    estimated_minutes: int = Field(default=35, ge=5, le=60)
    keywords: list[str] = Field(min_length=2, max_length=12)
    age_range: list[int] = Field(min_length=2, max_length=2)
    competencies: list[str] = Field(min_length=1, max_length=9)
    teacher_guide: str = Field(min_length=30, max_length=6000)
    materials: list[str] = Field(min_length=1, max_length=12)
    misconceptions: str = Field(min_length=10, max_length=2000)
    safety_notes: str = Field(min_length=10, max_length=2000)
    support: str = Field(min_length=15, max_length=1500)
    standard: str = Field(min_length=15, max_length=1500)
    advanced: str = Field(min_length=15, max_length=2000)
    accessibility: dict = Field(
        default_factory=lambda: {"keyboard": True, "transcript": True, "no_camera": True}
    )
    steps: list[Step] = Field(min_length=5, max_length=8)
    hero: AssetCode
    cards: list[AssetCode] = Field(min_length=2, max_length=20)

    @model_validator(mode="after")
    def complete(self):
        if len({step.id for step in self.steps}) != len(self.steps):
            raise ValueError("ID bước học phải khác nhau")
        if (
            not any(step.kind == "activity" for step in self.steps)
            or sum(len(step.questions) for step in self.steps) < 3
        ):
            raise ValueError("Bài cần hoạt động và ít nhất 3 câu checkpoint")
        if (
            self.age_range[0] > self.age_range[1]
            or not 6 <= self.age_range[0] <= self.age_range[1] <= 12
        ):
            raise ValueError("Tuổi chưa phù hợp tiểu học")
        return self


class DraftInput(StrictModel):
    unit_id: UUID
    code: str = Field(pattern=r"^[A-Za-z0-9_-]{3,80}$")
    title: str = Field(min_length=3, max_length=180)
    position: int = Field(ge=1, le=200)
    revision: int | None = Field(default=None, ge=1)
    content: LessonContent


class RevisionInput(StrictModel):
    revision: int = Field(ge=1)


class StepInput(StrictModel):
    step_id: str = Field(max_length=60)


class AttemptInput(StepInput):
    idempotency_key: UUID
    level: int = Field(default=2, ge=1, le=3)
    answers: dict[str, str] = Field(max_length=20)

    @field_validator("answers")
    @classmethod
    def bounded_answers(cls, value):
        if any(len(key) > 60 or len(text) > 100 for key, text in value.items()):
            raise ValueError("Đáp án quá dài")
        return value


class TutorInput(StrictModel):
    lesson_id: UUID
    mode: Literal[
        "ExplainConcept",
        "GiveHint",
        "AskSocraticQuestion",
        "ReviewStudentDraft",
        "PracticeEnglish",
        "BrainstormStory",
    ]
    tried: str = Field(default="", max_length=500)
    level: int = Field(default=1, ge=1, le=3)


class AssignmentInput(StrictModel):
    class_id: UUID
    lesson_id: UUID


class SubmissionInput(StrictModel):
    project_id: UUID
    class_id: UUID | None = None
    revision: int | None = Field(default=None, ge=1)
    artifact: dict[str, str] = Field(max_length=11)
    submit: bool = False

    @field_validator("artifact")
    @classmethod
    def bounded_artifact(cls, value):
        if any(
            key
            not in {
                "title",
                "kind",
                "character",
                "setting",
                "problem",
                "solution",
                "reflection",
                "frame1",
                "frame2",
                "frame3",
                "frame4",
            }
            or len(text) > 1500
            for key, text in value.items()
        ):
            raise ValueError("Trường sản phẩm không hợp lệ")
        if value.get("kind", "comic") not in {"comic", "poster", "quiz", "classifier"}:
            raise ValueError("Loại sản phẩm không hợp lệ")
        return value


class ReviewInput(RevisionInput):
    feedback: str = Field(min_length=10, max_length=2000)
    scores: dict[Literal["understanding", "practice", "creativity", "safety"], int]

    @field_validator("scores")
    @classmethod
    def rubric_bounds(cls, value):
        if set(value) != {"understanding", "practice", "creativity", "safety"} or any(
            not 0 <= n <= 4 for n in value.values()
        ):
            raise ValueError("Cần đủ 4 tiêu chí, mỗi tiêu chí từ 0 đến 4")
        return value
