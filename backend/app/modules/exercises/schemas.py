from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OptionOut(BaseModel):
    id: UUID
    option_text: str
    option_value: str | None = None
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class QuestionOut(BaseModel):
    id: UUID
    question_type: str
    question_text: str
    hint: str | None = None
    difficulty: str
    points: int
    display_order: int
    options: list[OptionOut] = []


class ExerciseOut(BaseModel):
    id: UUID
    lesson_id: UUID
    title: str | None = None
    description: str | None = None
    difficulty: str
    points: int
    questions: list[QuestionOut] = []


class ExerciseSummary(BaseModel):
    id: UUID
    lesson_id: UUID
    title: str | None = None
    description: str | None = None
    difficulty: str
    points: int

    model_config = ConfigDict(from_attributes=True)


class AnswerInput(BaseModel):
    question_id: UUID
    answer_text: str | None = Field(default=None, max_length=2000)
    selected_option_ids: list[UUID] = []


class SubmitExerciseRequest(BaseModel):
    answers: list[AnswerInput]


class QuestionResult(BaseModel):
    question_id: UUID
    is_correct: bool
    score: float
    max_score: int
    explanation: str | None = None


class ExerciseResult(BaseModel):
    attempt_id: UUID
    score: float
    max_score: float
    correct_count: int
    total_questions: int
    results: list[QuestionResult]
