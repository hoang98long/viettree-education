"""Short, rules-based learning plans using the existing curriculum and progress tables."""

from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import func, select

from app.core.security import now
from app.db import db
from app.services import access


def list_plans(conn, student_id, grade):
    suspend_unavailable_plans(conn, student_id)
    plans, subjects, items, lessons, assessments = (
        db.table(name)
        for name in (
            "student_learning_plans",
            "subjects",
            "learning_plan_items",
            "lessons",
            "assessments",
        )
    )
    rows = (
        conn.execute(
            select(
                plans,
                subjects.c.code.label("subject_code"),
                subjects.c.name_vi.label("subject_name"),
            )
            .select_from(plans.join(subjects))
            .where(
                plans.c.student_id == student_id,
                plans.c.plan_metadata["grade"].as_integer() == grade,
                plans.c.status.in_(["active", "completed", "paused"]),
            )
            .order_by((plans.c.status == "active").desc(), plans.c.created_at.desc())
            .limit(12)
        )
        .mappings()
        .all()
    )
    result = []
    for row in rows:
        steps = [
            dict(step)
            for step in conn.execute(
                select(
                    items.c.id,
                    items.c.position,
                    items.c.lesson_id,
                    items.c.assessment_id,
                    items.c.status,
                    items.c.due_at,
                    items.c.completed_at,
                    func.coalesce(lessons.c.title, assessments.c.title).label("title"),
                )
                .select_from(
                    items.outerjoin(lessons, items.c.lesson_id == lessons.c.id).outerjoin(
                        assessments, items.c.assessment_id == assessments.c.id
                    )
                )
                .where(items.c.learning_plan_id == row["id"])
                .order_by(items.c.position)
            ).mappings()
        ]
        for step in steps:
            step.update(
                access.content_access(
                    conn,
                    access.student_actor(student_id),
                    "lesson" if step["lesson_id"] else "assessment",
                    step["lesson_id"] or step["assessment_id"],
                    grade,
                )
            )
        result.append(
            {
                **dict(row),
                "items": steps,
                "completed_count": sum(step["status"] == "completed" for step in steps),
                "mode": row["plan_metadata"].get("mode", "basic"),
                "explanation": row["plan_metadata"].get(
                    "explanation", "Theo thứ tự chương trình, từng bước nhỏ."
                ),
            }
        )
    return result


