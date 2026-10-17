"""Training access is checked at the server, independently from progress and UI."""

from sqlalchemy import select

from app.db import db
from app.services.access import denied, require_feature, resolve_membership

FREE_CODES = (
    {f"AI{grade}-{number:02}" for grade in [1, 2, 3, 5] for number in [1, 2, 3]}
    | {
        "AI4-01",
        "AI4-04",
        "AI4-27",
    }
    | {f"AI{grade}-37" for grade in range(1, 6)}
)


def lesson_access(conn, user, lesson):
    if "student" in user["roles"] and lesson["minimum_plan_code"] == "vip":
        require_feature(conn, user["id"], "academy.full")


def student_feature(conn, user, feature):
    if "student" in user["roles"]:
        return require_feature(conn, user["id"], feature)


def media_access(conn, user, row):
    if {"teacher", "admin"} & set(user["roles"]) or row["category"] in {
        "hero",
        "cover",
        "mascot",
        "card",
        "badge",
        "ui",
    }:
        return
    usages, versions, lessons = (
        db.table(n) for n in ("ai_media_usages", "ai_lesson_versions", "ai_lessons")
    )
    plans = list(
        conn.execute(
            select(lessons.c.minimum_plan_code)
            .select_from(usages.join(versions).join(lessons))
            .where(usages.c.asset_id == row["id"])
        ).scalars()
    )
    entitled = (
        "student" in user["roles"] and resolve_membership(conn, user["id"])["plan_code"] == "vip"
    )
    if "guardian" in user["roles"]:
        links = db.table("guardian_students")
        entitled = entitled or any(
            resolve_membership(conn, identifier)["plan_code"] == "vip"
            for identifier in conn.execute(
                select(links.c.student_id).where(
                    links.c.guardian_user_id == user["id"], links.c.verified_at.is_not(None)
                )
            ).scalars()
        )
    if plans and "free" not in plans and not entitled:
        denied(
            message="Minh họa của bài này dành cho VIP; em có thể xem tranh bìa và bài nhập môn miễn phí."
        )
