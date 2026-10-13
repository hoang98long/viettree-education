from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from app.core.dependencies import database
from app.core.security import admin_user
from app.db import db
from app.schemas.authoring import (
    AssessmentInput,
    AssignmentInput,
    CloneAssessment,
    ContentAction,
    QuestionInput,
)
from app.services import authoring

router = APIRouter(prefix="/api/v1/admin/authoring", tags=["authoring"])


@router.get("/options")
def options(grade: int = Query(4, ge=1, le=5), user=Depends(admin_user), conn=database):
    subjects, topics, skills, lessons = (
        db.table(name) for name in ("subjects", "topics", "skills", "lessons")
    )
    return {
        "subjects": list(
            conn.execute(
                select(subjects.c.id, subjects.c.code, subjects.c.name_vi)
                .where(subjects.c.is_active.is_(True))
                .order_by(subjects.c.sort_order)
            ).mappings()
        ),
        "topics": list(
            conn.execute(
                select(topics.c.id, topics.c.subject_id, topics.c.title)
                .where(topics.c.grade == grade, topics.c.is_active.is_(True))
                .order_by(topics.c.sort_order)
            ).mappings()
        ),
        "skills": list(
            conn.execute(
                select(skills.c.id, skills.c.subject_id, skills.c.topic_id, skills.c.name)
                .where(skills.c.grade == grade, skills.c.is_active.is_(True))
                .order_by(skills.c.sort_order)
            ).mappings()
        ),
        "lessons": list(
            conn.execute(
                select(lessons.c.id, lessons.c.topic_id, lessons.c.title)
                .join(topics)
                .where(topics.c.grade == grade, lessons.c.status == "published")
                .order_by(lessons.c.sort_order)
            ).mappings()
        ),
    }


@router.post("/questions")
def create_question(payload: QuestionInput, user=Depends(admin_user), conn=database):
    return authoring.save_question(conn, user["id"], payload)


@router.get("/questions/{identifier}")
def question(identifier: UUID, user=Depends(admin_user), conn=database):
    return authoring.question_detail(conn, identifier)


@router.put("/questions/{identifier}")
def edit_question(
    identifier: UUID, payload: QuestionInput, user=Depends(admin_user), conn=database
):
    return authoring.save_question(conn, user["id"], payload, identifier)


@router.post("/questions/{identifier}/revise")
def revise_question(identifier: UUID, user=Depends(admin_user), conn=database):
    return authoring.revise_question(conn, user["id"], identifier)


@router.post("/questions/{identifier}/{action}")
def question_action(
    identifier: UUID,
    action: Literal["review", "publish", "archive"],
    payload: ContentAction,
    user=Depends(admin_user),
    conn=database,
):
    return authoring.question_action(conn, user["id"], identifier, action, payload)


@router.post("/assessments")
def create_assessment(payload: AssessmentInput, user=Depends(admin_user), conn=database):
    return authoring.save_assessment(conn, user["id"], payload)


@router.get("/assessments/{identifier}")
def assessment(identifier: UUID, user=Depends(admin_user), conn=database):
    return authoring.assessment_detail(conn, identifier)


@router.put("/assessments/{identifier}")
def edit_assessment(
    identifier: UUID, payload: AssessmentInput, user=Depends(admin_user), conn=database
):
    return authoring.save_assessment(conn, user["id"], payload, identifier)


@router.post("/assessments/{identifier}/clone")
def clone_assessment(
    identifier: UUID, payload: CloneAssessment, user=Depends(admin_user), conn=database
):
    return authoring.clone_assessment(conn, user["id"], identifier, payload.code)


@router.post("/assessments/{identifier}/assign")
def assign(identifier: UUID, payload: AssignmentInput, user=Depends(admin_user), conn=database):
    return authoring.assign_students(conn, user["id"], identifier, payload)


@router.post("/assessments/{identifier}/{action}")
def assessment_action(
    identifier: UUID,
    action: Literal["review", "publish", "archive"],
    payload: ContentAction,
    user=Depends(admin_user),
    conn=database,
):
    return authoring.assessment_action(conn, user["id"], identifier, action, payload)
