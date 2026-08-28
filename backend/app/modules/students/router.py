from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.learning import Grade, Student, Subject
from app.models.user import User
from app.modules.auth.router import get_current_user
from app.modules.students.schemas import StudentDashboardResponse, StudentProfileResponse

router = APIRouter(prefix="/students", tags=["Học sinh"])


@router.get("/me", response_model=StudentProfileResponse)
def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.scalar(select(Student).where(Student.user_id == user.id))
    grade_value = student.grade if student else None

    return StudentProfileResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        student_id=student.id if student else None,
        grade_id=grade_value,
        total_xp=student.total_xp if student else 0,
        stars=student.stars if student else 0,
        level=student.level if student else 1,
        streak_days=student.streak_days if student else 0,
    )


@router.get("/me/dashboard", response_model=StudentDashboardResponse)
def get_dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.scalar(select(Student).where(Student.user_id == user.id))
    subjects = db.scalars(select(Subject).where(Subject.is_active.is_(True)).order_by(Subject.name)).all()
    subject_names = [item.name for item in subjects[:3]]

    return StudentDashboardResponse(
        student_id=student.id if student else None,
        full_name=user.full_name,
        total_xp=student.total_xp if student else 0,
        stars=student.stars if student else 0,
        streak_days=student.streak_days if student else 0,
        level=student.level if student else 1,
        next_goal="Hoàn thành 2 bài học hôm nay",
        continue_lesson="Phép cộng trong phạm vi 10",
        subjects=subject_names,
    )
