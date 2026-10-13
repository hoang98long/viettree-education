import json
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.core.security import digest, hasher, now
from app.db import db
from app.schemas.accounts import AccountCreate

ADMIN_PASSWORD = "Quan tri vien rieng 2026"
TEMP = "Mat khau tam lop bon 2026"
NEW = "Cum tu moi cua hoc sinh 2026"


def insert_user(conn, roles=("admin",), password=ADMIN_PASSWORD):
    user_id = uuid4()
    username = "account-" + str(user_id)
    conn.execute(
        db.table("users")
        .insert()
        .values(
            id=user_id,
            username=username,
            display_name="Kiểm thử tài khoản",
            password_hash=hasher.hash(password),
        )
    )
    conn.execute(
        db.table("user_roles").insert(), [{"user_id": user_id, "role": role} for role in roles]
    )
    if "student" in roles:
        conn.execute(
            db.table("student_profiles").insert().values(student_id=user_id, current_grade=4)
        )
    return user_id, username


def login_as(client, username, password):
    result = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert result.status_code == 200, result.text
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    return result


@pytest.fixture
def manager(client, conn):
    user_id, username = insert_user(conn)
    login_as(client, username, ADMIN_PASSWORD)
    return client, user_id


def payload(**changes):
    return {
        "username": "new-" + str(uuid4()),
        "display_name": "Em học sinh mới",
        "roles": ["student"],
        "current_grade": 4,
        "password": TEMP,
        "actor_password": ADMIN_PASSWORD,
        "reason": "Tạo học sinh kiểm thử",
        **changes,
    }


def create(client, **changes):
    result = client.post("/api/v1/admin/accounts", json=payload(**changes))
    assert result.status_code == 201, result.text
    return result.json()


def edit_payload(account, **changes):
    return {
        "username": account["username"],
        "display_name": account["display_name"],
        "email": account["email"],
        "roles": account["roles"],
        "is_active": account["is_active"],
        "current_grade": account["current_grade"] if "student" in account["roles"] else None,
        "text_size": account["text_size"],
        "revision": account["account_revision"],
        "actor_password": ADMIN_PASSWORD,
        "reason": "Điều chỉnh tài khoản kiểm thử",
        **changes,
    }


@pytest.mark.parametrize(
    "changes",
    [
        {"username": "ab"},
        {"username": "có dấu"},
        {"username": "abc def"},
        {"display_name": "  "},
        {"email": "not-an-email"},
        {"email": "x@bad..com"},
        {"roles": []},
        {"roles": ["root"]},
        {"current_grade": None},
        {"current_grade": 6},
        {"roles": ["teacher"], "current_grade": 4},
        {"password": "short"},
        {"password": "               "},
        {"password": "123456789012345"},
        {"reason": "    a   "},
        {"unknown": True},
    ],
)
def test_invalid_account_inputs(changes):
    with pytest.raises(ValidationError):
        AccountCreate.model_validate(payload(**changes))


def test_normalize_contact_and_roles():
    value = AccountCreate.model_validate(
        payload(
            username=" ABC.Name ",
            email=" A@Example.COM ",
            roles=["student", "student", "guardian"],
            display_name="  Em học sinh  ",
        )
    )
    assert value.username == "abc.name" and value.email == "a@example.com"
    assert value.roles == ["guardian", "student"] and value.display_name == "Em học sinh"


@pytest.mark.integration
@pytest.mark.parametrize("text_size", ["large", "compact"])
def test_create_search_filters_and_no_secret_exposure(manager, conn, text_size):
    client, _ = manager
    account = create(client, email=" Parent@Example.COM ", text_size=text_size)
    assert account["text_size"] == text_size
    user_id = UUID(account["id"])
    assert account["email"] == "parent@example.com"
    assert account["roles"] == ["student"] and account["must_change_password"]
    profile = (
        conn.execute(
            select(db.table("student_profiles")).where(
                db.table("student_profiles").c.student_id == user_id
            )
        )
        .mappings()
        .one()
    )
    assert (
        profile["current_grade"] == 4 and profile["accessibility_options"]["text_size"] == text_size
    )
    for query in (
        f"search={account['username']}",
        "search=PARENT@EXAMPLE.COM&grade=4&role=student&status=active",
    ):
        page = client.get("/api/v1/admin/accounts?" + query).json()
        assert page["total"] == 1 and page["items"][0]["id"] == account["id"]
    assert (
        client.get("/api/v1/admin/accounts?search=" + account["username"] + "&grade=3").json()[
            "total"
        ]
        == 0
    )
    detail = client.get(f"/api/v1/admin/accounts/{account['id']}").json()
    assert detail["history"][0]["action"] == "account_created"
    serialized = json.dumps(detail)
    for forbidden in (
        TEMP,
        ADMIN_PASSWORD,
        "password_hash",
        "token_hash",
        "csrf_hash",
        "actor_password",
    ):
        assert forbidden not in serialized
    assert client.get("/api/v1/admin/accounts?search=%25").json()["total"] == 0
    assert client.get("/api/v1/admin/accounts?search=_").json()["total"] == 0


