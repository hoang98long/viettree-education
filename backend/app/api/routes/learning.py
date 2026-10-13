from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

import app.schemas.learning as schemas_learning
from app.api.routes.assessments import assignments
from app.api.routes.catalog import lesson, subjects
from app.core.dependencies import database
from app.core.security import (
    now,
    public_user,
    student_user,
)
from app.db import db
from app.personalization.engine import recommendations
from app.schemas.common import ReadingPreferences
from app.services import access, learning
from app.services import attempts as service
from app.services.accessibility import merge_text_size, reading_preferences

router = APIRouter(prefix="/api/v1")


@router.put(
    "/students/me/accessibility",
    response_model=ReadingPreferences,
    tags=["student"],
)
def accessibility(
    payload: schemas_learning.AccessibilityInput,
    user=Depends(student_user),
    conn=database,
):
    profile = service.lock_student(conn, user["id"])
    profiles = db.table("student_profiles")
    options = merge_text_size(
        profile["accessibility_options"], payload.text_size, payload.device_type
    )
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == user["id"])
        .values(
            accessibility_options=options,
            updated_at=now(),
        )
    )
    return reading_preferences(options)


@router.get(
    "/students/me/learning-plans",
    response_model=list[schemas_learning.LearningPlanResponse],
    tags=["student"],
)
def learning_plans(user=Depends(student_user), conn=database):
    profiles = db.table("student_profiles")
    grade = conn.execute(
        select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
    ).scalar_one()
    return learning.list_plans(conn, user["id"], grade)


@router.post(
    "/students/me/learning-plans",
    response_model=schemas_learning.LearningPlanResponse,
    tags=["student"],
)
def create_learning_plan(
    payload: schemas_learning.LearningPlanInput,
    user=Depends(student_user),
    conn=database,
):
    profile = service.lock_student(conn, user["id"])
    return learning.create_plan(
        conn, user["id"], profile["current_grade"], payload.subject_code, payload.mode
    )


@router.post("/lessons/{lesson_id}/visit", response_model=dict[str, bool], tags=["student"])
def visit_lesson(lesson_id: UUID, user=Depends(student_user), conn=database):
    profile = service.lock_student(conn, user["id"])
    record = lesson(lesson_id, user, conn)
    if record["grade"] != profile["current_grade"]:
        raise HTTPException(403, "Bài học không thuộc lớp của em")
    table = db.table("student_lesson_progress")
    statement = insert(table).values(
        student_id=user["id"],
        lesson_id=lesson_id,
        status="in_progress",
        first_started_at=now(),
        last_accessed_at=now(),
    )
    conn.execute(
        statement.on_conflict_do_update(
            index_elements=[table.c.student_id, table.c.lesson_id], set_={"last_accessed_at": now()}
        )
    )
    learning.update_targets(conn, user["id"], lesson_id=lesson_id, completed=False)
    return {"visited": True}


@router.post("/lessons/{lesson_id}/complete", response_model=dict[str, bool], tags=["student"])
def complete_lesson(lesson_id: UUID, user=Depends(student_user), conn=database):
    profile = service.lock_student(conn, user["id"])
    record = lesson(lesson_id, user, conn)
    if record["grade"] != profile["current_grade"]:
        raise HTTPException(403, "Bài học không thuộc lớp của em")
    progress = db.table("student_lesson_progress")
    at = now()
    statement = insert(progress).values(
        student_id=user["id"],
        lesson_id=lesson_id,
        status="completed",
        completion_ratio=1,
        first_started_at=at,
        completed_at=at,
        last_accessed_at=at,
    )
    conn.execute(
        statement.on_conflict_do_update(
            index_elements=[progress.c.student_id, progress.c.lesson_id],
            set_={
                "status": "completed",
                "completion_ratio": 1,
                "completed_at": func.coalesce(progress.c.completed_at, at),
                "last_accessed_at": at,
                "updated_at": at,
            },
        )
    )
    if record["progress_status"] != "completed":
        conn.execute(
            db.table("learning_events")
            .insert()
            .values(
                student_id=user["id"],
                event_type="lesson_completed",
                properties={"source": "student_read_confirmation", "lesson_id": str(lesson_id)},
            )
        )
    learning.update_targets(conn, user["id"], lesson_id=lesson_id)
    return {"completed": True}


