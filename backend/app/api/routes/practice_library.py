from typing import Literal

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import database
from app.core.security import student_user
from app.schemas.practice_library import PracticeLibraryResponse
from app.services.practice_library import practice_library

router = APIRouter(prefix="/api/v1", tags=["practice-library"])


@router.get("/students/me/practice-library", response_model=PracticeLibraryResponse)
def library(
    subject_code: Literal["MATH", "VIETNAMESE", "ENGLISH"] | None = None,
    plan: Literal["all", "free", "vip"] = "all",
    progress: Literal["all", "not_started", "review", "mastered"] = "all",
    max_questions: int | None = Query(None, ge=1, le=8),
    search: str = Query("", max_length=80),
    page: int = Query(1, ge=1, le=10000),
    kind: Literal["all", "practice", "homework", "quiz", "test", "placement", "adaptive"] = "all",
    user=Depends(student_user),
    conn=database,
):
    return practice_library(
        conn, user, subject_code, plan, progress, max_questions, search, page, kind
    )
