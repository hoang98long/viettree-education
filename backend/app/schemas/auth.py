from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.common import ReadingPreferences, StrictModel


class LoginInput(StrictModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=1, max_length=256)
    remember_me: bool = False


class UserResponse(ReadingPreferences):
    id: UUID
    username: str
    display_name: str
    roles: list[str]
    session_expires_at: datetime | None = None
    must_change_password: bool = False
