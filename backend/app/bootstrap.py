"""Tạo quản trị đầu tiên qua console; không reset tài khoản có sẵn."""

from pydantic import Field, field_validator
from sqlalchemy import func, select, text

from app.core.security import hasher, now
from app.db import db
from app.schemas.accounts import AccountFields, Password, Role, password_policy


class BootstrapAdmin(AccountFields):
    roles: list[Role] = Field(default_factory=lambda: ["admin"])
    password: Password

    _password_policy = field_validator("password")(password_policy)


def bootstrap_admin(conn, username, display_name, password):
    payload = BootstrapAdmin(username=username, display_name=display_name, password=password)
    conn.execute(text("SELECT pg_advisory_xact_lock(78249101)"))
    users, roles = db.table("users"), db.table("user_roles")
    if conn.execute(
        select(users.c.id).join(roles).where(users.c.is_active.is_(True), roles.c.role == "admin")
    ).first():
        raise ValueError("Đã có quản trị hoạt động. Hãy tạo tài khoản qua giao diện quản trị")
    if conn.execute(
        select(users.c.id).where(func.lower(users.c.username) == payload.username)
    ).first():
        raise ValueError("Tên đăng nhập đã tồn tại; công cụ không đổi mật khẩu hoặc vai trò cũ")
    identifier = conn.execute(
        users.insert()
        .values(
            username=payload.username,
            display_name=payload.display_name,
            password_hash=hasher.hash(payload.password),
            password_changed_at=now(),
        )
        .returning(users.c.id)
    ).scalar_one()
    conn.execute(roles.insert().values(user_id=identifier, role="admin"))
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            action="deployment.bootstrap_admin",
            entity_type="account",
            entity_id=identifier,
            new_values={"username": payload.username, "roles": ["admin"]},
        )
    )
    return identifier
