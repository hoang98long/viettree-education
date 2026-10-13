from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field

from app.core.dependencies import database
from app.core.security import admin_user
from app.schemas.authoring import StrictModel
from app.schemas.lessons import LessonInput
from app.services import lesson_studio

router = APIRouter(prefix="/api/v1/admin/lessons", tags=["lesson-studio"])


class LessonAction(StrictModel):
    expected_revision: int = Field(ge=0)
    reason: str = Field(min_length=5, max_length=500)


@router.get("")
def listing(
    grade: int = Query(4, ge=1, le=5),
    subject_code: str | None = Query(None, max_length=30),
    status: Literal["draft", "published", "archived", "pending"] | None = None,
    search: str = Query("", max_length=120),
    page: int = Query(1, ge=1, le=10000),
    user=Depends(admin_user),
    conn=database,
):
    return lesson_studio.listing(conn, grade, subject_code, status, search, page)


@router.post("")
def create(payload: LessonInput, user=Depends(admin_user), conn=database):
    return lesson_studio.save(conn, user["id"], payload)


@router.get("/{identifier}")
def detail(identifier: UUID, user=Depends(admin_user), conn=database):
    return lesson_studio.detail(conn, identifier)


@router.put("/{identifier}")
def save(identifier: UUID, payload: LessonInput, user=Depends(admin_user), conn=database):
    return lesson_studio.save(conn, user["id"], payload, identifier)


@router.post("/{identifier}/{name}")
def action(
    identifier: UUID,
    name: Literal["review", "publish", "reset"],
    payload: LessonAction,
    user=Depends(admin_user),
    conn=database,
):
    return lesson_studio.action(conn, user["id"], identifier, name, payload)
