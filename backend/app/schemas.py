from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LoginInput(StrictModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=1, max_length=256)


class UserResponse(BaseModel):
    id: UUID
    username: str
    display_name: str
    roles: list[str]
    text_size: Literal["comfortable", "large"] = "comfortable"


class AccessibilityInput(StrictModel):
    text_size: Literal["comfortable", "large"]


class LearningPlanInput(StrictModel):
    subject_code: str = Field(min_length=1, max_length=30)
    mode: Literal["basic", "adaptive"] = "basic"


class MembershipGrantInput(StrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    duration_days: Literal[30, 90, 365]
    reason: str = Field(min_length=5, max_length=500)


class MembershipRevokeInput(StrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    reason: str = Field(min_length=5, max_length=500)


class MembershipResponse(BaseModel):
    student_id: UUID
    plan_code: Literal["free", "vip"]
    status: Literal["free", "active", "expired", "revoked"]
    subscription_plan_code: str | None
    starts_at: datetime | None
    ends_at: datetime | None
    features: list[str]


class MembershipPlanResponse(BaseModel):
    code: str
    name: str
    features: list[str]


class PreviewInput(StrictModel):
    summary: str = Field(default="", max_length=350)
    goals: list[Annotated[str, Field(max_length=120)]] = Field(default_factory=list, max_length=5)


class ContentPolicyInput(StrictModel):
    minimum_plan_code: Literal["free", "vip"]
    learning_level: Literal["basic", "reinforcement", "advanced"]
    preview: PreviewInput
    reason: str = Field(min_length=5, max_length=500)


class CatalogAccess(BaseModel):
    minimum_plan_code: Literal["free", "vip"] | None = None
    learning_level: Literal["basic", "reinforcement", "advanced"] = "basic"
    locked: bool = False
    lock_reason: str | None = None


class PlanItemResponse(BaseModel):
    id: UUID
    position: int
    lesson_id: UUID | None
    assessment_id: UUID | None
    title: str
    status: str
    due_at: datetime | None
    completed_at: datetime | None
    locked: bool = False
    lock_reason: str | None = None


class LearningPlanResponse(BaseModel):
    id: UUID
    title: str
    subject_code: str
    subject_name: str
    status: str
    start_date: date | None
    end_date: date | None
    completed_count: int
    items: list[PlanItemResponse]
    mode: Literal["basic", "adaptive"] = "basic"
    explanation: str = ""


class StartInput(StrictModel):
    assignment_id: UUID


class ChoiceAnswer(StrictModel):
    option_id: str = Field(max_length=100)


class MultipleAnswer(StrictModel):
    option_ids: list[str] = Field(max_length=30)


class BlankAnswer(StrictModel):
    text: str = Field(max_length=500)


class OrderAnswer(StrictModel):
    ordered_ids: list[str] = Field(max_length=30)


class TextAnswer(StrictModel):
    text: str = Field(max_length=5000)


class AnswerInput(StrictModel):
    answer: dict
    response_time_ms: int | None = Field(default=None, ge=0, le=86400000)


class StudentUpdate(StrictModel):
    display_name: str = Field(min_length=1, max_length=160)
    current_grade: int = Field(ge=1, le=5)


class PublicContent(BaseModel):
    prompt: str
    options: list[dict[str, str]] = Field(default_factory=list)


class AttemptItem(BaseModel):
    id: UUID
    question_version_id: UUID
    position: int
    points: float
    question_type: str
    content: PublicContent
    answer: dict | None = None


class AttemptResponse(BaseModel):
    id: UUID
    assignment_id: UUID
    assessment_id: UUID
    title: str
    status: Literal["in_progress", "submitted", "graded", "abandoned"]
    started_at: str
    deadline: str | None
    items: list[AttemptItem]


Grade = Annotated[int, Field(ge=1, le=5)]


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
    content: dict
    grade: Grade
    topic_title: str
    subject_code: str
    subject_name: str
    practice: list[dict]
    progress_status: Literal["not_started", "in_progress", "completed"] = "not_started"


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


class HistoryResponse(BaseModel):
    id: UUID
    status: str
    total_score: float
    max_score: float
    started_at: datetime
    graded_at: datetime | None
    title: str
    subject_name: str
    subject_code: str


class SkillResponse(BaseModel):
    skill_id: UUID
    name: str
    subject_name: str
    mastery_score: float
    confidence: float
    questions_attempted: int
    correct_count: int
    recent_accuracy: float | None
    hint_usage_rate: float | None
    last_practiced_at: datetime | None
    next_review_at: datetime | None
    model_version: str


class RecommendationResponse(BaseModel):
    assessment_id: UUID
    title: str
    explanation: str
    reason_code: str


class DashboardResponse(BaseModel):
    user: UserResponse
    grade: Grade
    subjects: list[SubjectResponse]
    history: list[HistoryResponse]
    skills: list[SkillResponse]
    recommendations: list[RecommendationResponse]
    assignments: list[AssignmentResponse]
    continue_lesson: dict | None
    completed_lessons: int


class ResultItem(BaseModel):
    id: UUID
    position: int
    content: PublicContent
    question_type: str
    student_answer: dict
    is_correct: bool | None
    score: float
    points: float
    explanation: dict
    grading: dict


class ResultResponse(BaseModel):
    id: UUID
    total_score: float
    max_score: float
    correct_count: int
    answered_count: int
    graded_at: datetime
    items: list[ResultItem]


class StatisticsResponse(BaseModel):
    students: int
    users: int
    lessons: int
    question_versions: int
    assessments: int
    attempts: int
    average_percent: float | None
    correct_answers: int


class ProfileResponse(UserResponse):
    current_grade: Grade
    learning_preferences: dict
    accessibility_options: dict


class StartResponse(BaseModel):
    id: UUID
    resumed: bool


class StudentResponse(BaseModel):
    id: UUID
    username: str
    display_name: str
    is_active: bool
    current_grade: Grade


class StudentPageResponse(BaseModel):
    total: int
    page: int
    items: list[StudentResponse]


class QuestionResponse(BaseModel):
    id: UUID
    code: str
    grade: Grade
    question_type: str
    difficulty: int
    status: str
    subject_name: str
    content: PublicContent
    question_id: UUID | None = None
    version: int = 1
    reviewed_by: UUID | None = None
    minimum_plan_code: Literal["free", "vip"] | None = None


class QuestionPageResponse(BaseModel):
    total: int
    page: int
    items: list[QuestionResponse]
