import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, Integer, String, Text, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import UUIDTimestampMixin


class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    NUMERIC = "numeric"
    MATCHING = "matching"


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Exercise(Base, UUIDTimestampMixin):
    __tablename__ = "exercises"
    lesson_id: Mapped[UUID] = mapped_column(ForeignKey("lessons.id"), index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=Difficulty.EASY,
    )
    points: Mapped[int] = mapped_column(Integer, default=1)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)


class Question(Base, UUIDTimestampMixin):
    __tablename__ = "questions"
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id"), index=True)
    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, values_callable=lambda enum_cls: [member.value for member in enum_cls])
    )
    question_text: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=Difficulty.EASY,
    )
    points: Mapped[int] = mapped_column(Integer, default=1)
    display_order: Mapped[int] = mapped_column(Integer, default=0)


class QuestionOption(Base):
    __tablename__ = "question_options"
    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), index=True)
    option_text: Mapped[str] = mapped_column(Text)
    option_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_correct: Mapped[bool] = mapped_column(default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"
    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), index=True)
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id"), index=True)
    status: Mapped[AttemptStatus] = mapped_column(
        Enum(
            AttemptStatus,
            name="attempt_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=AttemptStatus.IN_PROGRESS,
    )
    score: Mapped[float | None] = mapped_column(nullable=True)
    max_score: Mapped[float | None] = mapped_column(nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    time_spent_seconds: Mapped[int | None] = mapped_column(nullable=True)


class AnswerSubmission(Base):
    __tablename__ = "answer_submissions"
    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("exercise_attempts.id"), index=True)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), index=True)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    selected_option_ids: Mapped[list[UUID] | None] = mapped_column(ARRAY(SQLUUID), nullable=True)
    is_correct: Mapped[bool | None] = mapped_column(nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
