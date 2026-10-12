from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import select, text

from app.classroom.service import audit, class_scope
from app.core.security import now
from app.db import db


def period_bounds(period):
    local = now().astimezone(ZoneInfo("Asia/Bangkok"))
    start = local.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "week":
        start -= timedelta(days=start.weekday())
        end = start + timedelta(days=7)
    else:
        start = start.replace(day=1)
        end = datetime(
            start.year + (start.month == 12),
            1 if start.month == 12 else start.month + 1,
            1,
            tzinfo=start.tzinfo,
        )
    return start, end


def score_records(conn, identifiers, grade, category, start, end, resource_id=None, class_id=None):
    params = {
        "students": identifiers,
        "grade": grade,
        "category": category,
        "start": start,
        "end": min(end, now()),
        "resource": resource_id,
        "class_id": class_id,
    }
    if category == "AI":
        query = """SELECT a.student_id,l.id AS resource_id,a.score*100 AS score,a.created_at AS at,a.id
          FROM ai_attempts a JOIN ai_lesson_versions v ON v.id=a.version_id
          JOIN ai_lessons l ON l.id=v.lesson_id JOIN ai_units u ON u.id=l.unit_id
          WHERE a.student_id=ANY(:students) AND u.grade=:grade AND a.created_at>=:start AND a.created_at<:end
          AND (CAST(:resource AS UUID) IS NULL OR l.id=CAST(:resource AS UUID))
          AND EXISTS(SELECT 1 FROM jsonb_array_elements(v.payload->'steps') s WHERE s->>'id'=a.step_id AND s->>'kind'='quiz')"""
    elif category == "AI_PROJECT":
        query = """SELECT s.student_id,p.id AS resource_id,r.total AS score,r.updated_at AS at,s.id
          FROM ai_rubric_scores r JOIN ai_project_submissions s ON s.id=r.submission_id
          JOIN ai_projects p ON p.id=s.project_id
          WHERE s.student_id=ANY(:students) AND p.grade=:grade AND s.status='reviewed'
          AND (CAST(:class_id AS UUID) IS NULL OR s.class_id=CAST(:class_id AS UUID))
          AND r.updated_at>=:start AND r.updated_at<:end AND (CAST(:resource AS UUID) IS NULL OR p.id=CAST(:resource AS UUID))"""
    else:
        query = """SELECT a.student_id,t.id AS resource_id,a.total_score*100/a.max_score AS score,a.graded_at AS at,a.id
          FROM attempts a JOIN assessments t ON t.id=a.assessment_id JOIN subjects s ON s.id=t.subject_id
          WHERE a.student_id=ANY(:students) AND t.grade=:grade AND s.code=:category AND a.status='graded' AND a.max_score>0
          AND a.graded_at>=:start AND a.graded_at<:end AND (CAST(:resource AS UUID) IS NULL OR t.id=CAST(:resource AS UUID))"""
    return conn.execute(text(query), params).mappings().all()


def aggregate(records):
    # Keep the best graded result per resource; retries never add extra ranking points.
    best = {}
    for row in records:
        key = row["student_id"], row["resource_id"]
        old = best.get(key)
        if (
            old is None
            or row["score"] > old["score"]
            or (row["score"] == old["score"] and row["at"] < old["at"])
        ):
            best[key] = row
    groups = {}
    for row in best.values():
        groups.setdefault(row["student_id"], []).append(row)
    output = [
        {
            "student_id": identifier,
            "score": sum(Decimal(str(r["score"])) for r in rows) / len(rows),
            "completed": len(rows),
            "achieved_at": max(r["at"] for r in rows),
        }
        for identifier, rows in groups.items()
    ]
    return sorted(
        output, key=lambda r: (-r["score"], -r["completed"], r["achieved_at"], str(r["student_id"]))
    )


