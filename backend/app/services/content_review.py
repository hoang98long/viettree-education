"""Apply reviewed lesson support only to an unchanged bundled source.

The previous content is retained in audit_logs. Questions, policies, drafts and
student progress are never rewritten by this command.
"""

import hashlib
import json
from pathlib import Path

from sqlalchemy import select, text

from app.core.security import now
from app.db import db
from app.schemas.lessons import LessonContent

CATALOG = json.loads(
    (Path(__file__).parents[1] / "curriculum/data/lesson-review-2026-11.json").read_text(
        encoding="utf-8"
    )
)


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def review_learning_content(conn, *, apply=False, grades=None):
    selected = set(grades or range(1, 6))
    if not selected <= set(range(1, 6)):
        raise ValueError("Chọn khối lớp 1–5")
    if apply:
        conn.execute(text("SELECT pg_advisory_xact_lock(78249104)"))
    lessons, drafts, logs = (db.table(n) for n in ("lessons", "lesson_drafts", "audit_logs"))
    report = {"release": CATALOG["release"], "applied": apply, "items": []}
    counts = {key: 0 for key in ("updated", "eligible", "current", "customized", "missing")}
    entries = [entry for entry in CATALOG["lessons"] if entry["grade"] in selected]
    statement = select(lessons).where(lessons.c.code.in_([entry["code"] for entry in entries]))
    if apply:
        statement = statement.order_by(lessons.c.code).with_for_update()
    rows = {row["code"]: row for row in conn.execute(statement).mappings()}
    drafted = set(
        conn.execute(
            select(drafts.c.lesson_id).where(
                drafts.c.lesson_id.in_([row["id"] for row in rows.values()])
            )
        ).scalars()
    )
    for entry in entries:
        row = rows.get(entry["code"])
        status = "missing"
        if row is not None:
            digest = fingerprint(row["content"])
            if digest == entry["after_sha256"]:
                status = "current"
            elif (
                digest != entry["before_sha256"]
                or row["created_by"] is not None
                or row["title"] != entry["title"]
                or row["status"] != "published"
                or row["id"] in drafted
            ):
                status = "customized"
            else:
                updated = {**row["content"], **entry["patch"]}
                LessonContent.model_validate(updated)
                if fingerprint(updated) != entry["after_sha256"]:
                    raise ValueError("Bản chỉnh sửa không khớp kiểm chứng nội dung")
                status = "eligible"
                if apply:
                    conn.execute(
                        lessons.update()
                        .where(lessons.c.id == row["id"])
                        .values(content=updated, updated_at=now())
                    )
                    conn.execute(
                        logs.insert().values(
                            action="authoring.lesson.editorial_review",
                            entity_type="lesson",
                            entity_id=row["id"],
                            old_values={"content": row["content"]},
                            new_values={
                                "content": updated,
                                "review_release": CATALOG["release"],
                                "reason": "Rà soát lời dẫn và minh họa theo bộ editorial-2026-11",
                            },
                        )
                    )
                    status = "updated"
        counts[status] += 1
        report["items"].append({"code": entry["code"], "grade": entry["grade"], "status": status})
    return {**report, "counts": counts}