@pytest.mark.integration
def test_duplicates_are_conflicts_with_no_partial_rows(manager, conn):
    client, _ = manager
    account = create(client, email="unique@example.com")
    users = db.table("users")
    count = conn.execute(select(func.count()).select_from(users)).scalar_one()
    for changes in ({"username": account["username"].upper()}, {"email": "UNIQUE@example.COM"}):
        assert client.post("/api/v1/admin/accounts", json=payload(**changes)).status_code == 409
    assert conn.execute(select(func.count()).select_from(users)).scalar_one() == count
    updated = create(client, roles=["teacher"], current_grade=None)
    assert updated["roles"] == ["teacher"] and updated["current_grade"] is None


@pytest.mark.integration
def test_forced_password_blocks_all_learning_and_admin_until_rotation(manager):
    client, _ = manager
    account = create(client, roles=["student", "admin"])
    result = login_as(client, account["username"], TEMP)
    assert result.json()["must_change_password"]
    token, csrf = client.cookies["viettree_session"], client.cookies["viettree_csrf"]
    for url in (
        "/api/v1/students/me/profile",
        "/api/v1/admin/accounts",
        "/api/v1/subjects",
        "/api/v1/students/me/thinking",
    ):
        result = client.get(url)
        assert (
            result.status_code == 403
            and result.json()["detail"]["code"] == "PASSWORD_CHANGE_REQUIRED"
        )
    assert client.get("/api/v1/auth/security").status_code == 200
    assert (
        client.post(
            "/api/v1/auth/password", json={"current_password": "wrong", "new_password": NEW}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/v1/auth/password", json={"current_password": TEMP, "new_password": TEMP}
        ).status_code
        == 422
    )
    result = client.post(
        "/api/v1/auth/password", json={"current_password": TEMP, "new_password": NEW}
    )
    assert result.status_code == 200
    assert client.cookies["viettree_session"] != token and client.cookies["viettree_csrf"] != csrf
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert not client.get("/api/v1/auth/me").json()["must_change_password"]
    assert client.get("/api/v1/admin/accounts").status_code == 200
    client.cookies.clear()
    client.cookies.set("viettree_session", token)
    assert client.get("/api/v1/auth/me").status_code == 401
    assert (
        client.post(
            "/api/v1/auth/login", json={"username": account["username"], "password": TEMP}
        ).status_code
        == 401
    )
    login_as(client, account["username"], NEW)


@pytest.mark.integration
def test_edit_preserves_profiles_history_and_stale_revision(manager, conn):
    client, _ = manager
    account = create(client, must_change_password=False)
    profiles = db.table("student_profiles")
    uid = UUID(account["id"])
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == uid)
        .values(
            learning_preferences={"keep": True},
            accessibility_options={
                "other": True,
                "text_size_by_device": {"phone": "compact", "tablet": "large"},
            },
        )
    )
    result = client.patch(
        f"/api/v1/admin/accounts/{uid}",
        json=edit_payload(account, display_name="Tên mới", current_grade=3, text_size="large"),
    )
    assert result.status_code == 200
    assert result.json()["account_revision"] == 2
    assert (
        client.patch(f"/api/v1/admin/accounts/{uid}", json=edit_payload(account)).status_code == 409
    )
    profile = conn.execute(select(profiles).where(profiles.c.student_id == uid)).mappings().one()
    assert profile["learning_preferences"] == {"keep": True} and profile[
        "accessibility_options"
    ] == {
        "other": True,
        "text_size": "large",
        "text_size_by_device": {"phone": "compact", "tablet": "large"},
    }
    updated = result.json()
    result = client.patch(
        f"/api/v1/admin/accounts/{uid}",
        json=edit_payload(updated, roles=["teacher"], current_grade=None),
    )
    assert result.status_code == 200 and result.json()["roles"] == ["teacher"]
    assert (
        conn.execute(
            select(profiles.c.current_grade).where(profiles.c.student_id == uid)
        ).scalar_one()
        == 3
    )
    updated = result.json()
    result = client.patch(
        f"/api/v1/admin/accounts/{uid}",
        json=edit_payload(updated, roles=["student"], current_grade=4),
    )
    assert result.status_code == 200
    assert conn.execute(
        select(profiles.c.learning_preferences).where(profiles.c.student_id == uid)
    ).scalar_one() == {"keep": True}


