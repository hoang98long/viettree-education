from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.learning import Course, Grade, Lesson, Subject
from app.modules.catalog.schemas import CourseOut, LessonOut, SubjectOut

router = APIRouter(prefix="/catalog", tags=["Danh mục"])


@router.get("/subjects", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.scalars(select(Subject).where(Subject.is_active.is_(True)).order_by(Subject.name)).all()
    return subjects


@router.get("/subjects/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: UUID, db: Session = Depends(get_db)):
    subject = db.get(Subject, subject_id)
    if not subject or not subject.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Môn học không tồn tại")
    return subject


@router.get("/grades", response_model=list[dict])
def list_grades(db: Session = Depends(get_db)):
    grades = db.scalars(select(Grade).order_by(Grade.name)).all()
    return [{"id": grade.id, "code": grade.code, "name": grade.name} for grade in grades]


@router.get("/courses", response_model=list[CourseOut])
def list_courses(subject_id: UUID | None = None, grade_id: UUID | None = None, db: Session = Depends(get_db)):
    query = select(Course)
    if subject_id:
        query = query.where(Course.subject_id == subject_id)
    if grade_id:
        query = query.where(Course.grade_id == grade_id)
    courses = db.scalars(query.order_by(Course.position, Course.title)).all()
    return courses


@router.get("/courses/{course_id}/lessons", response_model=list[LessonOut])
def list_lessons(course_id: UUID, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    lessons = db.scalars(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.position, Lesson.title)).all()
    return lessons
