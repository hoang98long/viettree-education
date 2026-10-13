"""Publish a visual revision only over an unchanged bundled baseline.

Teacher edits/drafts and all historical versions and student progress are retained.
"""

import hashlib
import json
from pathlib import Path

from sqlalchemy import func, select, update

from app.academy.access import FREE_CODES
from app.academy.media import uid
from app.db import db

BASELINE = json.loads(
    (Path(__file__).parent / "data/baseline-v1-hashes.json").read_text(encoding="utf-8")
)
LEGACY_FREE = {"AI1-01", "AI2-01", "AI3-01", "AI4-01", "AI4-04", "AI4-27", "AI5-01"}
BASELINE.update(
    json.loads(
        (Path(__file__).parent / "data/color-baseline-v2-hashes.json").read_text(encoding="utf-8")
    )
)


def fingerprint(payload):
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def publish_visual_revision(conn, row, payload):
    lessons, versions = db.table("ai_lessons"), db.table("ai_lesson_versions")
    lesson_id = uid(row["code"])
    current = (
        conn.execute(select(lessons).where(lessons.c.id == lesson_id).with_for_update())
        .mappings()
        .one()
    )
    existing = list(
        conn.execute(
            select(versions).where(versions.c.lesson_id == lesson_id).order_by(versions.c.version)
        ).mappings()
    )
    if not existing:
        version_id, number = uid(row["code"] + "-version-1"), 1
    else:
        original = BASELINE.get(row["code"])
        if (
            len(existing) != 1
            or original is None
            or current["created_by"] is not None
            or current["revision"] != 1
            or current["minimum_plan_code"] != ("free" if row["code"] in LEGACY_FREE else "vip")
            or current["title"] != original["title"]
            or current["position"] != original["position"]
            or current["unit_id"] != uid(original["unit_code"])
            or existing[0]["created_by"] is not None
            or existing[0]["reviewed_by"] is not None
            or existing[0]["status"] != "published"
            or fingerprint(existing[0]["payload"]) != original["sha256"]
        ):
            return None
        conn.execute(
            update(versions).where(versions.c.id == existing[0]["id"]).values(status="archived")
        )
        conn.execute(
            update(lessons)
            .where(lessons.c.id == lesson_id)
            .values(
                title=row["title"],
                revision=lessons.c.revision + 1,
                updated_at=func.now(),
                minimum_plan_code="free" if row["code"] in FREE_CODES else "vip",
            )
        )
        version_id, number = uid(row["code"] + "-visual-version-2"), 2
    conn.execute(
        versions.insert().values(
            id=version_id,
            lesson_id=lesson_id,
            version=number,
            status="published",
            payload=payload,
            published_at=func.now(),
        )
    )
    return version_id