@pytest.mark.integration
def test_lock_unlock_role_change_and_reset_revoke_all(manager, conn):
    client, _ = manager
    account = create(client, must_change_password=False)
    sessions = db.table("auth_sessions")
    token = "student-existing-" + str(uuid4())
    conn.execute(
        sessions.insert().values(
            token_hash=digest(token),
            csrf_hash=digest("csrf"),
            user_id=UUID(account["id"]),
            expires_at=now() + timedelta(hours=1),
        )
    )
    result = client.patch(
        f"/api/v1/admin/accounts/{account['id']}", json=edit_payload(account, is_active=False)
    )
    assert result.status_code == 200
    assert conn.execute(
        select(sessions.c.revoked_at).where(sessions.c.token_hash == digest(token))
    ).scalar_one()
    result = client.patch(
        f"/api/v1/admin/accounts/{account['id']}",
        json=edit_payload(result.json(), is_active=True, roles=["student", "teacher"]),
    )
    assert result.status_code == 200
    reset = client.post(
        f"/api/v1/admin/accounts/{account['id']}/reset-password",
        json={
            "revision": result.json()["account_revision"],
            "new_password": NEW,
            "actor_password": ADMIN_PASSWORD,
            "reason": "Hỗ trợ học sinh quên mật khẩu",
        },
    )
    assert reset.status_code == 200 and reset.json()["must_change_password"]
    login_as(client, account["username"], NEW)
    assert client.get("/api/v1/students/me/profile").status_code == 403


@pytest.mark.integration
def test_self_protection_and_reauthentication(manager):
    client, user_id = manager
    own = client.get(f"/api/v1/admin/accounts/{user_id}").json()
    for changes in ({"is_active": False}, {"roles": ["teacher"]}):
        assert (
            client.patch(
                f"/api/v1/admin/accounts/{user_id}", json=edit_payload(own, **changes)
            ).status_code
            == 409
        )
    assert (
        client.post(
            f"/api/v1/admin/accounts/{user_id}/reset-password",
            json={
                "revision": own["account_revision"],
                "new_password": NEW,
                "actor_password": ADMIN_PASSWORD,
                "reason": "Kiểm thử tự đặt lại mật khẩu",
            },
        ).status_code
        == 409
    )
    assert (
        client.post("/api/v1/admin/accounts", json=payload(actor_password="wrong")).status_code
        == 403
    )
    client.headers["X-CSRF-Token"] = "bad"
    assert client.post("/api/v1/admin/accounts", json=payload()).status_code == 403


@pytest.mark.integration
def test_revoke_others_keeps_current_and_owner_only(logged_student, conn):
    client = logged_student
    from app.core.config import settings

    user_id = UUID(client.get("/api/v1/auth/me").json()["id"])
    sessions = db.table("auth_sessions")
    other = digest("other-" + str(uuid4()))
    foreign_id, _ = insert_user(conn)
    foreign = digest("foreign-" + str(uuid4()))
    for uid, token in ((user_id, other), (foreign_id, foreign)):
        conn.execute(
            sessions.insert().values(
                user_id=uid,
                token_hash=token,
                csrf_hash=digest("csrf"),
                expires_at=now() + timedelta(hours=1),
            )
        )
    current = client.cookies["viettree_session"]
    response = client.post(
        "/api/v1/auth/sessions/revoke-others",
        json={"current_password": settings().seed_student_password},
    )
    assert response.status_code == 200 and response.json()["revoked_sessions"] == 1
    assert (
        client.cookies["viettree_session"] == current
        and client.get("/api/v1/auth/me").status_code == 200
    )
    assert conn.execute(
        select(sessions.c.revoked_at).where(sessions.c.token_hash == other)
    ).scalar_one()
    assert (
        conn.execute(
            select(sessions.c.revoked_at).where(sessions.c.token_hash == foreign)
        ).scalar_one()
        is None
    )
    assert "token_hash" not in client.get("/api/v1/auth/security").text
    assert client.get("/api/v1/admin/accounts").status_code == 403
    assert client.post("/api/v1/admin/accounts", json=payload()).status_code == 403


