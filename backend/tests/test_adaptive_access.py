from uuid import UUID

import pytest
from sqlalchemy import select

from app.core.security import now
from app.db import db
from tests.test_memberships import identities, membership

pytestmark = pytest.mark.integration


def test_advanced_plan_requires_evidence_for_every_linked_skill(logged_student, conn):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    lessons, topics, policies, links = (
        db.table(name) for name in ("lessons", "topics", "content_access_policies", "lesson_skills")
    )
    math_lessons = list(
        conn.execute(
            select(lessons.c.id, policies.c.minimum_plan_code)
            .join(topics, topics.c.id == lessons.c.topic_id)
            .join(policies, policies.c.lesson_id == lessons.c.id)
            .where(topics.c.code.like("VT4-MATH-%"))
        ).mappings()
    )
    progress = db.table("student_lesson_progress")
    for row in math_lessons:
        target_code = "VT4-MATH-vip-multi-step-lesson"
        target_id = conn.execute(
            select(lessons.c.id).where(lessons.c.code == target_code)
        ).scalar_one()
        if row["id"] != target_id:
            conn.execute(
                progress.insert().values(
                    student_id=student_id,
                    lesson_id=row["id"],
                    status="completed",
                    completion_ratio=1,
                    completed_at=now(),
                )
            )
    target = conn.execute(
        select(lessons.c.id).where(lessons.c.code == "VT4-MATH-vip-multi-step-lesson")
    ).scalar_one()
    known_skill = conn.execute(
        select(links.c.skill_id).where(links.c.lesson_id == target)
    ).scalar_one()
    unknown_skill = (
        conn.execute(select(links.c.skill_id).where(links.c.skill_id != known_skill))
        .scalars()
        .first()
    )
    conn.execute(
        db.table("student_skill_mastery")
        .insert()
        .values(
            student_id=student_id,
            skill_id=known_skill,
            mastery_score=1,
            confidence=0.5,
            questions_attempted=10,
            correct_count=10,
        )
    )
    conn.execute(links.insert().values(lesson_id=target, skill_id=unknown_skill, is_primary=False))
    payload = {"subject_code": "MATH", "mode": "adaptive"}
    assert client.post("/api/v1/students/me/learning-plans", json=payload).status_code == 409
    conn.execute(
        links.delete().where(links.c.lesson_id == target, links.c.skill_id == unknown_skill)
    )
    response = client.post("/api/v1/students/me/learning-plans", json=payload)
    assert response.status_code == 200, response.text
    plan = response.json()
    assert UUID(plan["items"][0]["lesson_id"]) == target
    assessment_id = next(item["assessment_id"] for item in plan["items"] if item["assessment_id"])
    assessments = db.table("assessments")
    assert (
        conn.execute(
            select(assessments.c.lesson_id).where(assessments.c.id == UUID(assessment_id))
        ).scalar_one()
        == target
    )
