"""Bounded, student-scoped practice discovery; never serializes answer keys."""

from sqlalchemy import case, func, or_, select, true
from sqlalchemy.dialects.postgresql import distinct_on

from app.db import db
from app.services import access
from app.services.lesson_library import ACCENTS, BASE_LETTERS, fold
from app.services.vip import profile


def practice_library(
    conn,
    user,
    subject_code=None,
    plan="all",
    progress="all",
    max_questions=None,
    search="",
    page=1,
    kind="all",
):
    grade = profile(conn, user["id"])
    assessments, subjects, topics, items, attempts, policies = (
        db.table(name)
        for name in (
            "assessments",
            "subjects",
            "topics",
            "assessment_items",
            "attempts",
            "content_access_policies",
        )
    )
    # Only this student's finalized attempts count. A submitted but ungraded
    # attempt must not turn its initial zero score into a recommendation to review.
    scores = (
        select(
            attempts.c.assessment_id,
            attempts.c.id.label("attempt_id"),
            attempts.c.graded_at,
            attempts.c.submitted_at,
            (100 * attempts.c.total_score / func.nullif(attempts.c.max_score, 0)).label("percent"),
        )
        .where(
            attempts.c.student_id == user["id"],
            attempts.c.status == "graded",
            attempts.c.max_score > 0,
        )
        .cte("my_scores")
    )
    best = (
        select(
            scores.c.assessment_id,
            func.max(scores.c.percent).label("best_percent"),
            func.count().label("graded_count"),
        )
        .group_by(scores.c.assessment_id)
        .subquery("my_best")
    )
    latest = (
        select(scores.c.assessment_id, scores.c.percent.label("latest_percent"))
        .ext(distinct_on(scores.c.assessment_id))
        .order_by(
            scores.c.assessment_id,
            scores.c.submitted_at.desc().nulls_last(),
            scores.c.graded_at.desc().nulls_last(),
            scores.c.attempt_id.desc(),
        )
        .subquery("my_latest")
    )
    counts = (
        select(items.c.assessment_id, func.count().label("item_count"))
        .select_from(items.join(assessments))
        .where(assessments.c.grade == grade, assessments.c.status == "published")
        .group_by(items.c.assessment_id)
        .subquery("item_counts")
    )
    progress_value = case(
        (latest.c.latest_percent.is_(None), "not_started"),
        (latest.c.latest_percent < 80, "review"),
        else_="mastered",
    )
    scope = (
        assessments.join(subjects)
        .outerjoin(topics, topics.c.id == assessments.c.topic_id)
        .join(counts, counts.c.assessment_id == assessments.c.id)
        .outerjoin(best, best.c.assessment_id == assessments.c.id)
        .outerjoin(latest, latest.c.assessment_id == assessments.c.id)
        .outerjoin(policies, policies.c.assessment_id == assessments.c.id)
    )
    predicates = [
        assessments.c.grade == grade,
        assessments.c.status == "published",
        subjects.c.is_active.is_(True),
        or_(assessments.c.topic_id.is_(None), topics.c.is_active.is_(True)),
    ]
    if subject_code:
        predicates.append(subjects.c.code == subject_code)
    if plan != "all":
        predicates.append(policies.c.minimum_plan_code == plan)
    if progress != "all":
        predicates.append(progress_value == progress)
    if kind != "all":
        predicates.append(assessments.c.assessment_type == kind)
    if max_questions:
        predicates.append(counts.c.item_count <= max_questions)
    search = fold(search.strip())
    if search:
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        predicates.append(
            or_(
                *[
                    func.translate(func.lower(column), ACCENTS, BASE_LETTERS).like(
                        "%" + escaped + "%", escape="\\"
                    )
                    for column in (assessments.c.title, topics.c.title)
                ]
            )
        )
    fields = [
        assessments.c.id,
        assessments.c.title,
        assessments.c.lesson_id,
        assessments.c.time_limit_seconds,
        assessments.c.assessment_type,
        subjects.c.code.label("subject_code"),
        subjects.c.name_vi.label("subject_name"),
        topics.c.title.label("topic_title"),
        counts.c.item_count,
        func.coalesce(best.c.graded_count, 0).label("graded_count"),
        best.c.best_percent,
        latest.c.latest_percent,
        progress_value.label("progress_status"),
    ]
    filtered = (
        select(
            *fields,
            subjects.c.sort_order.label("subject_order"),
            assessments.c.code.label("sort_code"),
        )
        .select_from(scope)
        .where(*predicates)
        .cte("practice_filtered")
    )
    totals = (
        select(
            func.count().label("total"),
            func.count().filter(filtered.c.progress_status == "review").label("review"),
            func.count().filter(filtered.c.progress_status == "mastered").label("mastered"),
            func.count().filter(filtered.c.progress_status == "not_started").label("not_started"),
        )
        .select_from(filtered)
        .subquery("practice_totals")
    )
    page_rows = (
        select(filtered)
        .order_by(filtered.c.subject_order, filtered.c.sort_code, filtered.c.id)
        .offset((page - 1) * 12)
        .limit(12)
        .subquery("practice_page")
    )
    rows = (
        conn.execute(
            select(*totals.c, *page_rows.c)
            .select_from(totals.outerjoin(page_rows, true()))
            .order_by(page_rows.c.subject_order, page_rows.c.sort_code, page_rows.c.id)
        )
        .mappings()
        .all()
    )
    membership = access.resolve_membership(conn, user["id"])
    result = []
    names = [field.name for field in fields]
    for row in rows:
        if row["id"] is not None:
            result.append(
                {
                    **{name: row[name] for name in names},
                    **access.content_access(conn, user, "assessment", row["id"], grade, membership),
                }
            )
    return {
        "grade": grade,
        "page": page,
        "page_size": 12,
        "summary": {name: rows[0][name] for name in ("total", "review", "mastered", "not_started")},
        "items": result,
    }
