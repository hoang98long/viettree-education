from sqlalchemy import func, select

from app.core.config import settings
from app.core.security import hasher, now
from app.core.seed_support import ensure
from app.db import db


def seed_accounts(conn, reset=False):
    config = settings()
    if config.app_env == "production":
        raise RuntimeError("Không seed tài khoản demo trong production")
    for username, role, display_name, password in (
        ("admin", "admin", "Quản trị VietTree", config.seed_admin_password),
        ("longnh", "student", "Học sinh Long (demo)", config.seed_student_password),
    ):
        users, roles = db.table("users"), db.table("user_roles")
        user = (
            conn.execute(select(users).where(func.lower(users.c.username) == username))
            .mappings()
            .first()
        )
        if not user:
            if not password:
                raise RuntimeError(
                    "Cần khai báo SEED_ADMIN_PASSWORD và SEED_STUDENT_PASSWORD trong .env local"
                )
            user, _ = ensure(
                conn,
                "users",
                {"username": username},
                {"display_name": display_name, "password_hash": hasher.hash(password)},
                "user/" + username,
            )
            ensure(
                conn, "user_roles", {"user_id": user["id"], "role": role}, {}, "role/" + username
            )
        else:
            exists = conn.execute(
                select(roles.c.role).where(roles.c.user_id == user["id"], roles.c.role == role)
            ).scalar()
            if not exists:
                raise RuntimeError(
                    f"Tài khoản {username} đã tồn tại với vai trò khác; seed không tự nâng quyền"
                )
            if reset:
                if not password:
                    raise RuntimeError("Chưa cấu hình password seed")
                conn.execute(
                    users.update()
                    .where(users.c.id == user["id"])
                    .values(password_hash=hasher.hash(password))
                )
                sessions = db.table("auth_sessions")
                conn.execute(
                    sessions.update()
                    .where(sessions.c.user_id == user["id"], sessions.c.revoked_at.is_(None))
                    .values(revoked_at=now())
                )
        if role == "student":
            ensure(
                conn,
                "student_profiles",
                {"student_id": user["id"]},
                {
                    "current_grade": 4,
                    "learning_preferences": {"language": "vi", "session_minutes": 15},
                },
                "profile/" + username,
            )
