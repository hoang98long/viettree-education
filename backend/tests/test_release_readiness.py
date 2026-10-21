import json

import pytest
from sqlalchemy import select, text

from app.core.config import settings
from app.db import db
from app.services.release_readiness import curriculum_inventory, release_report


@pytest.mark.integration
def test_release_api_is_admin_only_and_returns_no_student_answers(logged_student, conn):
    client = logged_student
    path = "/api/v1/admin/release-status"
    assert client.get(path).status_code == 403
    result = client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": settings().seed_admin_password}
    )
    assert result.status_code == 200
    response = client.get(path)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    report = response.json()
    assert len(report["curriculum"]) == 15
    assert report["academy"]["baseline_published"] == report["academy"]["baseline_required"] == 200
    assert report["media"]["valid"]
    assert all(row["ok"] for row in report["curriculum"])
    assert all(
        key not in response.text
        for key in ('"password_hash"', '"grading"', '"payload"', '"answers"')
    )
    token = client.cookies["viettree_csrf"]
    client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": token})
    assert client.get(path).status_code == 401


@pytest.mark.integration
def test_release_inventory_detects_archived_grade_subject_without_counting_drafts(conn):
    lessons, topics = db.table("lessons"), db.table("topics")
    english = conn.execute(
        select(db.table("subjects").c.id).where(db.table("subjects").c.code == "ENGLISH")
    ).scalar_one()
    conn.execute(
        lessons.update()
        .where(
            lessons.c.topic_id.in_(
                select(topics.c.id).where(topics.c.grade == 1, topics.c.subject_id == english)
            )
        )
        .values(status="archived")
    )
    row = next(
        row
        for row in curriculum_inventory(conn)
        if row["grade"] == 1 and row["subject_code"] == "ENGLISH"
    )
    assert row["actual"]["lessons"] == 0
    assert not row["ok"]
    report = release_report(conn)
    failed = next(item for item in report["checks"] if item["code"] == "curriculum_coverage")
    assert not failed["ok"] and failed["count"] == 1
    assert any(step["code"] == "curriculum_coverage" for step in report["next_steps"])


@pytest.mark.integration
def test_release_report_runs_in_read_only_transaction_and_handles_broken_media(
    test_engine, monkeypatch
):
    with test_engine.begin() as conn:
        conn.execute(text("SET TRANSACTION READ ONLY"))
        db.load(conn)
        before = release_report(conn)
        assert before["media"]["valid"]

        def broken():
            raise ValueError("private-file-path-with-secret")

        monkeypatch.setattr("app.services.release_readiness.validate_manifest", broken)
        after = release_report(conn)
        assert after["status"] == "attention" and not after["media"]["valid"]
        assert "private-file-path-with-secret" not in json.dumps(after, default=str)
        assert any(step["code"] == "academy_files" for step in after["next_steps"])


@pytest.mark.integration
def test_release_detects_unapproved_ai_picture(conn):
    media = db.table("ai_media_assets")
    conn.execute(media.update().where(media.c.code == "AI1-39-v2-hero").values(status="review"))
    report = release_report(conn)
    assert any(
        issue == {"code": "AI1-39", "reason": "missing_approved_media"}
        for issue in report["academy"]["issues"]
    )
    assert not next(check for check in report["checks"] if check["code"] == "academy_content")["ok"]
