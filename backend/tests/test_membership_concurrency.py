from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from app.db import db
from app.schemas import MembershipGrantInput
from app.seed import seed
from app.services.memberships import change_membership
from tests.test_concurrency import create_student

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("same_key", [True, False])
def test_concurrent_extensions_are_serialized_and_idempotent(test_engine, same_key):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        student_id = create_student(conn)["id"]
        users = db.table("users")
        admin_id = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
        payload = MembershipGrantInput(duration_days=30, reason="Concurrent membership test")
        initial = change_membership(conn, admin_id, student_id, "grant", payload, uuid4())
    keys = [uuid4(), uuid4()]
    if same_key:
        keys[1] = keys[0]
    barrier = Barrier(2)

    def extend(index):
        barrier.wait(timeout=10)
        with test_engine.begin() as conn:
            return change_membership(conn, admin_id, student_id, "extend", payload, keys[index])

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(extend, range(2)))
    if same_key:
        assert results[0] == results[1]
    with test_engine.connect() as conn:
        members, operations = db.table("student_memberships"), db.table("membership_operations")
        actual_end = conn.execute(
            select(members.c.ends_at).where(members.c.student_id == student_id)
        ).scalar_one()
        assert actual_end - datetime.fromisoformat(initial["ends_at"]) == timedelta(
            days=30 if same_key else 60
        )
        assert conn.execute(
            select(func.count())
            .select_from(operations)
            .where(operations.c.student_id == student_id)
        ).scalar_one() == (2 if same_key else 3)
