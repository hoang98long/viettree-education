import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.db import connection, db
from app.fixtures.development import seed
from app.main import app


@pytest.fixture
def test_engine():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Cần TEST_DATABASE_URL trỏ tới PostgreSQL test riêng")
    engine = create_engine(url, hide_parameters=True)
    if engine.url.database == "viettree-education" or "test" not in engine.url.database.lower():
        raise RuntimeError("Integration test chỉ cho phép database test riêng")
    yield engine
    engine.dispose()


@pytest.fixture
def conn(test_engine):
    with test_engine.connect() as conn:
        outer = conn.begin()
        db.load(conn)
        seed(conn)
        yield conn
        outer.rollback()


@pytest.fixture
def client(conn, test_engine, monkeypatch):
    # Toàn bộ học tập rollback; rate limit riêng chỉ ghi database test.
    monkeypatch.setattr("app.core.security.engine", lambda: test_engine)

    def override():
        with conn.begin_nested():
            yield conn

    app.dependency_overrides[connection] = override
    host = "test-" + str(uuid4())
    # Account limit shared across IPs in production; isolate each test's namespace.
    from app.core import security

    throttle = security._throttle
    monkeypatch.setattr(
        security, "_throttle", lambda identity, maximum: throttle(host + ":" + identity, maximum)
    )
    with TestClient(app, client=(host, 12345)) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def logged_student(client, conn):
    from app.core.config import settings
    from app.core.security import hasher

    user_id, username = uuid4(), "test-" + str(uuid4())
    conn.execute(
        db.table("users")
        .insert()
        .values(
            id=user_id,
            username=username,
            display_name="Test Student",
            password_hash=hasher.hash(settings().seed_student_password),
        )
    )
    conn.execute(db.table("user_roles").insert().values(user_id=user_id, role="student"))
    conn.execute(db.table("student_profiles").insert().values(student_id=user_id, current_grade=4))

    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": settings().seed_student_password},
    )
    assert response.status_code == 200, response.text
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    return client
