from uuid import UUID

from fastapi import APIRouter, Depends, Request

import app.schemas.attempts as schemas_attempts
from app.core.dependencies import database
from app.core.security import (
    current_user,
    student_user,
)
from app.schemas.attempts import AnswerInput, AttemptResponse, StartInput
from app.services import attempts as service

router = APIRouter(prefix="/api/v1")


@router.post("/attempts", response_model=schemas_attempts.StartResponse, tags=["attempts"])
def start(payload: StartInput, user=Depends(student_user), conn=database):
    return service.start_attempt(conn, user["id"], payload.assignment_id)


@router.get("/attempts/{attempt_id}", response_model=AttemptResponse, tags=["attempts"])
def attempt(attempt_id: UUID, user=Depends(current_user), conn=database):
    return service.get_attempt(conn, user, attempt_id)


@router.put(
    "/attempts/{attempt_id}/answers/{item_id}", response_model=dict[str, bool], tags=["attempts"]
)
def answer(
    attempt_id: UUID,
    item_id: UUID,
    payload: AnswerInput,
    request: Request,
    user=Depends(student_user),
    conn=database,
):
    return service.save_answer(conn, user, attempt_id, item_id, payload, request.state.received_at)


@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=schemas_attempts.ResultResponse,
    tags=["attempts"],
)
def submit(attempt_id: UUID, user=Depends(student_user), conn=database):
    return service.submit(conn, user, attempt_id)


@router.get(
    "/attempts/{attempt_id}/result",
    response_model=schemas_attempts.ResultResponse,
    tags=["attempts"],
)
def result(attempt_id: UUID, user=Depends(current_user), conn=database):
    return service.result(conn, user, attempt_id)
