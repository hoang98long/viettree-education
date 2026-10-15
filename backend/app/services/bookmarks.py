"""Idempotent, account-scoped bookmarks. A bookmark never grants lesson access."""

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from app.db import db
from app.services import access
from app.services.attempts import lock_student


def is_bookmarked(conn, student_id, lesson_id):
    table = db.table("student_lesson_bookmarks")
    return (
        conn.execute(
            select(table.c.lesson_id).where(
                table.c.student_id == student_id, table.c.lesson_id == lesson_id
            )
        ).first()
        is not None
    )


def set_bookmark(conn, user, lesson_id, saved):
    profile = lock_student(conn, user["id"])
    table = db.table("student_lesson_bookmarks")
    if saved:
        lessons, topics, subjects = (db.table(name) for name in ("lessons", "topics", "subjects"))
        available = conn.execute(
            select(lessons.c.id)
            .select_from(lessons.join(topics).join(subjects, subjects.c.id == topics.c.subject_id))
            .where(
                lessons.c.id == lesson_id,
                lessons.c.status == "published",
                topics.c.grade == profile["current_grade"],
                topics.c.is_active.is_(True),
                subjects.c.is_active.is_(True),
            )
        ).first()
        if not available:
            raise HTTPException(404, "Không tìm thấy bài học trong lớp của em")
        access.authorize_content(conn, user, "lesson", lesson_id, profile["current_grade"])
        conn.execute(
            insert(table)
            .values(student_id=user["id"], lesson_id=lesson_id)
            .on_conflict_do_nothing(index_elements=[table.c.student_id, table.c.lesson_id])
        )
    else:
        # Removing an old/archived/out-of-grade bookmark must remain possible.
        conn.execute(
            delete(table).where(table.c.student_id == user["id"], table.c.lesson_id == lesson_id)
        )
    return {"saved": saved}