def create_plan(conn, student_id, grade, subject_code, mode="basic"):
    # Caller holds the student-profile lock, serializing duplicate creations and submissions.
    if mode == "adaptive":
        access.require_feature(conn, student_id, "learning_plan.adaptive")
    else:
        access.require_feature(conn, student_id, "learning_plan.basic")
    suspend_unavailable_plans(conn, student_id)
    subjects, plans = db.table("subjects"), db.table("student_learning_plans")
    subject = (
        conn.execute(
            select(subjects).where(subjects.c.code == subject_code, subjects.c.is_active.is_(True))
        )
        .mappings()
        .first()
    )
    if not subject:
        raise HTTPException(404, "Không tìm thấy môn học")
    active = (
        conn.execute(
            select(plans).where(
                plans.c.student_id == student_id,
                plans.c.subject_id == subject["id"],
                plans.c.status == "active",
            )
        )
        .mappings()
        .first()
    )
    if (
        active
        and active["plan_metadata"].get("grade") == grade
        and active["plan_metadata"].get("mode", "basic") == mode
    ):
        return next(
            plan for plan in list_plans(conn, student_id, grade) if plan["id"] == active["id"]
        )

    lessons, topics, progress = (
        db.table(name) for name in ("lessons", "topics", "student_lesson_progress")
    )
    completed = select(progress.c.lesson_id).where(
        progress.c.student_id == student_id, progress.c.status == "completed"
    )
    candidates = (
        conn.execute(
            select(lessons.c.id, lessons.c.topic_id, lessons.c.title)
            .select_from(lessons.join(topics))
            .where(
                topics.c.subject_id == subject["id"],
                topics.c.grade == grade,
                topics.c.is_active.is_(True),
                lessons.c.status == "published",
                lessons.c.id.not_in(completed),
            )
            .order_by(topics.c.sort_order, lessons.c.sort_order, lessons.c.code)
        )
        .mappings()
        .all()
    )
    candidates = [
        row
        for row in candidates
        if access.eligible(conn, student_id, "lesson", row["id"], grade)
        and (
            mode == "adaptive"
            or access.policy(conn, "lesson", row["id"])["minimum_plan_code"] == "free"
        )
    ]
    explanation = "Theo thứ tự chương trình, từng bước nhỏ."
    if mode == "adaptive":
        mastery, links, prereqs = (
            db.table(name)
            for name in ("student_skill_mastery", "lesson_skills", "skill_prerequisites")
        )
        states = {
            row["skill_id"]: row
            for row in conn.execute(
                select(mastery).where(mastery.c.student_id == student_id)
            ).mappings()
        }
        lesson_skills = {}
        for row in conn.execute(select(links)).mappings():
            lesson_skills.setdefault(row["lesson_id"], []).append(row["skill_id"])
        urgent = set()
        for row in conn.execute(select(prereqs)).mappings():
            state = states.get(row["skill_id"])
            prior = states.get(row["prerequisite_skill_id"])
            if (
                state
                and state["questions_attempted"] >= 5
                and float(state["mastery_score"]) < 0.5
                and (not prior or float(prior["mastery_score"]) < 0.5)
            ):
                urgent.add(row["prerequisite_skill_id"])

        def rank(row):
            evidence = [
                states[skill]
                for skill in lesson_skills.get(row["id"], [])
                if skill in states and states[skill]["questions_attempted"] >= 5
            ]
            weak = min((float(state["mastery_score"]) for state in evidence), default=1)
            due = any(
                state["next_review_at"] and state["next_review_at"] <= now() for state in evidence
            )
            advanced = access.policy(conn, "lesson", row["id"])["learning_level"] == "advanced"
            linked_skills = lesson_skills.get(row["id"], [])
            confident = bool(linked_skills) and all(
                skill in states
                and states[skill]["questions_attempted"] >= 5
                and float(states[skill]["mastery_score"]) >= 0.8
                and float(states[skill]["confidence"]) >= 0.25
                for skill in linked_skills
            )
            return (
                not bool(set(lesson_skills.get(row["id"], [])) & urgent),
                advanced and not confident,
                not (weak < 0.5 or due),
                weak,
            )

        candidates = [row for row in candidates if not rank(row)[1]]
        candidates.sort(key=rank)
        explanation = "Ưu tiên kỹ năng nền tảng, kỹ năng cần ôn và bài nâng cao khi em đã vững. Chưa đủ dữ liệu thì bắt đầu từ bài nền tảng."
    candidates = candidates[:3]
    if not candidates:
        raise HTTPException(
            409, "Chưa có bài học mới để lập kế hoạch. Em có thể ôn lại bài đã học."
        )
    if active:
        conn.execute(plans.update().where(plans.c.id == active["id"]).values(status="archived"))
        record_change(
            conn, active["id"], student_id, "archived", {"reason": "grade_or_mode_changed"}
        )

    at = now()
    timezone = ZoneInfo("Asia/Bangkok")
    today = at.astimezone(timezone).date()
    plan_id = uuid4()
    conn.execute(
        plans.insert().values(
            id=plan_id,
            student_id=student_id,
            subject_id=subject["id"],
            title=f"7 ngày cùng {subject['name_vi']}",
            status="active",
            start_date=today,
            end_date=today + timedelta(days=6),
            generated_by="rules",
            model_version="plan_v2" if mode == "adaptive" else "plan_v1",
            plan_metadata={"grade": grade, "mode": mode, "explanation": explanation},
        )
    )
    assessments, attempts, assessment_items = (
        db.table(name) for name in ("assessments", "attempts", "assessment_items")
    )
    attempt_count = (
        select(func.count())
        .where(attempts.c.student_id == student_id, attempts.c.assessment_id == assessments.c.id)
        .scalar_subquery()
    )
    steps = []
    for index, candidate in enumerate(candidates):
        due = datetime.combine(today + timedelta(days=index * 2), datetime.max.time(), timezone)
        steps.append({"lesson_id": candidate["id"], "due_at": due})
        # Practice follows the final selected lesson in a topic, and respects the attempt cap.
        if any(other["topic_id"] == candidate["topic_id"] for other in candidates[index + 1 :]):
            continue
        possible_assessments = (
            conn.execute(
                select(assessments.c.id)
                .where(
                    assessments.c.topic_id == candidate["topic_id"],
                    assessments.c.subject_id == subject["id"],
                    assessments.c.grade == grade,
                    assessments.c.status == "published",
                    attempt_count < assessments.c.max_attempts,
                    select(assessment_items.c.id)
                    .where(assessment_items.c.assessment_id == assessments.c.id)
                    .exists(),
                )
                .order_by(
                    (assessments.c.lesson_id == candidate["id"]).desc().nullslast(),
                    assessments.c.code,
                )
            )
            .scalars()
            .all()
        )
        assessment = next(
            (
                candidate_id
                for candidate_id in possible_assessments
                if access.eligible(conn, student_id, "assessment", candidate_id, grade)
                and (
                    mode == "adaptive"
                    or access.policy(conn, "assessment", candidate_id)["minimum_plan_code"]
                    == "free"
                )
            ),
            None,
        )
        if assessment:
            steps.append({"assessment_id": assessment, "due_at": due})
    items = db.table("learning_plan_items")
    conn.execute(
        items.insert(),
        [
            {
                "learning_plan_id": plan_id,
                "position": position,
                "lesson_id": step.get("lesson_id"),
                "assessment_id": step.get("assessment_id"),
                "due_at": step["due_at"],
            }
            for position, step in enumerate(steps, 1)
        ],
    )
    record_change(conn, plan_id, student_id, "created", {"item_count": len(steps), "grade": grade})
    return next(plan for plan in list_plans(conn, student_id, grade) if plan["id"] == plan_id)


