"""Explicit, repeatable development-only learner accounts requested by the owner."""

from uuid import uuid4

from sqlalchemy import select, text

from app.core.config import settings
from app.core.security import hasher
from app.db import db
from app.schemas import MembershipGrantInput
from app.seed import ensure
from app.services.memberships import change_membership


def seed_demo_learners(conn):
    config = settings()
    if config.app_env == "production" or not config.seed_student_password:
        raise RuntimeError("Chỉ tạo demo ở development và cần SEED_STUDENT_PASSWORD")
    conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
    users, roles = db.table("users"), db.table("user_roles")
    admin_id = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    created = []
    for username, name, plan in (
        ("free4_01", "Minh Anh (Free demo)", "free"),
        ("free4_02", "Gia Bảo (Free demo)", "free"),
        ("vip4_01", "Khánh Linh (VIP demo)", "vip"),
        ("vip4_02", "Đức Minh (VIP demo)", "vip"),
    ):
        existing = (
            conn.execute(select(users).where(users.c.username == username)).mappings().first()
        )
        if existing:
            if not conn.execute(
                select(roles.c.user_id).where(
                    roles.c.user_id == existing["id"], roles.c.role == "student"
                )
            ).first():
                raise RuntimeError(f"Tài khoản {username} có vai trò khác; không tự đổi quyền")
            created.append({"username": username, "created": False})
            continue  # Never reset passwords, renew or re-grant previously created learners.
        user, _ = ensure(
            conn,
            "users",
            {"username": username},
            {"display_name": name, "password_hash": hasher.hash(config.seed_student_password)},
            "extra-demo/" + username,
        )
        ensure(
            conn,
            "user_roles",
            {"user_id": user["id"], "role": "student"},
            {},
            "extra-demo-role/" + username,
        )
        ensure(
            conn,
            "student_profiles",
            {"student_id": user["id"]},
            {"current_grade": 4, "learning_preferences": {"language": "vi"}},
            "extra-demo-profile/" + username,
        )
        if plan == "vip":
            change_membership(
                conn,
                admin_id,
                user["id"],
                "grant",
                MembershipGrantInput(
                    duration_days=90, reason="Tài khoản VIP demo được chủ dự án yêu cầu"
                ),
                uuid4(),
            )
        created.append({"username": username, "created": True, "initial_plan": plan})
    return created
