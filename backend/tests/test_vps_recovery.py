"""A real refused DB connection returns 503 and recovers without restarting API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select, text

from app.core.security import student_user
from app.db import Database, connection, db
from app.main import app
from tests.test_concurrency import create_student


@pytest.mark.integration
def test_readiness_warms_cold_api_metadata_before_first_request(test_engine, monkeypatch):
    cold_db = Database()
    monkeypatch.setattr("app.main.engine", lambda: test_engine)
    monkeypatch.setattr("app.main.db", cold_db)
    assert not cold_db.metadata.tables
    with TestClient(app) as client:
        response = client.get("/ready")
        assert response.status_code == 200
        assert "auth_login_limits" in cold_db.metadata.tables
        assert "student_profiles" in cold_db.metadata.tables
    assert test_engine.pool.checkedout() == 0


@pytest.mark.integration
def test_database_unavailable_then_recovered_does_not_leak_credentials(test_engine, monkeypatch):
    # Use a closed local port; never stop the PostgreSQL instance shared by
    # the development application or modify its connection settings.
    unavailable = create_engine(
        test_engine.url.set(port=1),
        hide_parameters=True,
        connect_args={"connect_timeout": 1},
    )
    try:
        monkeypatch.setattr("app.main.engine", lambda: unavailable)
        monkeypatch.setattr("app.core.security.engine", lambda: unavailable)
        with TestClient(app) as client:
            assert client.get("/health").status_code == 200
            not_ready = client.get("/ready")
            assert not_ready.status_code == 503
            failed_login = client.post(
                "/api/v1/auth/login",
                json={
                    "username": "recovery-test",
                    "password": "Private test password!",
                },
            )
            assert failed_login.status_code == 503
            assert failed_login.headers["cache-control"] == "no-store"
            body = failed_login.text + not_ready.text
            for private in ("Private test password!", "postgresql", "OperationalError"):
                assert private not in body
            if test_engine.url.password:
                assert test_engine.url.password not in body
            monkeypatch.setattr("app.main.engine", lambda: test_engine)
            assert client.get("/ready").status_code == 200
    finally:
        unavailable.dispose()


@pytest.mark.integration
def test_busy_student_row_times_out_safely_then_retry_creates_one_assignment(test_engine):
    limited = create_engine(
        test_engine.url,
        hide_parameters=True,
        connect_args={"options": "-c lock_timeout=1000 -c statement_timeout=5000"},
    )
    with test_engine.begin() as conn:
        db.load(conn)
        user = create_student(conn)
        assessments = db.table("assessments")
        assessment_id = conn.execute(
            select(assessments.c.id).where(assessments.c.code == "VT4-MATH-numbers-practice")
        ).scalar_one()

    def transaction():
        with limited.begin() as conn:
            yield conn

    app.dependency_overrides[connection] = transaction
    app.dependency_overrides[student_user] = lambda: user
    try:
        with TestClient(app) as client:
            path = f"/api/v1/students/me/assessments/{assessment_id}/assign-self"
            with test_engine.begin() as blocker:
                blocker.execute(
                    select(db.table("student_profiles"))
                    .where(db.table("student_profiles").c.student_id == user["id"])
                    .with_for_update()
                )
                response = client.post(path)
                assert response.status_code == 503
                assert "lock_timeout" not in response.text
            assert client.post(path).status_code == 200
            assert client.post(path).status_code == 200
        with test_engine.connect() as conn:
            assignments = db.table("student_assignments")
            assert (
                conn.execute(
                    select(func.count())
                    .select_from(assignments)
                    .where(
                        assignments.c.student_id == user["id"],
                        assignments.c.assessment_id == assessment_id,
                    )
                ).scalar_one()
                == 1
            )
        with limited.connect() as conn:
            assert conn.execute(text("SHOW lock_timeout")).scalar_one() == "1s"
    finally:
        app.dependency_overrides.clear()
        limited.dispose()


@pytest.mark.integration
def test_dashboard_is_read_only_and_does_not_wait_for_student_write(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        user = create_student(conn)
        user.update(
            conn.execute(select(db.table("users")).where(db.table("users").c.id == user["id"]))
            .mappings()
            .one()
        )

    def read_transaction():
        with test_engine.begin() as conn:
            conn.execute(text("SET TRANSACTION READ ONLY"))
            conn.execute(text("SET LOCAL lock_timeout = '500ms'"))
            yield conn

    app.dependency_overrides[connection] = read_transaction
    app.dependency_overrides[student_user] = lambda: user
    try:
        with test_engine.begin() as blocker:
            profiles = db.table("student_profiles")
            blocker.execute(
                select(profiles).where(profiles.c.student_id == user["id"]).with_for_update()
            )
            with TestClient(app) as client:
                response = client.get("/api/v1/students/me/dashboard")
                assert response.status_code == 200, response.text
                assert 1 <= len(response.json()["recommendations"]) <= 5
        with test_engine.connect() as conn:
            rec = db.table("student_recommendations")
            assert (
                conn.execute(
                    select(func.count()).select_from(rec).where(rec.c.student_id == user["id"])
                ).scalar_one()
                == 0
            )
    finally:
        app.dependency_overrides.clear()
