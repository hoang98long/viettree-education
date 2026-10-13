from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from threading import Barrier
from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy import func, select

from app.db import db
from app.fixtures.development import seed
from app.schemas.memberships import MembershipGrantInput, MembershipRevokeInput
from app.services.memberships import change_membership
from tests.test_concurrency import create_student

pytestmark = pytest.mark.integration


def setup(conn):
    db.load(conn)
    seed(conn)
    student = create_student(conn)["id"]
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    return student, admin


def test_concurrent_grants_never_add_two_periods(test_engine):
    with test_engine.begin() as conn:
        student, admin = setup(conn)
    barrier = Barrier(2)
    payload = MembershipGrantInput(duration_days=30, reason="Concurrent grant verification")

    def run(_):
        barrier.wait(timeout=10)
        try:
            with test_engine.begin() as conn:
                return change_membership(conn, admin, student, "grant", payload, uuid4())
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, range(2)))
    assert sum(isinstance(r, dict) for r in results) == 1 and 409 in results
    result = next(r for r in results if isinstance(r, dict))
    assert datetime.fromisoformat(result["ends_at"]) - datetime.fromisoformat(
        result["starts_at"]
    ) == timedelta(days=30)
    with test_engine.connect() as conn:
        table = db.table("membership_operations")
        assert (
            conn.execute(
                select(func.count()).select_from(table).where(table.c.student_id == student)
            ).scalar_one()
            == 1
        )


def test_revocation_wins_over_concurrent_extension(test_engine):
    payload = MembershipGrantInput(duration_days=30, reason="Concurrent extension verification")
    with test_engine.begin() as conn:
        student, admin = setup(conn)
        change_membership(conn, admin, student, "grant", payload, uuid4())
    barrier = Barrier(2)

    def run(operation):
        barrier.wait(timeout=10)
        try:
            with test_engine.begin() as conn:
                return change_membership(
                    conn,
                    admin,
                    student,
                    operation,
                    MembershipRevokeInput(reason="Concurrent revocation verification")
                    if operation == "revoke"
                    else payload,
                    uuid4(),
                )
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, ["extend", "revoke"]))
    assert isinstance(results[1], dict) and results[1]["status"] == "revoked"
    assert isinstance(results[0], dict) or results[0] == 409
    with test_engine.connect() as conn:
        members = db.table("student_memberships")
        assert (
            conn.execute(
                select(members.c.status).where(members.c.student_id == student)
            ).scalar_one()
            == "revoked"
        )
