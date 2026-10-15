from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import database
from app.core.security import student_user
from app.schemas.common import StrictModel
from app.services.bookmarks import set_bookmark

router = APIRouter(prefix="/api/v1", tags=["bookmarks"])


class BookmarkInput(StrictModel):
    saved: bool


@router.put("/students/me/lessons/{lesson_id}/bookmark", response_model=dict[str, bool])
def bookmark(lesson_id: UUID, payload: BookmarkInput, user=Depends(student_user), conn=database):
    return set_bookmark(conn, user, lesson_id, payload.saved)
