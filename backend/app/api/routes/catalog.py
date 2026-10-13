from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select

import app.schemas.catalog as schemas_catalog
from app.core.dependencies import database
from app.core.security import (
    current_user,
)
from app.curriculum.lesson_content import distribute_hints, enrich
from app.db import db
from app.schemas.common import Grade
from app.services import access

router = APIRouter(prefix="/api/v1")


@router.get("/grades", response_model=list[schemas_catalog.GradeResponse], tags=["curriculum"])
def grades(user=Depends(current_user), conn=database):
    topics, lessons, subjects = (db.table(name) for name in ("topics", "lessons", "subjects"))
    available = set(
        conn.execute(
            select(topics.c.grade)
            .distinct()
            .select_from(topics.join(lessons).join(subjects))
            .where(
                topics.c.is_active.is_(True),
                subjects.c.is_active.is_(True),
                lessons.c.status == "published",
            )
        ).scalars()
    )
    return [
        {
            "grade": grade,
            "status": "available" if grade in available else "building",
            "label": "Có thể học ngay" if grade in available else "Đang xây dựng",
        }
        for grade in range(1, 6)
    ]


@router.get("/subjects", response_model=list[schemas_catalog.SubjectResponse], tags=["curriculum"])
def subjects(grade: Grade = 4, user=Depends(current_user), conn=database):
    table, topics = db.table("subjects"), db.table("topics")
    rows = (
        conn.execute(
            select(
                table.c.id,
                table.c.code,
                table.c.name_vi,
                table.c.description,
                select(func.count())
                .where(
                    topics.c.subject_id == table.c.id,
                    topics.c.grade == grade,
                    topics.c.is_active.is_(True),
                )
                .scalar_subquery()
                .label("topic_count"),
            )
            .where(table.c.is_active.is_(True))
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )
    return [
        {**dict(row), "grade": grade, "status": "available" if row["topic_count"] else "building"}
        for row in rows
    ]


@router.get("/topics", response_model=list[schemas_catalog.TopicResponse], tags=["curriculum"])
def topics(
    grade: Grade = 4,
    subject_code: str = "MATH",
    user=Depends(current_user),
    conn=database,
):
    table, subjects = db.table("topics"), db.table("subjects")
    return (
        conn.execute(
            select(table)
            .join(subjects)
            .where(
                table.c.grade == grade, subjects.c.code == subject_code, table.c.is_active.is_(True)
            )
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )


@router.get(
    "/lessons", response_model=list[schemas_catalog.LessonSummaryResponse], tags=["curriculum"]
)
def lessons(topic_id: UUID, user=Depends(current_user), conn=database):
    table = db.table("lessons")
    topics = db.table("topics")
    grade = conn.execute(select(topics.c.grade).where(topics.c.id == topic_id)).scalar()
    rows = (
        conn.execute(
            select(
                table.c.id,
                table.c.topic_id,
                table.c.code,
                table.c.title,
                table.c.description,
                table.c.estimated_minutes,
                table.c.status,
            )
            .where(table.c.topic_id == topic_id, table.c.status == "published")
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )
    return [
        {**dict(row), **access.content_access(conn, user, "lesson", row["id"], grade)}
        for row in rows
    ]


@router.get(
    "/lessons/{lesson_id}", response_model=schemas_catalog.LessonResponse, tags=["curriculum"]
)
def lesson(lesson_id: UUID, user=Depends(current_user), conn=database):
    table, topics, subjects, assessments = (
        db.table(name) for name in ("lessons", "topics", "subjects", "assessments")
    )
    row = (
        conn.execute(
            select(
                table,
                topics.c.grade,
                topics.c.title.label("topic_title"),
                subjects.c.code.label("subject_code"),
                subjects.c.name_vi.label("subject_name"),
            )
            .select_from(table.join(topics).join(subjects))
            .where(
                table.c.id == lesson_id, table.c.status == "published", topics.c.is_active.is_(True)
            )
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài học")
    gate = access.authorize_content(conn, user, "lesson", lesson_id, row["grade"])
    practice = (
        conn.execute(
            select(assessments.c.id, assessments.c.title).where(
                assessments.c.topic_id == row["topic_id"], assessments.c.status == "published"
            )
        )
        .mappings()
        .all()
    )
    progress = db.table("student_lesson_progress")
    progress_status = (
        conn.execute(
            select(progress.c.status).where(
                progress.c.student_id == user["id"], progress.c.lesson_id == lesson_id
            )
        ).scalar()
        or "not_started"
    )
    practice = [
        dict(item)
        for item in practice
        if access.eligible(conn, user["id"], "assessment", item["id"], row["grade"])
        or "admin" in user["roles"]
    ]
    topic_code = conn.execute(
        select(topics.c.code).where(topics.c.id == row["topic_id"])
    ).scalar_one()
    candidates = conn.execute(
        select(table.c.id, table.c.title, progress.c.status.label("progress_status"))
        .select_from(
            table.outerjoin(
                progress,
                (progress.c.lesson_id == table.c.id) & (progress.c.student_id == user["id"]),
            )
        )
        .where(
            table.c.topic_id == row["topic_id"],
            table.c.status == "published",
            table.c.id != lesson_id,
            (progress.c.status.is_(None) | (progress.c.status != "completed")),
        )
        .order_by(table.c.sort_order, table.c.id)
    ).mappings()
    membership = access.resolve_membership(conn, user["id"]) if "student" in user["roles"] else None
    next_lessons = []
    for candidate in candidates:
        if not access.content_access(
            conn, user, "lesson", candidate["id"], row["grade"], membership
        )["locked"]:
            next_lessons.append(
                {
                    "id": candidate["id"],
                    "title": candidate["title"],
                    "reason": "Cùng chủ đề, em chưa đánh dấu đọc xong.",
                }
            )
        if len(next_lessons) == 3:
            break
    content, hint_access = distribute_hints(enrich(row["content"], topic_code), user, membership)
    return {
        **dict(row),
        **gate,
        "content": content,
        "hint_access": hint_access,
        "practice": practice,
        "progress_status": progress_status,
        "next_lessons": next_lessons,
    }
