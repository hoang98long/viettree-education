from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

import app.schemas.administration as schemas_administration
import app.schemas.catalog as schemas_catalog
from app.core.dependencies import database
from app.core.security import (
    admin_user,
    now,
)
from app.db import db
from app.schemas.administration import StudentUpdate
from app.schemas.common import Grade
from app.services import access
from app.services import attempts as service
from app.services.catalog import assessment_list

router = APIRouter(prefix="/api/v1")


@router.get(
    "/admin/statistics", response_model=schemas_administration.StatisticsResponse, tags=["admin"]
)
def statistics(user=Depends(admin_user), conn=database):
    attempts, answers = db.table("attempts"), db.table("attempt_answers")
    profiles, roles = db.table("student_profiles"), db.table("user_roles")
    stats = {
        "students": conn.execute(
            select(func.count())
            .select_from(profiles)
            .where(
                select(roles.c.user_id)
                .where(roles.c.user_id == profiles.c.student_id, roles.c.role == "student")
                .exists()
            )
        ).scalar_one()
    }
    for name in ("users", "lessons", "question_versions", "assessments"):
        table = db.table(name)
        statement = select(func.count()).select_from(table)
        if "status" in table.c:
            statement = statement.where(table.c.status == "published")
        stats[name] = conn.execute(statement).scalar_one()
    stats["attempts"] = conn.execute(
        select(func.count()).select_from(attempts).where(attempts.c.status == "graded")
    ).scalar_one()
    stats["average_percent"] = conn.execute(
        select(func.avg(attempts.c.total_score / func.nullif(attempts.c.max_score, 0) * 100)).where(
            attempts.c.status == "graded"
        )
    ).scalar()
    stats["correct_answers"] = conn.execute(
        select(func.count())
        .select_from(answers.join(attempts))
        .where(attempts.c.status == "graded", answers.c.is_correct.is_(True))
    ).scalar_one()
    return stats


@router.get(
    "/admin/students", response_model=schemas_administration.StudentPageResponse, tags=["admin"]
)
def students(search: str = "", page: int = Query(1, ge=1), user=Depends(admin_user), conn=database):
    users, profiles, roles = db.table("users"), db.table("student_profiles"), db.table("user_roles")
    statement = (
        select(
            users.c.id,
            users.c.username,
            users.c.display_name,
            users.c.is_active,
            profiles.c.current_grade,
        )
        .join(profiles, profiles.c.student_id == users.c.id)
        .where(
            select(roles.c.user_id)
            .where(roles.c.user_id == users.c.id, roles.c.role == "student")
            .exists()
        )
    )
    if search:
        statement = statement.where(
            users.c.display_name.ilike("%" + search.replace("%", "\\%").replace("_", "\\_") + "%")
            | users.c.username.ilike("%" + search.replace("%", "\\%").replace("_", "\\_") + "%")
        )
    total = conn.execute(select(func.count()).select_from(statement.subquery())).scalar_one()
    return dict(
        total=total,
        page=page,
        items=conn.execute(statement.order_by(users.c.username).offset((page - 1) * 20).limit(20))
        .mappings()
        .all(),
    )


@router.patch("/admin/students/{student_id}", response_model=dict[str, bool], tags=["admin"])
def update_student(
    student_id: UUID, payload: StudentUpdate, user=Depends(admin_user), conn=database
):
    users = db.table("users")
    conn.execute(
        select(users.c.id).where(users.c.id == student_id).with_for_update(key_share=True)
    ).first()
    service.lock_student(conn, student_id)
    if not payload.display_name.strip():
        raise HTTPException(422, "Tên hiển thị không được để trống")
    users, profiles = db.table("users"), db.table("student_profiles")
    conn.execute(
        users.update()
        .where(users.c.id == student_id)
        .values(
            display_name=payload.display_name.strip(),
            updated_at=now(),
            account_revision=users.c.account_revision + 1,
        )
    )
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == student_id)
        .values(current_grade=payload.current_grade, updated_at=now())
    )
    conn.execute(
        insert(db.table("audit_logs")).values(
            actor_user_id=user["id"],
            action="student_profile_updated",
            entity_type="student_profile",
            entity_id=student_id,
            new_values={"current_grade": payload.current_grade},
        )
    )
    return {"updated": True}


