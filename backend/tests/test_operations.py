import json
from datetime import timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import func, select

from app.bootstrap import bootstrap_admin
from app.core.config import Settings, settings
from app.core.security import digest, now, throttle_login, verify_password
from app.db import SchemaNotReady, db
from app.main import app
from app.operations import Readiness, cleanup_auth, expected_heads, system_report


@pytest.mark.parametrize(
    "origin",
    [
        "",
        ",,",
        "*",
        "https://*.example.com",
        "https://",
        "https://example.com/path",
        "https://user:pass@example.com",
        "https://example.com?next=1",
        "https://example.com#page",
        "https://example.com:0",
        "https://example.com:99999",
        "https://exa mple.com",
        "https://example.com\\evil",
    ],
)
def test_config_rejects_invalid_origins(origin, monkeypatch):
    monkeypatch.delenv("ALLOWED_ORIGINS", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None, allowed_origins=origin)


def test_production_config_and_env_typos(monkeypatch):
    for name in ("APP_ENV", "COOKIE_SECURE", "DB_USER", "DB_PASSWORD", "ALLOWED_ORIGINS"):
        monkeypatch.delenv(name, raising=False)
    valid = dict(
        app_env="production",
        cookie_secure=True,
        db_user="viettree_app",
        db_password="a sufficiently long password",
        allowed_origins="https://hoc.example.com",
    )
    assert Settings(_env_file=None, **valid).origins == ["https://hoc.example.com"]
    for change in (
        dict(app_env="prodction"),
        dict(cookie_secure=False),
        dict(db_user="postgres"),
        dict(db_password="short"),
        dict(db_password="CHANGE_ME_UNIQUE_APP_PASSWORD"),
        dict(allowed_origins="http://hoc.example.com"),
    ):
        with pytest.raises(ValidationError) as failure:
            Settings(_env_file=None, **(valid | change))
        assert valid["db_password"] not in str(failure.value)


def test_ready_caches_structure_but_checks_migration_each_time(monkeypatch):
    checker, conn = Readiness(), Mock()
    validate = Mock()
    clock = [100.0]
    monkeypatch.setattr("app.operations.db.validate", validate)
    monkeypatch.setattr("app.operations.time.monotonic", lambda: clock[0])
    monkeypatch.setattr("app.operations.current_heads", lambda _: expected_heads())
    checker.check(conn)
    clock[0] += 59
    checker.check(conn)
    assert validate.call_count == 1
    clock[0] += 1
    checker.check(conn)
    assert validate.call_count == 2
    monkeypatch.setattr("app.operations.current_heads", lambda _: ["0008_account_management"])
    with pytest.raises(SchemaNotReady):
        checker.check(conn)


def test_ready_does_not_cache_schema_failure(monkeypatch):
    checker = Readiness()
    validate = Mock(side_effect=[SchemaNotReady("missing"), None])
    monkeypatch.setattr("app.operations.db.validate", validate)
    monkeypatch.setattr("app.operations.current_heads", lambda _: expected_heads())
    with pytest.raises(SchemaNotReady):
        checker.check(Mock())
    checker.check(Mock())
    assert validate.call_count == 2


def test_login_limits_canonical_account_and_ignores_forwarded_headers(monkeypatch):
    counter = {}

    def throttle(key, maximum):
        counter[key] = counter.get(key, 0) + 1
        return counter[key] > maximum

    monkeypatch.setattr("app.core.security._throttle", throttle)
    request = Request(
        {
            "type": "http",
            "client": ("school-ip", 1000),
            "headers": [(b"x-forwarded-for", b"forged-ip")],
        }
    )
    for number in range(30):
        assert not throttle_login(request, f"student-{number}")
    for _ in range(10):
        assert not throttle_login(request, " ADMIN ")
    assert throttle_login(request, "admin")
    assert counter["login-account:admin"] == 11
    assert all("forged-ip" not in key for key in counter)


def test_login_ip_limit_stops_before_adding_new_account_key(monkeypatch):
    calls = []

    def throttle(key, maximum):
        calls.append(key)
        return True

    monkeypatch.setattr("app.core.security._throttle", throttle)
    request = Request({"type": "http", "client": ("ip", 1000), "headers": []})
    assert throttle_login(request, "never-added")
    assert calls == ["login-ip:ip"]


@pytest.mark.integration
def test_login_accepts_many_accounts_from_school_ip_and_limits_shared_account(client):
    suffix = str(uuid4())
    for number in range(15):
        result = client.post(
            "/api/v1/auth/login",
            json={"username": f"missing-{number}-{suffix}", "password": "wrong"},
        )
        assert result.status_code == 401
    name = "target-" + suffix
    for _ in range(10):
        assert (
            client.post(
                "/api/v1/auth/login", json={"username": name, "password": "wrong"}
            ).status_code
            == 401
        )
    assert (
        client.post(
            "/api/v1/auth/login", json={"username": name.upper(), "password": "wrong"}
        ).status_code
        == 429
    )


def test_unexpected_error_has_safe_response_and_correlated_log(monkeypatch, caplog):
    def fail():
        raise ValueError("private password=secret-answer")

    monkeypatch.setattr("app.main.engine", fail)
    with TestClient(app) as client:
        response = client.get("/ready", headers={"X-Request-ID": "untrusted-password"})
        assert response.status_code == 500
        assert response.headers["cache-control"] == "no-store"
        request_id = response.headers["x-request-id"]
        assert len(request_id) == 32
        assert request_id[:12] in response.json()["detail"]
        assert "secret-answer" not in response.text + caplog.text
        assert "untrusted-password" not in caplog.text
        assert request_id in caplog.text
        assert client.get("/health").status_code == 200


