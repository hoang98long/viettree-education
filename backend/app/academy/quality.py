"""Read-only checks for published Academy content; never repair teacher work."""

from pydantic import ValidationError
from sqlalchemy import select

from app.academy.curriculum import records
from app.academy.schemas import LessonContent
from app.db import db


def report(conn):
    lessons, versions = db.table("ai_lessons"), db.table("ai_lesson_versions")
    published = list(
        conn.execute(
            select(lessons.c.code, versions.c.payload)
            .join(versions)
            .where(versions.c.status == "published")
        ).mappings()
    )
    expected = {row["code"] for row in records()}
    available = {row["code"] for row in published}
    assets = {
        row.code
        for row in conn.execute(
            select(db.table("ai_media_assets").c.code).where(
                db.table("ai_media_assets").c.status == "approved"
            )
        )
    }
    issues = [
        {"code": code, "reason": "baseline_not_published"} for code in sorted(expected - available)
    ]
    for row in published:
        try:
            body = LessonContent.model_validate(row["payload"]).model_dump()
        except ValidationError:
            issues.append({"code": row["code"], "reason": "invalid_lesson_structure"})
            continue
        references = {
            body["hero"],
            *body["cards"],
            *[asset for step in body["steps"] for asset in step["media"]],
            *[
                item["asset"]
                for step in body["steps"]
                if step.get("activity")
                for item in step["activity"]["items"]
                if item.get("asset")
            ],
        }
        if not references <= assets:
            issues.append({"code": row["code"], "reason": "missing_approved_media"})
    for project in conn.execute(select(db.table("ai_projects"))).mappings():
        rubric = project["rubric"]
        if (
            set(rubric) != {"understanding", "practice", "creativity", "safety"}
            or any(not isinstance(n, (float, int)) or not 0 <= n <= 100 for n in rubric.values())
            or sum(rubric.values()) != 100
        ):
            issues.append({"code": project["code"], "reason": "invalid_rubric"})
    return {
        "baseline_published": len(expected & available),
        "baseline_required": len(expected),
        "issues": issues,
    }
