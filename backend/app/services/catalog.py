"""Shared catalogue lookups; routes and write services own authorization."""

from fastapi import HTTPException
from sqlalchemy import func, select

from app.db import db


def published_lesson(conn, lesson_id, student_id, *, detail=False):
    """Use the same visibility and owner-scoped progress for read/write paths.

    Progress updates need only identity, grade and prior status. Do not read
    lesson JSON, resolve related practice or render hints on that hot path.
    """
    lessons, topics, subjects, progress = (
        db.table(name) for name in ("lessons", "topics", "subjects", "student_lesson_progress")
    )
    columns = [lessons if detail else lessons.c.id, topics.c.grade]
    if detail:
        columns.extend(
            [
                topics.c.title.label("topic_title"),
                subjects.c.code.label("subject_code"),
                subjects.c.name_vi.label("subject_name"),
            ]
        )
    columns.append(
        func.coalesce(
            select(progress.c.status)
            .where(progress.c.student_id == student_id, progress.c.lesson_id == lessons.c.id)
            .scalar_subquery(),
            "not_started",
        ).label("progress_status")
    )
    row = (
        conn.execute(
            select(*columns)
            .select_from(lessons.join(topics).join(subjects))
            .where(
                lessons.c.id == lesson_id,
                lessons.c.status == "published",
                topics.c.is_active.is_(True),
            )
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài học")
    return row


def assessment_list(conn, grade, subject_code=None, published_only=True):
    table, items, subjects = (
        db.table(name) for name in ("assessments", "assessment_items", "subjects")
    )
    statement = select(
        table.c.id,
        table.c.code,
        table.c.title,
        table.c.description,
        table.c.grade,
        table.c.status,
        table.c.lesson_id,
        table.c.topic_id,
        table.c.max_attempts,
        table.c.time_limit_seconds,
        table.c.assessment_type,
        subjects.c.code.label("subject_code"),
        subjects.c.name_vi.label("subject_name"),
        select(func.count())
        .where(items.c.assessment_id == table.c.id)
        .scalar_subquery()
        .label("item_count"),
    )
    statement = statement.select_from(table.join(subjects)).where(table.c.grade == grade)
    if published_only:
        statement = statement.where(table.c.status == "published")
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    return conn.execute(statement.order_by(table.c.code)).mappings().all()
