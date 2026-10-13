"""Explicit, repeatable development-only learner accounts requested by the owner."""

from uuid import uuid4

from sqlalchemy import select, text

from app.core.config import settings
from app.core.security import hasher
from app.core.seed_support import ensure
from app.curriculum.registry import SUPPORTED_GRADES
from app.db import db
from app.schemas.memberships import MembershipGrantInput
from app.services.access import resolve_membership
from app.services.memberships import change_membership


def seed_demo_learners(conn, grades=SUPPORTED_GRADES):
    config = settings()
    if config.app_env != "development" or not config.seed_student_password:
        raise RuntimeError("Chỉ tạo demo ở development và cần SEED_STUDENT_PASSWORD")
    grades = tuple(dict.fromkeys(grades))
    if not grades or any(grade not in SUPPORTED_GRADES for grade in grades):
        raise ValueError("Chọn ít nhất một khối đã có học liệu: 1–5")
    conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
    users, roles = db.table("users"), db.table("user_roles")
    admin_id = conn.execute(
        select(users.c.id).where(
            users.c.username == "admin",
            users.c.is_active.is_(True),
            select(roles.c.user_id)
            .where(roles.c.user_id == users.c.id, roles.c.role == "admin")
            .exists(),
        )
    ).scalar_one_or_none()
    if admin_id is None:
        raise RuntimeError("Cần tài khoản admin đang hoạt động để ghi audit cấp VIP demo")
    created = []
    catalogue = (
        (
            f"{plan}{grade}_{index:02}",
            name + (f" lớp {grade}" if grade != 4 else "") + f" ({plan.upper()} demo)",
            plan,
            grade,
        )
        for grade in grades
        for index, name, plan in (
            (1, "Minh Anh", "free"),
            (2, "Gia Bảo", "free"),
            (1, "Khánh Linh", "vip"),
            (2, "Đức Minh", "vip"),
        )
    )
    for username, name, plan, grade in catalogue:
        existing = (
            conn.execute(select(users).where(users.c.username == username)).mappings().first()
        )
        if existing:
            existing_roles = set(
                conn.execute(
                    select(roles.c.role).where(roles.c.user_id == existing["id"])
                ).scalars()
            )
            if existing_roles != {"student"}:
                raise RuntimeError(f"Tài khoản {username} có vai trò khác; không tự đổi quyền")
            actual_grade = conn.execute(
                select(db.table("student_profiles").c.current_grade).where(
                    db.table("student_profiles").c.student_id == existing["id"]
                )
            ).scalar_one_or_none()
            if actual_grade is None:
                raise RuntimeError(f"Tài khoản {username} thiếu hồ sơ; không tự sửa dữ liệu cũ")
            membership = resolve_membership(conn, existing["id"])
            created.append(
                {
                    "username": username,
                    "created": False,
                    "grade": actual_grade,
                    "current_plan": membership["plan_code"],
                }
            )
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
            {"current_grade": grade, "learning_preferences": {"language": "vi"}},
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
        created.append(
            {
                "username": username,
                "created": True,
                "grade": grade,
                "initial_plan": plan,
                "current_plan": plan,
            }
        )
    return created
