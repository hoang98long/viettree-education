from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.core.config import Settings, settings
from app.core.security import digest, now
from app.db import db


def test_session_duration_settings_are_bounded():
    for field, value in (
        ("session_hours", 0),
        ("session_hours", 25),
        ("remember_session_days", 0),
        ("remember_session_days", 31),
    ):
        with pytest.raises(ValidationError):
            Settings(_env_file=None, **{field: value})


def login(client, username="longnh", remember=False):
    return client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": (
                settings().seed_admin_password
                if username == "admin"
                else settings().seed_student_password
            ),
            "remember_me": remember,
        },
    )


@pytest.mark.integration
@pytest.mark.parametrize("remember", [False, True])
def test_cookie_and_database_share_session_deadline(client, conn, remember):
    before = now()
    response = login(client, remember=remember)
    assert response.status_code == 200
    duration = (
        timedelta(days=settings().remember_session_days)
        if remember
        else timedelta(hours=settings().session_hours)
    )
    expiry = datetime.fromisoformat(response.json()["session_expires_at"])
    assert before + duration <= expiry <= now() + duration
    token = client.cookies["viettree_session"]
    sessions = db.table("auth_sessions")
    stored = (
        conn.execute(select(sessions).where(sessions.c.token_hash == digest(token)))
        .mappings()
        .one()
    )
    assert stored["expires_at"] == expiry
    assert stored["token_hash"] != token
    for cookie in response.headers.get_list("set-cookie"):
        assert f"Max-Age={int(duration.total_seconds())}" in cookie
        assert "expires=" in cookie.lower()
        assert "SameSite=lax" in cookie
    assert "HttpOnly" in response.headers.get_list("set-cookie")[0]
    assert response.headers["cache-control"] == "no-store"
    assert (
        datetime.fromisoformat(client.get("/api/v1/auth/me").json()["session_expires_at"]) == expiry
    )


@pytest.mark.integration
@pytest.mark.parametrize("role", ["admin", "teacher"])
def test_privileged_student_cannot_request_long_session(client, conn, role):
    users = db.table("users")
    student_id = conn.execute(select(users.c.id).where(users.c.username == "longnh")).scalar_one()
    conn.execute(db.table("user_roles").insert().values(user_id=student_id, role=role))
    before = now()
    response = login(client, remember=True)
    assert response.status_code == 200
    expiry = datetime.fromisoformat(response.json()["session_expires_at"])
    assert expiry <= before + timedelta(hours=settings().session_hours, seconds=5)


@pytest.mark.integration
def test_admin_remember_uses_normal_session(client):
    response = login(client, username="admin", remember=True)
    assert response.status_code == 200
    assert f"Max-Age={settings().session_hours * 3600}" in response.headers["set-cookie"]


@pytest.mark.integration
def test_privileged_role_added_later_caps_existing_remembered_session(client, conn):
    response = login(client, remember=True)
    assert response.status_code == 200
    sessions = db.table("auth_sessions")
    user_id = response.json()["id"]
    token_hash = digest(client.cookies["viettree_session"])
    conn.execute(db.table("user_roles").insert().values(user_id=user_id, role="admin"))
    current = client.get("/api/v1/auth/me")
    assert current.status_code == 200
    assert datetime.fromisoformat(current.json()["session_expires_at"]) <= now() + timedelta(
        hours=settings().session_hours
    )
    conn.execute(
        sessions.update()
        .where(sessions.c.token_hash == token_hash)
        .values(created_at=now() - timedelta(hours=settings().session_hours, seconds=1))
    )
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.get("/api/v1/admin/statistics").status_code == 401


@pytest.mark.integration
def test_expiration_is_enforced_with_retained_cookie(client, conn):
    assert login(client, remember=True).status_code == 200
    sessions = db.table("auth_sessions")
    token = client.cookies["viettree_session"]
    conn.execute(
        sessions.update()
        .where(sessions.c.token_hash == digest(token))
        .values(expires_at=now() - timedelta(seconds=1))
    )
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.get("/api/v1/subjects?grade=4").status_code == 401


@pytest.mark.integration
def test_remembered_session_is_revocable_and_inactive_users_are_rejected(client, conn):
    assert login(client, remember=True).status_code == 200
    cookie = client.cookies["viettree_session"]
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert client.post("/api/v1/auth/logout").status_code == 200
    client.cookies.set("viettree_session", cookie)
    assert client.get("/api/v1/auth/me").status_code == 401
    client.cookies.clear()
    assert login(client, remember=True).status_code == 200
    user_id = client.get("/api/v1/auth/me").json()["id"]
    users = db.table("users")
    conn.execute(users.update().where(users.c.id == user_id).values(is_active=False))
    assert client.get("/api/v1/auth/me").status_code == 401


@pytest.mark.integration
def test_relogin_rotates_and_revokes_old_browser_session(client, conn):
    assert login(client).status_code == 200
    old = client.cookies["viettree_session"]
    assert login(client, remember=True).status_code == 200
    new = client.cookies["viettree_session"]
    assert old != new
    sessions = db.table("auth_sessions")
    assert (
        conn.execute(
            select(sessions.c.revoked_at).where(sessions.c.token_hash == digest(old))
        ).scalar_one()
        is not None
    )
    client.cookies.set("viettree_session", old)
    assert client.get("/api/v1/auth/me").status_code == 401


@pytest.mark.integration
def test_login_returns_saved_text_size_for_shared_session_cache(client, conn):
    users, profiles = db.table("users"), db.table("student_profiles")
    user_id = conn.execute(select(users.c.id).where(users.c.username == "longnh")).scalar_one()
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == user_id)
        .values(accessibility_options={"text_size": "large"})
    )
    response = login(client)
    assert response.status_code == 200
    assert response.json()["text_size"] == "large"
    assert client.get("/api/v1/auth/me").json()["text_size"] == "large"
