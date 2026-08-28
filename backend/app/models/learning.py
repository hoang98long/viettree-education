import enum
from uuid import UUID
from sqlalchemy import Enum, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDTimestampMixin


class PublishStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Subject(Base, UUIDTimestampMixin):
    __tablename__ = "subjects"
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80), index=True)
    color: Mapped[str] = mapped_column(String(16), default="#2F855A")
    is_active: Mapped[bool] = mapped_column(default=True)


class Grade(Base, UUIDTimestampMixin):
    __tablename__ = "grades"
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(40))


class Course(Base, UUIDTimestampMixin):
    __tablename__ = "courses"
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), index=True)
    grade_id: Mapped[UUID] = mapped_column(ForeignKey("grades.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    status: Mapped[PublishStatus] = mapped_column(
        Enum(PublishStatus, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=PublishStatus.DRAFT,
    )
    position: Mapped[int] = mapped_column(Integer, default=0)


class Lesson(Base, UUIDTimestampMixin):
    __tablename__ = "lessons"
    __table_args__ = (UniqueConstraint("course_id", "position", name="uq_lesson_course_position"),)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[PublishStatus] = mapped_column(
        Enum(PublishStatus, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=PublishStatus.DRAFT,
    )
    position: Mapped[int] = mapped_column(Integer, default=0)


class LessonContent(Base, UUIDTimestampMixin):
    __tablename__ = "lesson_contents"
    __table_args__ = (UniqueConstraint("lesson_id", "position", name="uq_block_lesson_position"),)
    lesson_id: Mapped[UUID] = mapped_column(ForeignKey("lessons.id"), index=True)
    block_type: Mapped[str] = mapped_column(String(48))
    position: Mapped[int] = mapped_column(Integer)
    data: Mapped[dict] = mapped_column(JSON)


class Student(Base, UUIDTimestampMixin):
    __tablename__ = "students"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    date_of_birth: Mapped[str | None] = mapped_column(nullable=True)
    grade: Mapped[int] = mapped_column(default=1)
    school_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    xp: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)
    current_streak: Mapped[int] = mapped_column(default=0)
    longest_streak: Mapped[int] = mapped_column(default=0)
    last_learning_date: Mapped[str | None] = mapped_column(nullable=True)

    @property
    def grade_id(self):
        return self.grade

    @property
    def total_xp(self) -> int:
        return self.xp

    @property
    def stars(self) -> int:
        return 0

    @property
    def streak_days(self) -> int:
        return self.current_streak
