from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.auth import UserResponse
from app.schemas.catalog import AssignmentResponse, SubjectResponse
from app.schemas.common import DeviceType, Grade, StrictModel, TextSize


class AccessibilityInput(StrictModel):
    text_size: TextSize
    device_type: DeviceType | None = None


class LearningPlanInput(StrictModel):
    subject_code: str = Field(min_length=1, max_length=30)
    mode: Literal["basic", "adaptive"] = "basic"


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


class ProfileResponse(UserResponse):
    current_grade: Grade
    learning_preferences: dict
    accessibility_options: dict
