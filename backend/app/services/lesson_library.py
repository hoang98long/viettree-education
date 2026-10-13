"""Published lesson metadata for a student's own grade, with accent-aware search."""

import unicodedata

from sqlalchemy import func, or_, select

from app.db import db
from app.services import access
from app.services.vip import profile

ACCENTS = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"


def fold(value):
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value.lower().replace("đ", "d"))
        if not unicodedata.combining(char)
    )


BASE_LETTERS = "".join(fold(char) for char in ACCENTS)


def lesson_library(
    conn, user, subject_code=None, plan="all", progress="all", category="all", search="", page=1
):
    grade = profile(conn, user["id"])
    lessons, topics, subjects, policies, progress_rows = (
        db.table(name)
        for name in (
            "lessons",
            "topics",
            "subjects",
            "content_access_policies",
            "student_lesson_progress",
        )
    )
    progress_status = func.coalesce(progress_rows.c.status, "not_started")
    category_value = func.coalesce(lessons.c.content["category"].astext, "core")
    scope = (
        lessons.join(topics)
        .join(subjects, subjects.c.id == topics.c.subject_id)
        .outerjoin(policies, policies.c.lesson_id == lessons.c.id)
        .outerjoin(
            progress_rows,
            (progress_rows.c.lesson_id == lessons.c.id)
            & (progress_rows.c.student_id == user["id"]),
        )
    )
    predicates = [
        topics.c.grade == grade,
        topics.c.is_active.is_(True),
        subjects.c.is_active.is_(True),
        lessons.c.status == "published",
    ]
    if subject_code:
        predicates.append(subjects.c.code == subject_code)
    if plan != "all":
        predicates.append(policies.c.minimum_plan_code == plan)
    if progress != "all":
        predicates.append(progress_status == progress)
    if category != "all":
        predicates.append(category_value == category)
    search = fold(search.strip())
    if search:
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        predicates.append(
            or_(
                *[
                    func.translate(func.lower(column), ACCENTS, BASE_LETTERS).like(
                        "%" + escaped + "%", escape="\\"
                    )
                    for column in (lessons.c.title, topics.c.title)
                ]
            )
        )
    totals = (
        conn.execute(
            select(
                func.count().label("total"),
                func.count().filter(progress_status == "completed").label("completed"),
                func.count().filter(progress_status == "in_progress").label("in_progress"),
                func.count().filter(policies.c.minimum_plan_code == "free").label("free"),
                func.count().filter(policies.c.minimum_plan_code == "vip").label("vip"),
            )
            .select_from(scope)
            .where(*predicates)
        )
        .mappings()
        .one()
    )
    rows = (
        conn.execute(
            select(
                lessons.c.id,
                lessons.c.title,
                lessons.c.estimated_minutes,
                topics.c.title.label("topic_title"),
                subjects.c.code.label("subject_code"),
                subjects.c.name_vi.label("subject_name"),
                progress_status.label("progress_status"),
                category_value.label("category"),
            )
            .select_from(scope)
            .where(*predicates)
            .order_by(
                subjects.c.sort_order,
                topics.c.sort_order,
                lessons.c.sort_order,
                lessons.c.id,
            )
            .offset((page - 1) * 12)
            .limit(12)
        )
        .mappings()
        .all()
    )
    membership = access.resolve_membership(conn, user["id"])
    items = [
        {**dict(row), **access.content_access(conn, user, "lesson", row["id"], grade, membership)}
        for row in rows
    ]
    return {"grade": grade, "page": page, "page_size": 12, "summary": dict(totals), "items": items}
