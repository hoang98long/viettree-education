from typing import Literal

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import database
from app.core.security import student_user
from app.schemas.lesson_library import LessonLibraryResponse
from app.services.lesson_library import lesson_library

router = APIRouter(prefix="/api/v1", tags=["lesson-library"])


@router.get("/students/me/lesson-library", response_model=LessonLibraryResponse)
def library(
    subject_code: Literal["MATH", "VIETNAMESE", "ENGLISH"] | None = None,
    plan: Literal["all", "free", "vip"] = "all",
    progress: Literal["all", "not_started", "in_progress", "completed"] = "all",
    category: Literal["all", "core", "thinking"] = "all",
    search: str = Query("", max_length=80),
    page: int = Query(1, ge=1, le=10000),
    user=Depends(student_user),
    conn=database,
):
    return lesson_library(conn, user, subject_code, plan, progress, category, search, page)
