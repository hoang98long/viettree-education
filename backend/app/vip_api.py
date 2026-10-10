from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import student_user
from app.db import connection
from app.schemas import AnswerInput
from app.services import vip

router = APIRouter(prefix="/api/v1/students/me/vip", tags=["vip"])


@router.get("/library", response_model=dict)
def library(user=Depends(student_user), conn=Depends(connection)):
    return vip.library(conn, user)


@router.get("/mistakes", response_model=dict)
def mistakes(
    subject_code: str | None = Query(None, max_length=30),
    page: int = Query(1, ge=1, le=10000),
    user=Depends(student_user),
    conn=Depends(connection),
):
    return vip.mistakes(conn, user["id"], subject_code, page)


@router.post("/mistakes/{answer_id}/check", response_model=dict)
def check(
    answer_id: UUID, payload: AnswerInput, user=Depends(student_user), conn=Depends(connection)
):
    return vip.check_mistake(conn, user["id"], answer_id, payload)


@router.get("/report", response_model=dict)
def report(days: int = Query(7, ge=7, le=30), user=Depends(student_user), conn=Depends(connection)):
    if days not in (7, 30):
        raise HTTPException(422, "Chọn báo cáo 7 hoặc 30 ngày")
    return vip.report(conn, user["id"], days)