@router.get(
    "/students/me/history", response_model=list[schemas_learning.HistoryResponse], tags=["student"]
)
def history(
    subject_code: str | None = None,
    date: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    user=Depends(student_user),
    conn=database,
):
    attempts, assessments, subjects = (
        db.table(name) for name in ("attempts", "assessments", "subjects")
    )
    statement = (
        select(
            attempts.c.id,
            attempts.c.status,
            attempts.c.total_score,
            attempts.c.max_score,
            attempts.c.started_at,
            attempts.c.graded_at,
            assessments.c.title,
            subjects.c.name_vi.label("subject_name"),
            subjects.c.code.label("subject_code"),
        )
        .select_from(
            attempts.join(assessments, attempts.c.assessment_id == assessments.c.id).join(subjects)
        )
        .where(attempts.c.student_id == user["id"])
    )
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    if date:
        statement = statement.where(
            func.to_char(func.timezone("Asia/Bangkok", attempts.c.started_at), "YYYY-MM-DD") == date
        )
    return (
        conn.execute(statement.order_by(attempts.c.started_at.desc()).limit(200)).mappings().all()
    )


@router.get(
    "/students/me/skills", response_model=list[schemas_learning.SkillResponse], tags=["student"]
)
def skill_progress(user=Depends(student_user), conn=database):
    mastery, skills, subjects = (
        db.table(name) for name in ("student_skill_mastery", "skills", "subjects")
    )
    return (
        conn.execute(
            select(mastery, skills.c.name, subjects.c.name_vi.label("subject_name"))
            .select_from(mastery.join(skills).join(subjects))
            .where(mastery.c.student_id == user["id"])
            .order_by(mastery.c.mastery_score)
        )
        .mappings()
        .all()
    )


@router.get(
    "/students/me/recommendations",
    response_model=list[schemas_learning.RecommendationResponse],
    tags=["student"],
)
def recommended(user=Depends(student_user), conn=database):
    profile = service.lock_student(conn, user["id"])
    return recommendations(conn, user["id"], profile["current_grade"])


@router.get(
    "/students/me/dashboard", response_model=schemas_learning.DashboardResponse, tags=["student"]
)
def dashboard(user=Depends(student_user), conn=database):
    profile = service.lock_student(conn, user["id"])
    progress, lessons = db.table("student_lesson_progress"), db.table("lessons")
    continue_lesson = (
        conn.execute(
            select(lessons.c.id, lessons.c.title)
            .select_from(progress.join(lessons))
            .where(
                progress.c.student_id == user["id"],
                progress.c.status == "in_progress",
                lessons.c.status == "published",
            )
            .order_by(progress.c.last_accessed_at.desc())
            .limit(1)
        )
        .mappings()
        .first()
    )
    if continue_lesson and not access.eligible(
        conn, user["id"], "lesson", continue_lesson["id"], profile["current_grade"]
    ):
        continue_lesson = None
    return dict(
        user={**public_user(user), **reading_preferences(profile["accessibility_options"])},
        grade=profile["current_grade"],
        subjects=subjects(profile["current_grade"], user, conn),
        history=history(None, None, user, conn),
        skills=skill_progress(user, conn),
        recommendations=recommendations(conn, user["id"], profile["current_grade"]),
        assignments=assignments(user, conn),
        continue_lesson=continue_lesson,
        completed_lessons=conn.execute(
            select(func.count())
            .select_from(progress)
            .where(progress.c.student_id == user["id"], progress.c.status == "completed")
        ).scalar_one(),
    )


@router.get(
    "/students/me/profile", response_model=schemas_learning.ProfileResponse, tags=["student"]
)
def profile(user=Depends(student_user), conn=database):
    table = db.table("student_profiles")
    row = (
        conn.execute(
            select(
                table.c.current_grade, table.c.learning_preferences, table.c.accessibility_options
            ).where(table.c.student_id == user["id"])
        )
        .mappings()
        .one()
    )
    return {**public_user(user), **dict(row), **reading_preferences(row["accessibility_options"])}
