from uuid import uuid4

import pytest
from sqlalchemy import func, select, text

from app.core.config import settings
from app.core.security import now
from app.db import db
from app.operations import launch_report


@pytest.mark.integration
def test_launch_detects_unrotated_demo_all_grades_and_legacy_admin_without_writing(
    conn, monkeypatch
):
    users, roles = db.table("users"), db.table("user_roles")
    # This test's transaction rolls back every change, including legacy fixtures.
    conn.execute(users.update().values(is_active=False))
    administrator = uuid4()
    conn.execute(
        users.insert().values(
            id=administrator,
            username="launch-" + uuid4().hex,
            display_name="Launch review",
            password_hash="not-a-login-fixture",
            is_active=True,
        )
    )
    conn.execute(roles.insert().values(user_id=administrator, role="admin"))
    for grade in (1, 2, 3, 4, 5):
        username = f"vip{grade}_02"
        identifier = conn.execute(select(users.c.id).where(users.c.username == username)).scalar()
        if identifier:
            conn.execute(
                users.update()
                .where(users.c.id == identifier)
                .values(is_active=True, password_changed_at=None)
            )
        else:
            conn.execute(
                users.insert().values(username=username, display_name="Demo", is_active=True)
            )
    monkeypatch.setattr(settings(), "app_env", "production")
    before = conn.execute(select(func.count()).select_from(users)).scalar_one()
    # The diagnostic must also run with a read-only transaction in real usage;
    # here verify it leaves the account state intact across repeated calls.
    report = launch_report(conn)
    checks = {item["code"]: item for item in report["checks"]}
    assert checks["review_demo_accounts"]["count"] == 5
    assert not checks["ready_admin"]["ok"]
    assert not checks["runtime_db_role"][
        "ok"
    ]  # PostgreSQL test superuser is deliberately rejected.
    assert report["status"] == "attention"
    conn.execute(users.update().values(password_changed_at=now()))
    approved = {item["code"]: item for item in launch_report(conn)["checks"]}
    assert approved["review_demo_accounts"]["ok"]
    assert approved["ready_admin"]["ok"]
    assert conn.execute(select(func.count()).select_from(users)).scalar_one() == before


@pytest.mark.integration
def test_launch_diagnostic_is_read_only(test_engine):
    with test_engine.begin() as conn:
        conn.execute(text("SET TRANSACTION READ ONLY"))
        db.load(conn)
        assert launch_report(conn)["status"] in ("ok", "attention")
