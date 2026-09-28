import enum
from datetime import datetime
from uuid import UUID
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDTimestampMixin


class UserRole(str, enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(Base, UUIDTimestampMixin):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=UserRole.STUDENT,
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, values_callable=lambda enum_cls: [member.value for member in enum_cls]),
        default=UserStatus.ACTIVE,
        nullable=False,
    )

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE


class RefreshToken(Base, UUIDTimestampMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UUID] = mapped_column(index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(nullable=True, index=True)
    replaced_by_token_id: Mapped[UUID | None] = mapped_column(nullable=True)
