from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select

from app.core.security import admin_user, student_user
from app.curriculum_map import SOURCES, TOPIC_MAP
from app.db import connection, db
from app.services import access
from app.services.vip import profile

router = APIRouter(prefix="/api/v1", tags=["curriculum-extension"])


@router.get("/admin/curriculum-map", response_model=dict)
def curriculum_map(
    grade: int = Query(4, ge=3, le=4), user=Depends(admin_user), conn=Depends(connection)
):
    from app.grade3_curriculum import FOCUS, TOPICS

    topic_map = (
        TOPIC_MAP
        if grade == 4
        else {
            subject: {key: (title, FOCUS[subject][key]) for key, title in source.items()}
            for subject, source in TOPICS.items()
        }
    )
    topics, subjects, lessons, policies = (
        db.table(name) for name in ("topics", "subjects", "lessons", "content_access_policies")
    )
    topic_rows = {
        (row["subject_id"], row["code"]): dict(row)
        for row in conn.execute(select(topics).where(topics.c.grade == grade)).mappings()
    }
    counts = {}
    for row in conn.execute(
        select(lessons.c.topic_id, policies.c.minimum_plan_code, func.count().label("total"))
        .select_from(lessons.join(topics).outerjoin(policies, policies.c.lesson_id == lessons.c.id))
        .where(topics.c.grade == grade, lessons.c.status == "published")
        .group_by(lessons.c.topic_id, policies.c.minimum_plan_code)
    ).mappings():
        counts.setdefault(row["topic_id"], {})[row["minimum_plan_code"]] = row["total"]
    resources = {}
    for name in ("assessments", "questions"):
        table = db.table(name)
        query = select(table.c.topic_id, func.count().label("total")).where(table.c.grade == grade)
        if name == "questions":
            versions = db.table("question_versions")
            # Count distinct questions, not every published revision of the same question.
            query = select(table.c.topic_id, func.count(func.distinct(table.c.id)).label("total"))
            query = query.join(versions).where(
                table.c.grade == grade,
                table.c.is_active.is_(True),
                versions.c.status == "published",
            )
        else:
            query = query.where(table.c.status == "published")
        resources[name] = {
            r.topic_id: r.total for r in conn.execute(query.group_by(table.c.topic_id))
        }
    subject_rows = {r["code"]: dict(r) for r in conn.execute(select(subjects)).mappings()}
    rows = []
    for subject_code, source in topic_map.items():
        for key, (title, focus) in source.items():
            subject = subject_rows.get(subject_code)
            topic = (
                topic_rows.get((subject["id"], f"VT{grade}-{subject_code}-{key}"))
                if subject
                else None
            )
            topic_id = topic["id"] if topic else None
            numbers = counts.get(topic_id, {})
            rows.append(
                dict(
                    code=f"VT{grade}-{subject_code}-{key}",
                    subject_code=subject_code,
                    subject_name=subject["name_vi"] if subject else subject_code,
                    title=title,
                    focus=focus,
                    topic_id=topic_id,
                    active=bool(subject and subject["is_active"] and topic and topic["is_active"]),
                    free_lessons=numbers.get("free", 0),
                    vip_lessons=numbers.get("vip", 0),
                    unconfigured_lessons=numbers.get(None, 0),
                    questions=resources["questions"].get(topic_id, 0),
                    assessments=resources["assessments"].get(topic_id, 0),
                    source_url=SOURCES[subject_code],
                )
            )
    return {"grade": grade, "rows": rows}


@router.get("/students/me/thinking", response_model=dict)
def thinking(
    subject_code: Literal["MATH", "VIETNAMESE", "ENGLISH"] | None = None,
    page: int = Query(1, ge=1, le=10000),
    user=Depends(student_user),
    conn=Depends(connection),
):
    grade = profile(conn, user["id"])
    lessons, topics, subjects, progress = (
        db.table(name) for name in ("lessons", "topics", "subjects", "student_lesson_progress")
    )
    scope = lessons.join(topics).join(subjects, subjects.c.id == topics.c.subject_id)
    predicates = [
        topics.c.grade == grade,
        topics.c.is_active.is_(True),
        subjects.c.is_active.is_(True),
        lessons.c.status == "published",
        lessons.c.content["category"].astext == "thinking",
    ]
    if subject_code:
        predicates.append(subjects.c.code == subject_code)
    total = conn.execute(select(func.count()).select_from(scope).where(*predicates)).scalar_one()
    query = (
        select(
            lessons.c.id,
            lessons.c.title,
            lessons.c.estimated_minutes,
            subjects.c.code.label("subject_code"),
            subjects.c.name_vi.label("subject_name"),
            progress.c.status.label("progress_status"),
        )
        .select_from(
            scope.outerjoin(
                progress,
                (progress.c.lesson_id == lessons.c.id) & (progress.c.student_id == user["id"]),
            )
        )
        .where(*predicates)
        .order_by(subjects.c.code, topics.c.sort_order, lessons.c.sort_order, lessons.c.id)
        .offset((page - 1) * 20)
        .limit(20)
    )
    membership = access.resolve_membership(conn, user["id"])
    # Only catalogue metadata. Paid text, hints, answers stay behind the lesson endpoint.
    items = [
        {**dict(row), **access.content_access(conn, user, "lesson", row["id"], grade, membership)}
        for row in conn.execute(query).mappings()
    ]
    return {"grade": grade, "items": items, "total": total, "page": page}
