"""Observe PostgreSQL from another connection before ASGI sends a success response."""

from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import hasher
from app.db import connection, db
from app.fixtures.development import seed
from app.main import app
from tests.test_concurrency import create_student


def test_every_database_dependency_finishes_before_response():
    checked = 0

    def check(node):
        nonlocal checked
        if node.call is connection:
            assert node.scope == "function"
            checked += 1
        for dependency in node.dependencies:
            check(dependency)

    def check_route(route):
        if isinstance(route, APIRoute):
            check(route.dependant)
        nested = getattr(route, "original_router", None)
        if nested is not None:
            for child in nested.routes:
                check_route(child)

    for route in app.routes:
        check_route(route)
    assert checked >= 100


@pytest.mark.integration
@pytest.mark.parametrize(
    "commit_fails", [False, True], ids=["commit-before-response", "rollback-before-response"]
)
def test_login_session_committed_before_success_response(test_engine, monkeypatch, commit_fails):
    password = "Regression session password 2026!"
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        user = create_student(conn)
        users = db.table("users")
        conn.execute(
            users.update()
            .where(users.c.id == user["id"])
            .values(password_hash=hasher.hash(password))
        )
        username = conn.execute(
            select(users.c.username).where(users.c.id == user["id"])
        ).scalar_one()
    monkeypatch.setattr("app.db.engine", lambda: test_engine)
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)
    observed = []

    if commit_fails:

        def failed_transaction():
            with test_engine.begin() as conn:
                yield conn
                raise SQLAlchemyError("Simulated commit failure for regression test")

        app.dependency_overrides[connection] = failed_transaction

    async def observe(scope, receive, send):
        async def check_response(message):
            if (
                scope.get("path") == "/api/v1/auth/login"
                and message["type"] == "http.response.start"
                and message["status"] == 200
            ):
                sessions = db.table("auth_sessions")
                with test_engine.connect() as conn:
                    observed.append(
                        conn.execute(
                            select(func.count())
                            .select_from(sessions)
                            .where(sessions.c.user_id == user["id"])
                        ).scalar_one()
                    )
            await send(message)

        await app(scope, receive, check_response)

    try:
        with TestClient(observe, client=("transaction-" + uuid4().hex, 12345)) as client:
            response = client.post(
                "/api/v1/auth/login", json={"username": username, "password": password}
            )
            if commit_fails:
                assert response.status_code == 503
                assert observed == []
                assert "Simulated" not in response.text
                sessions = db.table("auth_sessions")
                with test_engine.connect() as conn:
                    assert (
                        conn.execute(
                            select(func.count())
                            .select_from(sessions)
                            .where(sessions.c.user_id == user["id"])
                        ).scalar_one()
                        == 0
                    )
            else:
                assert response.status_code == 200
                assert observed == [1], "Login reported success before the session was committed"
                assert client.get("/api/v1/auth/me").status_code == 200
    finally:
        app.dependency_overrides.clear()
