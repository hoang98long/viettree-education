"""Published lesson metadata for a student's own grade, with accent-aware search."""

import unicodedata

from sqlalchemy import func, or_, select, true

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
    conn,
    user,
    subject_code=None,
    plan="all",
    progress="all",
    category="all",
    search="",
    page=1,
    bookmarked_only=False,
):
    grade = profile(conn, user["id"])
    lessons, topics, subjects, policies, progress_rows, bookmarks = (
        db.table(name)
        for name in (
            "lessons",
            "topics",
            "subjects",
            "content_access_policies",
            "student_lesson_progress",
            "student_lesson_bookmarks",
        )
    )
    progress_status = func.coalesce(progress_rows.c.status, "not_started")
    category_value = func.coalesce(lessons.c.content["category"].astext, "core")
    bookmarked = bookmarks.c.lesson_id.is_not(None)
    scope = (
        lessons.join(topics)
        .join(subjects, subjects.c.id == topics.c.subject_id)
        .outerjoin(policies, policies.c.lesson_id == lessons.c.id)
        .outerjoin(
            progress_rows,
            (progress_rows.c.lesson_id == lessons.c.id)
            & (progress_rows.c.student_id == user["id"]),
        )
        .outerjoin(
            bookmarks,
            (bookmarks.c.lesson_id == lessons.c.id) & (bookmarks.c.student_id == user["id"]),
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
    if bookmarked_only:
        predicates.append(bookmarked)
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
    # One PostgreSQL statement gives the count and page the same MVCC snapshot.
    # Progress can otherwise change between COUNT and SELECT under READ COMMITTED.
    filtered = (
        select(
            lessons.c.id,
            lessons.c.title,
            lessons.c.estimated_minutes,
            topics.c.title.label("topic_title"),
            subjects.c.code.label("subject_code"),
            subjects.c.name_vi.label("subject_name"),
            progress_status.label("progress_status"),
            category_value.label("category"),
            bookmarked.label("is_bookmarked"),
            policies.c.minimum_plan_code,
            subjects.c.sort_order.label("subject_order"),
            topics.c.sort_order.label("topic_order"),
            lessons.c.sort_order.label("lesson_order"),
        )
        .select_from(scope)
        .where(*predicates)
        .cte("library_filtered")
    )
    counts = (
        select(
            func.count().label("total"),
            func.count().filter(filtered.c.progress_status == "completed").label("completed"),
            func.count().filter(filtered.c.progress_status == "in_progress").label("in_progress"),
            func.count().filter(filtered.c.minimum_plan_code == "free").label("free"),
            func.count().filter(filtered.c.minimum_plan_code == "vip").label("vip"),
            func.count().filter(filtered.c.is_bookmarked).label("bookmarked"),
        )
        .select_from(filtered)
        .subquery("library_counts")
    )
    fields = [
        "id",
        "title",
        "estimated_minutes",
        "topic_title",
        "subject_code",
        "subject_name",
        "progress_status",
        "category",
        "is_bookmarked",
    ]
    page_rows = (
        select(
            *(filtered.c[name] for name in fields),
            filtered.c.subject_order,
            filtered.c.topic_order,
            filtered.c.lesson_order,
        )
        .order_by(
            filtered.c.subject_order,
            filtered.c.topic_order,
            filtered.c.lesson_order,
            filtered.c.id,
        )
        .offset((page - 1) * 12)
        .limit(12)
        .subquery("library_page")
    )
    result = (
        conn.execute(
            select(*counts.c, *page_rows.c)
            .select_from(counts.outerjoin(page_rows, true()))
            .order_by(
                page_rows.c.subject_order,
                page_rows.c.topic_order,
                page_rows.c.lesson_order,
                page_rows.c.id,
            )
        )
        .mappings()
        .all()
    )
    totals = {
        name: result[0][name]
        for name in ["total", "completed", "in_progress", "free", "vip", "bookmarked"]
    }
    rows = [{name: row[name] for name in fields} for row in result if row["id"] is not None]
    membership = access.resolve_membership(conn, user["id"])
    items = [
        {**dict(row), **access.content_access(conn, user, "lesson", row["id"], grade, membership)}
        for row in rows
    ]
    return {"grade": grade, "page": page, "page_size": 12, "summary": dict(totals), "items": items}