def leaderboard(conn, user, class_id, category, period, resource_id=None):
    classroom = class_scope(conn, user, class_id)
    settings = db.table("classroom_settings")
    enabled = conn.execute(
        select(settings.c.recognition_enabled).where(settings.c.class_id == class_id)
    ).scalar()
    if not classroom["is_active"]:
        raise HTTPException(409, "Lớp đã đóng")
    if enabled is False:
        return {
            "enabled": False,
            "rows": [],
            "top_three": [],
            "category": category,
            "period": period,
        }
    enrollments, users = db.table("class_enrollments"), db.table("users")
    learners = list(
        conn.execute(
            select(users.c.id, users.c.display_name, enrollments.c.recognition_alias)
            .join(enrollments, enrollments.c.student_id == users.c.id)
            .where(
                enrollments.c.class_id == class_id,
                enrollments.c.left_at.is_(None),
                users.c.is_active.is_(True),
            )
        ).mappings()
    )
    start, end = period_bounds(period)
    ranked = (
        aggregate(
            score_records(
                conn,
                [r["id"] for r in learners],
                classroom["grade"],
                category,
                start,
                end,
                resource_id,
                class_id,
            )
        )
        if learners
        else []
    )
    names = {r["id"]: r for r in learners}
    staff = bool({"teacher", "admin"} & set(user["roles"]))
    rows = []
    for index, record in enumerate(ranked, 1):
        learner = names[record["student_id"]]
        alias = learner["recognition_alias"] or "Bạn " + record["student_id"].hex[:6]
        item = {
            "rank": index,
            "alias": alias,
            "display_name": learner["display_name"] if staff else alias,
            "score": round(record["score"], 3),
            "completed": record["completed"],
            "is_me": record["student_id"] == user["id"],
        }
        if staff:
            item["student_id"] = record["student_id"]
        rows.append(item)
    return {
        "enabled": True,
        "rows": rows,
        "top_three": rows[:3],
        "category": category,
        "period": period,
        "period_start": start,
        "period_end": end,
        "eligible_count": len(learners),
        "resource_id": resource_id,
        "formula": "Điểm trung bình các kết quả tốt nhất của từng bài đã chấm; đồng điểm xét số bài, rồi thời điểm đạt. VIP không cộng điểm thưởng.",
    }


def publish(conn, user, class_id, payload):
    class_scope(conn, user, class_id, staff_only=True, lock=True)
    # Stable period + scope key makes repeat publication idempotent.
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
        {
            "key": f"class-awards:{class_id}:{payload.category}:{payload.period}:{payload.resource_id}"
        },
    )
    ranked = leaderboard(
        conn, user, class_id, payload.category, payload.period, payload.resource_id
    )
    if not ranked["enabled"] or not ranked["rows"]:
        raise HTTPException(409, "Chưa bật tuyên dương hoặc chưa có bài đã chấm trong kỳ")
    batches, awards = db.table("class_award_batches"), db.table("class_awards")
    key = str(payload.resource_id) if payload.resource_id else "all"
    old = conn.execute(
        select(batches.c.id).where(
            batches.c.class_id == class_id,
            batches.c.category == payload.category,
            batches.c.period_start == ranked["period_start"],
            batches.c.period_end == ranked["period_end"],
            batches.c.resource_key == key,
        )
    ).scalar()
    if old:
        return {"id": old, "replayed": True}
    identifier = uuid4()
    conn.execute(
        batches.insert().values(
            id=identifier,
            class_id=class_id,
            category=payload.category,
            period_start=ranked["period_start"],
            period_end=ranked["period_end"],
            resource_key=key,
            published_by=user["id"],
        )
    )
    for row in ranked["top_three"]:
        conn.execute(
            awards.insert().values(
                batch_id=identifier,
                rank=row["rank"],
                student_id=row["student_id"],
                alias=row["alias"],
                score=row["score"],
                completed=row["completed"],
            )
        )
    audit(
        conn,
        user,
        "classroom.top_three_published",
        class_id,
        {"category": payload.category, "count": len(ranked["top_three"])},
    )
    return {"id": identifier, "replayed": False}
