from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, BoundedSemaphore, Lock
from time import sleep
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import HTTPException, Request
from pydantic import ValidationError
from sqlalchemy import select

from app.api.routes.auth import login_guard
from app.core import security
from app.core.config import Settings
from app.db import Database, db
from app.fixtures.development import seed
from app.personalization.engine import rebuild_statistics
from app.schemas.auth import LoginInput
from app.services.attempts import assign_self, start_attempt, submit
from tests.test_concurrency import create_student


def test_production_worker_and_proxy_configuration(monkeypatch):
    from scripts import serve

    config = SimpleNamespace(
        server_workers=3, server_limit_concurrency=96, server_graceful_timeout=40
    )
    monkeypatch.setattr(serve, "settings", lambda: config)
    options = serve.server_options()
    assert options["workers"] == 3 and options["limit_concurrency"] == 96
    assert options["timeout_graceful_shutdown"] == 40
    assert options["forwarded_allow_ips"] == "172.30.40.2"
    assert options["proxy_headers"] is True


@pytest.mark.parametrize(
    "values",
    [
        {"server_workers": 0},
        {"server_workers": 9},
        {"server_limit_concurrency": 0},
        {"server_limit_concurrency": 2001},
        {"server_graceful_timeout": 0},
        {"server_graceful_timeout": 121},
        {"password_verify_concurrency": 0},
        {"password_verify_concurrency": 9},
        {"db_lock_timeout_ms": 0},
        {"db_lock_timeout_ms": 30001},
    ],
)
def test_worker_configuration_rejects_unbounded_values(values):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **values)


def test_password_memory_concurrency_is_bounded_and_slots_released(monkeypatch):
    monkeypatch.setattr(security, "password_slots", BoundedSemaphore(2))
    active = maximum = 0
    lock = Lock()

    def verify(_hash, _password):
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        sleep(0.01)
        with lock:
            active -= 1
        return True

    monkeypatch.setattr(security, "hasher", SimpleNamespace(verify=verify))
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert all(pool.map(lambda _: security.verify_password("hash", "password"), range(8)))
    assert maximum == 2 and active == 0
    assert security.verify_password("hash", "password")


def test_password_capacity_returns_retry_and_releases_on_failure(monkeypatch):
    slots = Mock()
    monkeypatch.setattr(security, "password_slots", slots)
    slots.acquire.return_value = False
    with pytest.raises(HTTPException) as failure:
        security.verify_password("hash", "password")
    assert failure.value.status_code == 503
    assert failure.value.headers["Retry-After"] == "5"
    slots.release.assert_not_called()
    slots.acquire.return_value = True
    monkeypatch.setattr(security, "hasher", SimpleNamespace(verify=Mock(side_effect=ValueError)))
    with pytest.raises(ValueError):
        security.verify_password("hash", "password")
    slots.release.assert_called_once()


def test_hash_and_verify_share_one_memory_slot(monkeypatch):
    monkeypatch.setattr(security, "password_slots", BoundedSemaphore(1))
    active = maximum = 0
    lock = Lock()

    def work(result):
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        sleep(0.01)
        with lock:
            active -= 1
        return result

    monkeypatch.setattr(
        security,
        "hasher",
        SimpleNamespace(
            hash=lambda _: work("encoded"),
            verify=lambda *_: work(True),
        ),
    )

    def operation(index):
        if index % 2:
            return security.verify_password("encoded", "password")
        return security.hash_password("password") == "encoded"

    with ThreadPoolExecutor(max_workers=12) as pool:
        assert all(pool.map(operation, range(12)))
    assert maximum == 1 and active == 0


def test_hash_failure_releases_memory_slot(monkeypatch):
    monkeypatch.setattr(security, "password_slots", BoundedSemaphore(1))
    monkeypatch.setattr(security, "hasher", SimpleNamespace(hash=Mock(side_effect=ValueError)))
    with pytest.raises(ValueError):
        security.hash_password("password")
    assert security.password_slots.acquire(blocking=False)
    security.password_slots.release()