def suspend_unavailable_plans(conn, student_id):
    if "learning_plan.adaptive" in access.resolve_membership(conn, student_id)["features"]:
        return
    profiles, plans = db.table("student_profiles"), db.table("student_learning_plans")
    conn.execute(
        select(profiles.c.student_id).where(profiles.c.student_id == student_id).with_for_update()
    )
    changed = (
        conn.execute(
            plans.update()
            .where(
                plans.c.student_id == student_id,
                plans.c.status == "active",
                plans.c.plan_metadata["mode"].as_string() == "adaptive",
            )
            .values(status="paused", updated_at=now())
            .returning(plans.c.id)
        )
        .scalars()
        .all()
    )
    for plan_id in changed:
        record_change(conn, plan_id, student_id, "paused", {"reason": "membership_unavailable"})


def record_change(conn, plan_id, student_id, change_type, snapshot):
    conn.execute(
        db.table("learning_plan_history")
        .insert()
        .values(
            learning_plan_id=plan_id,
            changed_by=student_id,
            change_type=change_type,
            snapshot=snapshot,
        )
    )


def update_targets(conn, student_id, *, lesson_id=None, assessment_id=None, completed=True):
    plans, items = db.table("student_learning_plans"), db.table("learning_plan_items")
    target = items.c.lesson_id == lesson_id if lesson_id else items.c.assessment_id == assessment_id
    active = select(plans.c.id).where(plans.c.student_id == student_id, plans.c.status == "active")
    at = now()
    changed = conn.execute(
        items.update()
        .where(
            items.c.learning_plan_id.in_(active),
            target,
            items.c.status.in_(["pending", "in_progress"] if completed else ["pending"]),
        )
        .values(
            status="completed" if completed else "in_progress",
            updated_at=at,
            completed_at=at if completed else None,
        )
        .returning(items.c.learning_plan_id, items.c.id)
    ).all()
    for plan_id in {row.learning_plan_id for row in changed}:
        conn.execute(plans.update().where(plans.c.id == plan_id).values(updated_at=at))
        record_change(
            conn,
            plan_id,
            student_id,
            "progress",
            {
                "item_ids": [str(row.id) for row in changed if row.learning_plan_id == plan_id],
                "status": "completed" if completed else "in_progress",
            },
        )
        unfinished = conn.execute(
            select(func.count())
            .select_from(items)
            .where(items.c.learning_plan_id == plan_id, items.c.status != "completed")
        ).scalar_one()
        if unfinished == 0:
            conn.execute(
                plans.update()
                .where(plans.c.id == plan_id)
                .values(status="completed", updated_at=at)
            )
            record_change(conn, plan_id, student_id, "completed", {})