@pytest.mark.integration
def test_rate_limit_and_errors_do_not_echo_passwords(manager):
    client, _ = manager
    for _ in range(10):
        result = client.post("/api/v1/admin/accounts", json=payload(actor_password="bad secret"))
        assert result.status_code == 403 and "bad secret" not in result.text
    result = client.post("/api/v1/admin/accounts", json=payload())
    assert result.status_code == 429 and result.headers["retry-after"] == "60"
    result = client.post(
        "/api/v1/auth/password",
        json={"current_password": "secret old", "new_password": "secret short"},
    )
    assert result.status_code == 422 and "secret" not in result.text


@pytest.mark.integration
def test_legacy_profile_edit_invalidates_account_revision(manager, conn):
    client, _ = manager
    account = create(client)
    response = client.patch(
        f"/api/v1/admin/students/{account['id']}",
        json={"display_name": "Tên từ hồ sơ", "current_grade": 3},
    )
    assert response.status_code == 200
    assert (
        client.patch(
            f"/api/v1/admin/accounts/{account['id']}", json=edit_payload(account)
        ).status_code
        == 409
    )


@pytest.mark.integration
def test_account_changes_keep_existing_learning_and_membership(manager, conn):
    client, admin_id = manager
    from tests.test_integration import start

    admin_name = conn.execute(
        select(db.table("users").c.username).where(db.table("users").c.id == admin_id)
    ).scalar_one()
    account = create(client, must_change_password=False)
    login_as(client, account["username"], TEMP)
    attempt_id, _, _ = start(client)
    user_id = UUID(account["id"])
    preserved = {}
    for name, key in (
        ("attempts", "student_id"),
        ("student_assignments", "student_id"),
        ("student_lesson_progress", "student_id"),
        ("student_memberships", "student_id"),
    ):
        table = db.table(name)
        preserved[name] = [
            dict(r) for r in conn.execute(select(table).where(table.c[key] == user_id)).mappings()
        ]
    assert preserved["attempts"] and preserved["student_assignments"]
    login_as(client, admin_name, ADMIN_PASSWORD)
    response = client.patch(
        f"/api/v1/admin/accounts/{account['id']}",
        json=edit_payload(account, current_grade=3, is_active=False),
    )
    assert response.status_code == 200
    result = client.post(
        f"/api/v1/admin/accounts/{account['id']}/reset-password",
        json={
            "revision": response.json()["account_revision"],
            "actor_password": ADMIN_PASSWORD,
            "new_password": NEW,
            "reason": "Hỗ trợ đổi mật khẩu tài khoản",
        },
    )
    assert result.status_code == 200
    for name, previous in preserved.items():
        table = db.table(name)
        assert [
            dict(r)
            for r in conn.execute(select(table).where(table.c.student_id == user_id)).mappings()
        ] == previous
    assert str(preserved["attempts"][0]["id"]) == attempt_id


@pytest.mark.integration
def test_privileged_session_summary_honors_shorter_deadline(manager, conn):
    client, uid = manager
    sessions = db.table("auth_sessions")
    expired = digest("expired-" + str(uuid4()))
    conn.execute(
        sessions.insert().values(
            user_id=uid,
            token_hash=expired,
            csrf_hash=digest("csrf"),
            created_at=now() - timedelta(days=1),
            expires_at=now() + timedelta(days=5),
        )
    )
    response = client.get("/api/v1/auth/security")
    assert response.status_code == 200 and response.json()["active_sessions"] == 1
