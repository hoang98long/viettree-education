from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select

import app.schemas.catalog as schemas_catalog
from app.core.dependencies import database
from app.core.security import (
    current_user,
    student_user,
)
from app.db import db
from app.schemas.common import Grade
from app.services import access
from app.services import attempts as service
from app.services.catalog import assessment_list

router = APIRouter(prefix="/api/v1")


@router.get(
    "/assessments", response_model=list[schemas_catalog.AssessmentResponse], tags=["curriculum"]
)
def assessments(
    grade: Grade = 4,
    subject_code: str | None = None,
    user=Depends(current_user),
    conn=database,
):
    return [
        {**dict(row), **access.content_access(conn, user, "assessment", row["id"], grade)}
        for row in assessment_list(conn, grade, subject_code)
    ]


@router.get(
    "/assessments/{assessment_id}",
    response_model=schemas_catalog.AssessmentResponse,
    tags=["curriculum"],
)
def assessment(assessment_id: UUID, user=Depends(current_user), conn=database):
    row = service.published_assessment(conn, assessment_id)
    return next(
        {**dict(item), **access.content_access(conn, user, "assessment", item["id"], row["grade"])}
        for item in assessment_list(conn, row["grade"])
        if item["id"] == assessment_id
    )


@router.post(
    "/students/me/assessments/{assessment_id}/assign-self",
    response_model=schemas_catalog.AssignmentResponse,
    tags=["student"],
)
def assign(assessment_id: UUID, user=Depends(student_user), conn=database):
    return service.assign_self(conn, user["id"], assessment_id)


@router.get(
    "/students/me/assignments",
    response_model=list[schemas_catalog.AssignmentResponse],
    tags=["student"],
)
def assignments(user=Depends(student_user), conn=database):
    table, assessments = db.table("student_assignments"), db.table("assessments")
    rows = (
        conn.execute(
            select(table, assessments.c.title)
            .join(assessments)
            .where(table.c.student_id == user["id"])
            .order_by(table.c.created_at.desc())
        )
        .mappings()
        .all()
    )
    return [
        row
        for row in rows
        if access.eligible(conn, user["id"], "assessment", row["assessment_id"], None)
    ]
