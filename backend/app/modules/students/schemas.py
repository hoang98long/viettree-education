from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class StudentProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str
    student_id: UUID | None = None
    grade_id: UUID | None = None
    total_xp: int = 0
    stars: int = 0
    level: int = 1
    streak_days: int = 0

    model_config = ConfigDict(from_attributes=True)


class StudentDashboardResponse(BaseModel):
    student_id: UUID | None = None
    full_name: str
    total_xp: int = 0
    stars: int = 0
    streak_days: int = 0
    level: int = 1
    next_goal: str = "Hoàn thành 2 bài học hôm nay"
    continue_lesson: str = "Phép cộng trong phạm vi 10"
    subjects: list[str] = []

    model_config = ConfigDict(from_attributes=True)
