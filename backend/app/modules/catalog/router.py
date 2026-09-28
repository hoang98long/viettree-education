from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.learning import Course, Grade, Lesson, Subject
from app.modules.catalog.schemas import CourseDetailOut, CourseOut, LessonOut, SubjectOut

router = APIRouter(prefix="/catalog", tags=["Danh mục"])


@router.get("/subjects", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.scalars(select(Subject).where(Subject.is_active.is_(True)).order_by(Subject.display_order, Subject.name)).all()
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
def list_courses(subject_id: UUID | None = None, grade: int | None = None, db: Session = Depends(get_db)):
    query = select(Course).where(Course.is_published.is_(True))
    if subject_id:
        query = query.where(Course.subject_id == subject_id)
    if grade:
        query = query.where(Course.grade == grade)
    courses = db.scalars(query.order_by(Course.display_order, Course.title)).all()
    return courses


@router.get("/courses/{course_id}", response_model=CourseDetailOut)
def get_course(course_id: UUID, db: Session = Depends(get_db)):
    course_model = db.scalar(
        select(Course).where(Course.id == course_id, Course.is_published.is_(True))
    )
    if not course_model:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại")
    subject = db.get(Subject, course_model.subject_id)
    if not subject or not subject.is_active:
        raise HTTPException(status_code=404, detail="Môn học không tồn tại")
    return CourseDetailOut(
        id=course_model.id,
        subject_id=course_model.subject_id,
        grade=course_model.grade,
        title=course_model.title,
        description=course_model.description,
        thumbnail_url=course_model.thumbnail_url,
        display_order=course_model.display_order,
        is_published=course_model.is_published,
        subject_name=subject.name,
    )


@router.get("/courses/{course_id}/lessons", response_model=list[LessonOut])
def list_lessons(course_id: UUID, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    lessons = db.scalars(
        select(Lesson)
        .where(Lesson.course_id == course_id, Lesson.is_published.is_(True))
        .order_by(Lesson.lesson_number, Lesson.title)
    ).all()
    return lessons
