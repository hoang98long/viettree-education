from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier, Event
from uuid import uuid4

import pytest
from fastapi import HTTPException, Request, Response
from sqlalchemy import func, select

from app.api.routes import auth as api
from app.api.routes.accounts import account_row
from app.core.security import digest, now
from app.db import db
from app.fixtures.development import seed
from app.schemas.accounts import AccountReset, AccountUpdate
from app.schemas.auth import LoginInput
from app.services import accounts
from tests.test_accounts import ADMIN_PASSWORD, NEW, TEMP, edit_payload, insert_user

pytestmark = pytest.mark.integration


def actor(conn, user_id):
    token = digest(str(uuid4()))
    conn.execute(
        db.table("auth_sessions")
        .insert()
        .values(
            token_hash=token,
            csrf_hash=digest(str(uuid4())),
            user_id=user_id,
            expires_at=now() + timedelta(hours=1),
        )
    )
    return {"id": user_id, "session_hash": token, "roles": ["admin"]}


def run_two(operations):
    barrier = Barrier(2)

    def run(operation):
        barrier.wait(timeout=10)
        try:
            operation()
            return 200
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        return list(pool.map(run, operations))


def test_concurrent_edits_one_revision_wins(test_engine, monkeypatch):
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        admin_id, _ = insert_user(conn)
        target_id, _ = insert_user(conn, roles=("student",))
        manager = actor(conn, admin_id)
        target = accounts.safe_account(conn, account_row(conn, target_id))

    def edit():
        with test_engine.begin() as conn:
            accounts.edit(
                conn,
                manager,
                target_id,
                AccountUpdate.model_validate(edit_payload(target, display_name="Sửa đồng thời")),
            )

    assert sorted(run_two([edit, edit])) == [200, 409]
    with test_engine.connect() as conn:
        assert (
            conn.execute(
                select(db.table("users").c.account_revision).where(
                    db.table("users").c.id == target_id
                )
            ).scalar_one()
            == 2
        )


def test_two_admins_cannot_disable_each_other_simultaneously(test_engine, monkeypatch):
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        ids = [insert_user(conn)[0] for _ in range(2)]
        actors = [actor(conn, uid) for uid in ids]
        rows = [
            accounts.safe_account(
                conn,
                conn.execute(select(db.table("users")).where(db.table("users").c.id == uid))
                .mappings()
                .one(),
            )
            for uid in ids
        ]

    def operation(index):
        def disable():
            with test_engine.begin() as conn:
                accounts.edit(
                    conn,
                    actors[index],
                    ids[1 - index],
                    AccountUpdate.model_validate(edit_payload(rows[1 - index], is_active=False)),
                )

        return disable

    assert sorted(run_two([operation(0), operation(1)])) == [200, 401]
    with test_engine.connect() as conn:
        users = db.table("users")
        assert (
            conn.execute(
                select(func.count())
                .select_from(users)
                .where(users.c.id.in_(ids), users.c.is_active.is_(True))
            ).scalar_one()
            == 1
        )


def test_old_password_login_racing_reset_cannot_leave_active_session(test_engine, monkeypatch):
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        admin_id, _ = insert_user(conn)
        target_id, username = insert_user(conn, roles=("student",), password=TEMP)
        manager = actor(conn, admin_id)
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/auth/login",
            "headers": [],
            "client": ("race-" + str(uuid4()), 1234),
        }
    )

    def login():
        payload = api.login_guard(LoginInput(username=username, password=TEMP), request)
        with test_engine.begin() as conn:
            api.login(request, Response(), payload=payload, conn=conn)

    def reset():
        with test_engine.begin() as conn:
            accounts.reset_password(
                conn,
                manager,
                target_id,
                AccountReset(
                    revision=1,
                    new_password=NEW,
                    actor_password=ADMIN_PASSWORD,
                    reason="Kiểm thử đặt lại đồng thời",
                ),
            )

    result = sorted(run_two([login, reset]))
    assert result in ([200, 200], [200, 401])
    with test_engine.connect() as conn:
        sessions = db.table("auth_sessions")
        assert (
            conn.execute(
                select(func.count())
                .select_from(sessions)
                .where(sessions.c.user_id == target_id, sessions.c.revoked_at.is_(None))
            ).scalar_one()
            == 0
        )


def test_profile_operation_can_audit_while_account_edit_waits(test_engine, monkeypatch):
    """Profile-first operations must not deadlock on the audit actor's user FK."""
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        admin_id, _ = insert_user(conn)
        target_id, _ = insert_user(conn, roles=("student",))
        manager = actor(conn, admin_id)
        target = accounts.safe_account(conn, account_row(conn, target_id))
    profile_locked, account_locked = Event(), Event()
    original_lock = accounts.admin_lock

    def traced_lock(*args, **kwargs):
        row = original_lock(*args, **kwargs)
        account_locked.set()
        return row

    monkeypatch.setattr(accounts, "admin_lock", traced_lock)

    def profile_operation():
        with test_engine.begin() as conn:
            profiles = db.table("student_profiles")
            conn.execute(
                select(profiles).where(profiles.c.student_id == target_id).with_for_update()
            ).one()
            profile_locked.set()
            assert account_locked.wait(15)
            conn.execute(
                db.table("audit_logs")
                .insert()
                .values(
                    actor_user_id=admin_id,
                    entity_type="account_concurrency_test",
                    entity_id=target_id,
                    action="profile_operation",
                    new_values={"completed": True},
                )
            )

    def edit():
        assert profile_locked.wait(15)
        with test_engine.begin() as conn:
            accounts.edit(
                conn,
                manager,
                target_id,
                AccountUpdate.model_validate(
                    edit_payload(target, display_name="Sửa không tranh chấp FK")
                ),
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        jobs = [pool.submit(profile_operation), pool.submit(edit)]
        for job in jobs:
            job.result(timeout=25)