@pytest.mark.integration
def test_first_login_guard_loads_metadata_with_one_pool_connection(test_engine, monkeypatch):
    # Fresh workers have no reflected tables. The guard must complete its own
    # rate-limit transaction before the request borrows a DB connection.
    cold_db = Database()
    monkeypatch.setattr(security, "db", cold_db)
    monkeypatch.setattr(security, "engine", lambda: test_engine)
    request = Request({"type": "http", "headers": [], "client": ("cold-" + uuid4().hex, 1234)})
    payload = LoginInput(username="cold-" + uuid4().hex, password="A test password!")
    assert login_guard(payload, request) is payload
    assert "auth_login_limits" in cold_db.metadata.tables
    assert test_engine.pool.checkedout() == 0


@pytest.mark.integration
def test_many_students_submit_and_full_repair_keep_identical_statistics(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        assessments = db.table("assessments")
        assessment_id = conn.execute(
            select(assessments.c.id).where(assessments.c.code == "VT4-MATH-numbers-practice")
        ).scalar_one()
        users = [create_student(conn) for _ in range(8)]
        attempt_ids = [
            start_attempt(conn, user["id"], assign_self(conn, user["id"], assessment_id)["id"])[
                "id"
            ]
            for user in users
        ]
    barrier = Barrier(9)

    def run(index):
        barrier.wait(timeout=15)
        with test_engine.begin() as conn:
            if index == 8:
                rebuild_statistics(conn)
            else:
                submit(conn, users[index], attempt_ids[index])

    with ThreadPoolExecutor(max_workers=9) as pool:
        list(pool.map(run, range(9)))
    with test_engine.begin() as conn:
        stats = db.table("question_statistics")
        daily = db.table("student_daily_statistics")

        def snapshot():
            question_rows = conn.execute(
                select(
                    stats.c.question_version_id,
                    stats.c.attempts_count,
                    stats.c.correct_count,
                    stats.c.incorrect_count,
                    stats.c.avg_response_time_ms,
                ).order_by(stats.c.question_version_id)
            ).all()
            daily_rows = conn.execute(
                select(
                    daily.c.student_id,
                    daily.c.stat_date,
                    daily.c.subject_id,
                    daily.c.questions_answered,
                    daily.c.correct_answers,
                    daily.c.assessments_completed,
                ).order_by(daily.c.student_id, daily.c.stat_date, daily.c.subject_id)
            ).all()
            return question_rows, daily_rows

        before = snapshot()
        rebuild_statistics(conn)
        assert before == snapshot()
        counts = (
            conn.execute(
                select(daily.c.assessments_completed).where(
                    daily.c.student_id.in_([user["id"] for user in users])
                )
            )
            .scalars()
            .all()
        )
        assert counts == [1] * 8


@pytest.mark.integration
def test_same_student_submits_disjoint_exercises_keep_daily_total(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        user = create_student(conn)
        assessments = db.table("assessments")
        rows = conn.execute(
            select(assessments.c.id, assessments.c.subject_id).where(
                assessments.c.code.in_(
                    ["VT4-MATH-numbers-practice", "VT4-MATH-operations-practice"]
                )
            )
        ).all()
        assert len(rows) == 2 and rows[0].subject_id == rows[1].subject_id
        ids = [
            start_attempt(conn, user["id"], assign_self(conn, user["id"], row.id)["id"])["id"]
            for row in rows
        ]
    barrier = Barrier(2)

    def run(attempt_id):
        barrier.wait(timeout=15)
        with test_engine.begin() as conn:
            submit(conn, user, attempt_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, ids))
    with test_engine.begin() as conn:
        daily = db.table("student_daily_statistics")
        query = select(daily.c.assessments_completed).where(daily.c.student_id == user["id"])
        assert conn.execute(query).scalar_one() == 2
        rebuild_statistics(conn)
        assert conn.execute(query).scalar_one() == 2