@router.get("/admin/users", response_model=list[dict], tags=["admin"])
def users(page: int = Query(1, ge=1), user=Depends(admin_user), conn=database):
    table = db.table("users")
    return (
        conn.execute(
            select(table.c.id, table.c.username, table.c.display_name, table.c.is_active)
            .order_by(table.c.username)
            .offset((page - 1) * 20)
            .limit(20)
        )
        .mappings()
        .all()
    )


@router.get(
    "/admin/questions", response_model=schemas_administration.QuestionPageResponse, tags=["admin"]
)
def questions(
    grade: Grade = 4,
    subject_code: str | None = None,
    search: str = "",
    status: Literal["draft", "published", "archived"] | None = None,
    question_type: Literal["single_choice", "multiple_choice", "fill_blank", "ordering"]
    | None = None,
    minimum_plan_code: Literal["free", "vip"] | None = None,
    topic_id: UUID | None = None,
    page: int = Query(1, ge=1),
    user=Depends(admin_user),
    conn=database,
):
    questions, versions, subjects = (
        db.table(name) for name in ("questions", "question_versions", "subjects")
    )
    policies = db.table("question_version_access_policies")
    statement = select(
        questions.c.code,
        questions.c.grade,
        versions.c.id,
        versions.c.question_id,
        versions.c.version,
        versions.c.reviewed_by,
        policies.c.minimum_plan_code,
        versions.c.question_type,
        versions.c.status,
        versions.c.difficulty,
        versions.c.content,
        subjects.c.name_vi.label("subject_name"),
    )
    statement = statement.select_from(
        questions.join(versions)
        .join(subjects)
        .outerjoin(policies, policies.c.question_version_id == versions.c.id)
    ).where(questions.c.grade == grade)
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    if search:
        statement = statement.where(
            questions.c.code.ilike("%" + search + "%")
            | versions.c.content["prompt"].as_string().ilike("%" + search + "%")
        )
    if status:
        statement = statement.where(versions.c.status == status)
    if question_type:
        statement = statement.where(versions.c.question_type == question_type)
    if minimum_plan_code:
        statement = statement.where(policies.c.minimum_plan_code == minimum_plan_code)
    if topic_id:
        statement = statement.where(questions.c.topic_id == topic_id)
    total = conn.execute(select(func.count()).select_from(statement.subquery())).scalar_one()
    return dict(
        total=total,
        page=page,
        items=conn.execute(statement.order_by(questions.c.code).offset((page - 1) * 20).limit(20))
        .mappings()
        .all(),
    )


@router.get("/admin/questions/{version_id}", response_model=dict, tags=["admin"])
def question_detail(version_id: UUID, user=Depends(admin_user), conn=database):
    from app.services.authoring import question_detail

    return question_detail(conn, version_id)


@router.get(
    "/admin/assessments", response_model=list[schemas_catalog.AssessmentResponse], tags=["admin"]
)
def admin_assessments(grade: Grade = 4, user=Depends(admin_user), conn=database):
    rows = assessment_list(conn, grade, published_only=False)
    attempts = db.table("attempts")
    return [
        {
            **dict(row),
            **access.content_access(conn, user, "assessment", row["id"], grade),
            "attempt_count": conn.execute(
                select(func.count())
                .select_from(attempts)
                .where(attempts.c.assessment_id == row["id"])
            ).scalar_one(),
        }
        for row in rows
    ]


@router.get("/admin/curriculum", response_model=dict[str, list[dict]], tags=["admin"])
def curriculum(grade: Grade = 4, user=Depends(admin_user), conn=database):
    topics, lessons, skills, subjects = (
        db.table(name) for name in ("topics", "lessons", "skills", "subjects")
    )
    return dict(
        subjects=conn.execute(select(subjects)).mappings().all(),
        topics=conn.execute(select(topics).where(topics.c.grade == grade)).mappings().all(),
        lessons=conn.execute(select(lessons).join(topics).where(topics.c.grade == grade))
        .mappings()
        .all(),
        skills=conn.execute(select(skills).where(skills.c.grade == grade)).mappings().all(),
    )
