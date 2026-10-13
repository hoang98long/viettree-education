"""Shared assessment catalogue query; routes own authorization."""

from sqlalchemy import func, select

from app.db import db


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
