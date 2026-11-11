"""Media policy regressions, using real SQL on isolated in-memory tables."""

from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine

from app.academy import access


@pytest.fixture
def media_policy(monkeypatch):
    metadata = MetaData()
    lessons = Table(
        "ai_lessons",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("code", String),
        Column("minimum_plan_code", String),
    )
    versions = Table(
        "ai_lesson_versions",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("lesson_id", ForeignKey("ai_lessons.id")),
        Column("status", String),
    )
    usages = Table(
        "ai_media_usages",
        metadata,
        Column("asset_id", String),
        Column("lesson_version_id", ForeignKey("ai_lesson_versions.id")),
    )
    links = Table(
        "guardian_students",
        metadata,
        Column("guardian_user_id", String),
        Column("student_id", String),
        Column("verified_at", String),
    )
    tables = {table.name: table for table in (lessons, versions, usages, links)}
    monkeypatch.setattr(access.db, "table", lambda name: tables[name])
    monkeypatch.setattr(
        access, "resolve_membership", lambda conn, identifier: {"plan_code": "free"}
    )
    storage = create_engine("sqlite+pysqlite:///:memory:")
    metadata.create_all(storage)
    with storage.begin() as conn:
        conn.execute(
            lessons.insert(),
            [
                {"id": 1, "code": "AI4-02", "minimum_plan_code": "vip"},
                {"id": 2, "code": "AI1-01", "minimum_plan_code": "free"},
            ],
        )
        yield conn, tables
    storage.dispose()


def picture(code="AI4-02-v2-item-2", *, bundled=True):
    return {"id": str(uuid4()), "code": code, "category": "lesson", "bundled": bundled}


STUDENT = {"id": "learner", "roles": ["student"]}


@pytest.mark.parametrize(
    "code",
    [
        "AI4-02-support-1",
        "AI4-02-v2-item-2",
        "AI4-02-color-v3-item-2",
        "AI4-02-review-v3-item-2",
    ],
)
def test_orphan_bundled_legacy_media_does_not_bypass_vip(media_policy, code):
    conn, _ = media_policy
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, picture(code))
    assert error.value.status_code == 403


def test_bundled_legacy_art_uses_live_lesson_policy_not_static_default(media_policy):
    conn, tables = media_policy
    # The configured policy, including custom changes, wins over FREE_CODES.
    conn.execute(
        tables["ai_lessons"]
        .update()
        .where(tables["ai_lessons"].c.id == 2)
        .values(minimum_plan_code="vip")
    )
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, picture("AI1-01-v2-item-1"))
    assert error.value.status_code == 403
    conn.execute(
        tables["ai_lessons"]
        .update()
        .where(tables["ai_lessons"].c.id == 1)
        .values(minimum_plan_code="free")
    )
    access.media_access(conn, STUDENT, picture())


def test_vip_revocation_is_observed_for_same_orphan_asset(media_policy, monkeypatch):
    conn, _ = media_policy
    plan = {"plan_code": "vip"}
    monkeypatch.setattr(access, "resolve_membership", lambda conn, identifier: plan)
    image = picture()
    access.media_access(conn, STUDENT, image)
    plan["plan_code"] = "free"
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, image)
    assert error.value.status_code == 403


def test_archived_vip_usage_remains_restricted(media_policy):
    conn, tables = media_policy
    image = picture("generated-for-vip", bundled=False)
    conn.execute(tables["ai_lesson_versions"].insert().values(id=1, lesson_id=1, status="archived"))
    conn.execute(
        tables["ai_media_usages"].insert().values(asset_id=image["id"], lesson_version_id=1)
    )
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, image)
    assert error.value.status_code == 403


def test_media_deliberately_shared_with_a_free_lesson_stays_accessible(media_policy):
    conn, tables = media_policy
    image = picture()
    conn.execute(
        tables["ai_lesson_versions"].insert(),
        [
            {"id": 1, "lesson_id": 1, "status": "archived"},
            {"id": 2, "lesson_id": 2, "status": "published"},
        ],
    )
    conn.execute(
        tables["ai_media_usages"].insert(),
        [{"asset_id": image["id"], "lesson_version_id": identifier} for identifier in (1, 2)],
    )
    access.media_access(conn, STUDENT, image)


def test_a_free_draft_does_not_unlock_an_existing_vip_image(media_policy):
    conn, tables = media_policy
    image = picture()
    conn.execute(
        tables["ai_lesson_versions"].insert(),
        [
            {"id": 1, "lesson_id": 1, "status": "archived"},
            {"id": 2, "lesson_id": 2, "status": "draft"},
        ],
    )
    conn.execute(
        tables["ai_media_usages"].insert(),
        [{"asset_id": image["id"], "lesson_version_id": identifier} for identifier in (1, 2)],
    )
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, image)
    assert error.value.status_code == 403


@pytest.mark.parametrize("code,bundled", [("AI1-01-v2-item-1", False), ("unlinked-image", True)])
@pytest.mark.parametrize("plan", ["free", "vip"])
def test_unknown_or_unlinked_upload_does_not_infer_access_from_its_name(
    media_policy, monkeypatch, code, bundled, plan
):
    conn, _ = media_policy
    monkeypatch.setattr(access, "resolve_membership", lambda conn, identifier: {"plan_code": plan})
    with pytest.raises(HTTPException) as error:
        access.media_access(conn, STUDENT, picture(code, bundled=bundled))
    assert error.value.status_code == 403
    assert error.value.detail["code"] == "MEDIA_NOT_ASSIGNED"


@pytest.mark.parametrize("verified", [None, "verified"])
def test_guardian_needs_verified_link_to_vip_child(media_policy, monkeypatch, verified):
    conn, tables = media_policy
    conn.execute(
        tables["guardian_students"]
        .insert()
        .values(guardian_user_id="parent", student_id="child", verified_at=verified)
    )
    monkeypatch.setattr(access, "resolve_membership", lambda conn, identifier: {"plan_code": "vip"})
    guardian = {"id": "parent", "roles": ["guardian"]}
    if verified:
        access.media_access(conn, guardian, picture())
    else:
        with pytest.raises(HTTPException) as error:
            access.media_access(conn, guardian, picture())
        assert error.value.status_code == 403


@pytest.mark.parametrize("category", ["hero", "cover", "mascot", "card", "badge", "ui"])
def test_preview_categories_remain_available_without_lesson_policy(category):
    image = {**picture(), "category": category}
    access.media_access(None, STUDENT, image)


@pytest.mark.parametrize("role", ["admin", "teacher"])
def test_staff_can_review_unassigned_media(role):
    access.media_access(None, {"id": "staff", "roles": [role]}, picture("unlinked-image"))
