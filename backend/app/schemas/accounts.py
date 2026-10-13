import re
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator

from app.schemas.common import StrictModel, TextSize

Role = Literal["student", "guardian", "teacher", "admin"]
Password = Annotated[str, Field(min_length=15, max_length=256)]


def password_policy(value):
    if not value.strip() or value.casefold() in {
        "123456789012345",
        "passwordpassword",
        "qwertyuiopasdfgh",
    }:
        raise ValueError("Hãy chọn cụm mật khẩu khó đoán")
    return value


class AccountFields(StrictModel):
    username: str = Field(min_length=3, max_length=80)
    display_name: str = Field(min_length=1, max_length=160)
    email: str | None = Field(default=None, max_length=255)
    roles: list[Role] = Field(min_length=1, max_length=4)
    current_grade: int | None = Field(default=None, ge=1, le=5)
    text_size: TextSize = "comfortable"

    @field_validator("username")
    @classmethod
    def username_format(cls, value):
        value = value.strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,79}", value):
            raise ValueError("Tên đăng nhập dùng chữ không dấu, số, dấu chấm, gạch dưới/gạch ngang")
        return value

    @field_validator("display_name")
    @classmethod
    def name_format(cls, value):
        value = value.strip()
        if not value or any(ord(char) < 32 for char in value):
            raise ValueError("Tên hiển thị không hợp lệ")
        return value

    @field_validator("email")
    @classmethod
    def email_format(cls, value):
        if value is None or not value.strip():
            return None
        value = value.strip().lower()
        if not re.fullmatch(
            r"[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,63}", value
        ):
            raise ValueError("Email liên hệ chưa hợp lệ")
        return value

    @model_validator(mode="after")
    def student_grade(self):
        self.roles = sorted(set(self.roles))
        if "student" in self.roles and self.current_grade is None:
            raise ValueError("Học sinh cần lớp đang học")
        if "student" not in self.roles and self.current_grade is not None:
            raise ValueError("Chỉ sửa lớp khi tài khoản có vai trò học sinh")
        return self


class AdminAction(StrictModel):
    actor_password: str = Field(min_length=1, max_length=256)
    reason: str = Field(min_length=5, max_length=500)

    @field_validator("reason")
    @classmethod
    def reason_format(cls, value):
        value = value.strip()
        if len(value) < 5:
            raise ValueError("Cần lý do thao tác")
        return value


class AccountCreate(AccountFields, AdminAction):
    password: Password
    must_change_password: bool = True

    _password_policy = field_validator("password")(password_policy)


class AccountUpdate(AccountFields, AdminAction):
    revision: int = Field(ge=1)
    is_active: bool


class AccountReset(AdminAction):
    revision: int = Field(ge=1)
    new_password: Password
    _password_policy = field_validator("new_password")(password_policy)


class AccountRevoke(AdminAction):
    revision: int = Field(ge=1)


class ChangePassword(StrictModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: Password
    _password_policy = field_validator("new_password")(password_policy)


class RevokeOthers(StrictModel):
    current_password: str = Field(min_length=1, max_length=256)