@pytest.mark.integration
def test_ready_fails_on_outdated_revision(client, conn, test_engine, monkeypatch):
    monkeypatch.setattr("app.main.engine", lambda: test_engine)
    assert client.get("/ready").status_code == 200
    monkeypatch.setattr("app.operations.current_heads", lambda _: ["0008_account_management"])
    assert client.get("/ready").status_code == 503


@pytest.mark.integration
def test_system_status_is_admin_only_and_read_only(client, conn):
    assert client.get("/api/v1/admin/system-status").status_code == 401
    client.post(
        "/api/v1/auth/login",
        json={"username": "longnh", "password": settings().seed_student_password},
    )
    assert client.get("/api/v1/admin/system-status").status_code == 403
    client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": settings().seed_admin_password}
    )
    sessions = db.table("auth_sessions")
    before = conn.execute(select(func.count()).select_from(sessions)).scalar_one()
    response = client.get("/api/v1/admin/system-status")
    assert response.status_code == 200, response.text
    report = response.json()
    assert report["status"] == "ok", report
    assert report["migrations"]["current"] == expected_heads()
    assert response.headers["cache-control"] == "no-store"
    assert conn.execute(select(func.count()).select_from(sessions)).scalar_one() == before
    for secret in ("password", "csrf_hash", "token_hash", "email", "db_host", "student_id"):
        assert secret not in json.dumps(report).lower()


@pytest.mark.integration
def test_system_report_flags_missing_policy_but_allows_archived_pinned_questions(conn):
    lessons, policies, versions, items = (
        db.table(name)
        for name in ("lessons", "content_access_policies", "question_versions", "assessment_items")
    )
    lesson_id = conn.execute(
        select(lessons.c.id).where(lessons.c.status == "published").limit(1)
    ).scalar_one()
    conn.execute(policies.delete().where(policies.c.lesson_id == lesson_id))
    version_id = conn.execute(select(items.c.question_version_id).limit(1)).scalar_one()
    conn.execute(versions.update().where(versions.c.id == version_id).values(status="archived"))
    report = system_report(conn)
    checks = {check["code"]: check for check in report["checks"]}
    assert report["status"] == "attention"
    assert checks["lesson_policies"]["count"] == 1
    assert checks["assessment_items"]["ok"]


@pytest.mark.integration
def test_cleanup_preserves_live_sessions_recent_limits_audit_and_learning(conn):
    sessions, limits, users = (
        db.table(name) for name in ("auth_sessions", "auth_login_limits", "users")
    )
    user_id = conn.execute(select(users.c.id).limit(1)).scalar_one()
    at = now()
    ids = {}
    for name, expiry, revoked in (
        ("expired_old", at - timedelta(days=31), None),
        ("revoked_old", at + timedelta(days=1), at - timedelta(days=31)),
        ("expired_recent", at - timedelta(days=1), None),
        ("live", at + timedelta(days=1), None),
    ):
        key = digest(str(uuid4()))
        ids[name] = key
        conn.execute(
            sessions.insert().values(
                token_hash=key,
                user_id=user_id,
                csrf_hash=digest(str(uuid4())),
                expires_at=expiry,
                revoked_at=revoked,
            )
        )
    limit_keys = [digest(str(uuid4())), digest(str(uuid4()))]
    for key, age in zip(limit_keys, (31, 0), strict=True):
        conn.execute(
            limits.insert().values(key_hash=key, window_start=at - timedelta(days=age), failures=10)
        )
    protected = [db.table(name) for name in ("audit_logs", "attempts", "learning_events", "users")]
    before = [
        conn.execute(select(func.count()).select_from(table)).scalar_one() for table in protected
    ]
    dry_run = cleanup_auth(conn)
    assert dry_run["mode"] == "dry_run"
    assert conn.execute(
        select(sessions.c.token_hash).where(sessions.c.token_hash == ids["expired_old"])
    ).first()
    assert cleanup_auth(conn, apply=True)["counts"]["auth_sessions"] >= 2
    remaining = set(
        conn.execute(
            select(sessions.c.token_hash).where(sessions.c.token_hash.in_(ids.values()))
        ).scalars()
    )
    assert remaining == {ids["expired_recent"], ids["live"]}
    assert set(
        conn.execute(select(limits.c.key_hash).where(limits.c.key_hash.in_(limit_keys))).scalars()
    ) == {limit_keys[1]}
    assert before == [
        conn.execute(select(func.count()).select_from(table)).scalar_one() for table in protected
    ]
    assert cleanup_auth(conn)["counts"] == {"auth_sessions": 0, "auth_login_limits": 0}


@pytest.mark.integration
def test_bootstrap_cannot_replace_existing_admin_or_existing_user(conn):
    with pytest.raises(ValueError, match="quản trị"):
        bootstrap_admin(conn, "initial-admin", "Quản trị", "a long new admin password")
    users = db.table("users")
    conn.execute(users.update().values(is_active=False))
    old_hash = conn.execute(
        select(users.c.password_hash).where(users.c.username == "longnh")
    ).scalar_one()
    with pytest.raises(ValueError, match="tồn tại"):
        bootstrap_admin(conn, "longnh", "Quản trị", "a long new admin password")
    assert (
        conn.execute(select(users.c.password_hash).where(users.c.username == "longnh")).scalar_one()
        == old_hash
    )
    identifier = bootstrap_admin(conn, "INITIAL-ADMIN", "Quản trị", "a long new admin password")
    account = conn.execute(select(users).where(users.c.id == identifier)).mappings().one()
    assert account["username"] == "initial-admin"
    assert verify_password(account["password_hash"], "a long new admin password")
    assert not account["must_change_password"]
    assert (
        conn.execute(
            select(db.table("user_roles").c.role).where(
                db.table("user_roles").c.user_id == identifier
            )
        ).scalar_one()
        == "admin"
    )
