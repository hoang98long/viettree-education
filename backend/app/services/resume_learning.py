"""Recent unfinished work, scoped to the learner and rechecked against live access."""

from fastapi import HTTPException
from sqlalchemy import false, func, literal_column, or_, select

from app.core.security import now
from app.db import db
from app.services import access


def recent_work(conn, user, grade):
    membership = access.resolve_membership(conn, user["id"])
    at = now()
    result = []
    progress, lessons, topics, subjects, policies = (
        db.table(n)
        for n in (
            "student_lesson_progress",
            "lessons",
            "topics",
            "subjects",
            "content_access_policies",
        )
    )
    plans = [
        plan
        for plan, feature in (("free", "learning.basic"), ("vip", "learning.advanced"))
        if feature in membership["features"]
    ]
    reading = (
        conn.execute(
            select(
                lessons.c.id,
                lessons.c.title,
                subjects.c.name_vi.label("subject_name"),
                func.coalesce(progress.c.last_accessed_at, progress.c.updated_at).label(
                    "last_activity_at"
                ),
            )
            .select_from(
                progress.join(lessons, lessons.c.id == progress.c.lesson_id)
                .join(topics, topics.c.id == lessons.c.topic_id)
                .join(subjects, subjects.c.id == topics.c.subject_id)
                .join(policies, policies.c.lesson_id == lessons.c.id)
            )
            .where(
                progress.c.student_id == user["id"],
                progress.c.status == "in_progress",
                lessons.c.status == "published",
                topics.c.grade == grade,
                topics.c.is_active.is_(True),
                subjects.c.is_active.is_(True),
                policies.c.minimum_plan_code.in_(plans),
            )
            .order_by(
                func.coalesce(progress.c.last_accessed_at, progress.c.updated_at).desc(),
                lessons.c.id,
            )
            .limit(1)
        )
        .mappings()
        .first()
    )
    if reading:
        result.append(dict(reading, kind="lesson", grade=grade))

    attempts, assessments, assignments, grants = (
        db.table(n)
        for n in ("attempts", "assessments", "student_assignments", "attempt_access_grants")
    )
    practice_plans = [
        plan
        for plan, feature in (("free", "practice.basic"), ("vip", "practice.advanced"))
        if feature in membership["features"]
    ]
    # Time and assignment state are filtered before LIMIT. Do not recommend an expired exam.
    recent_attempts = conn.execute(
        select(
            attempts,
            assessments.c.title,
            subjects.c.name_vi.label("subject_name"),
            func.coalesce(attempts.c.updated_at, attempts.c.started_at).label("last_activity_at"),
        )
        .select_from(
            attempts.join(assessments, assessments.c.id == attempts.c.assessment_id)
            .join(subjects, subjects.c.id == assessments.c.subject_id)
            .join(assignments, assignments.c.id == attempts.c.assignment_id)
            .outerjoin(topics, topics.c.id == assessments.c.topic_id)
            .outerjoin(grants, grants.c.attempt_id == attempts.c.id)
            .join(policies, policies.c.assessment_id == assessments.c.id)
        )
        .where(
            attempts.c.student_id == user["id"],
            assignments.c.student_id == user["id"],
            attempts.c.status == "in_progress",
            assessments.c.status == "published",
            assessments.c.grade == grade,
            subjects.c.is_active.is_(True),
            or_(assessments.c.topic_id.is_(None), topics.c.is_active.is_(True)),
            assignments.c.status.in_(["assigned", "in_progress"]),
            assignments.c.available_at <= at,
            or_(assignments.c.due_at.is_(None), assignments.c.due_at > at),
            or_(
                assessments.c.time_limit_seconds.is_(None),
                attempts.c.started_at
                + assessments.c.time_limit_seconds * literal_column("INTERVAL '1 second'")
                > at,
            ),
            grants.c.revoked_at.is_(None),
            or_(
                policies.c.minimum_plan_code.in_(practice_plans),
                grants.c.allowed_until > at if membership["status"] == "expired" else false(),
            ),
        )
        .order_by(func.coalesce(attempts.c.updated_at, attempts.c.started_at).desc(), attempts.c.id)
        .limit(5)
    ).mappings()
    for row in recent_attempts:
        try:
            access.authorize_attempt(conn, row)
        except HTTPException as error:
            if error.status_code != 403:
                raise
            continue
        result.append(
            {key: row[key] for key in ("id", "title", "subject_name", "last_activity_at")}
            | {"kind": "practice", "grade": grade}
        )
        break

    ai_progress, ai_lessons, ai_units, versions = (
        db.table(n) for n in ("ai_progress", "ai_lessons", "ai_units", "ai_lesson_versions")
    )
    published = versions.alias("currently_published")
    ai = (
        conn.execute(
            select(
                ai_lessons.c.id,
                ai_lessons.c.title,
                ai_units.c.grade,
                ai_progress.c.updated_at.label("last_activity_at"),
                ai_progress.c.next_step,
                func.jsonb_array_length(versions.c.payload["steps"]).label("step_count"),
            )
            .select_from(
                ai_progress.join(ai_lessons, ai_lessons.c.id == ai_progress.c.lesson_id)
                .join(ai_units, ai_units.c.id == ai_lessons.c.unit_id)
                .join(versions, versions.c.id == ai_progress.c.version_id)
            )
            .where(
                ai_progress.c.student_id == user["id"],
                ai_progress.c.completed_at.is_(None),
                ai_units.c.grade <= grade,
                ai_lessons.c.minimum_plan_code.in_(
                    ["free", "vip"] if "academy.full" in membership["features"] else ["free"]
                ),
                select(published.c.id)
                .where(published.c.lesson_id == ai_lessons.c.id, published.c.status == "published")
                .exists(),
            )
            .order_by(ai_progress.c.updated_at.desc(), ai_lessons.c.id)
            .limit(1)
        )
        .mappings()
        .first()
    )
    if ai:
        result.append(dict(ai, kind="ai", subject_name="Khám phá AI"))
    return sorted(
        result, key=lambda row: (row["last_activity_at"], row["kind"], str(row["id"])), reverse=True
    )
