"""Real PostgreSQL coverage for discovery, private scores and live VIP gates."""

from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.core.security import now
from app.curriculum.supplements.applied.pack import seed
from app.db import db
from app.services.attempts import assign_self
from tests.test_concurrency import create_student

pytestmark = pytest.mark.integration
PATH = "/api/v1/students/me/practice-library"


def assessment(conn, grade=4, suffix="ribbon"):
    table = db.table("assessments")
    return conn.execute(
        select(table.c.id).where(
            table.c.code == f"VT{grade}-MATH-applied-2026-01-{suffix}-practice"
        )
    ).scalar_one()


def graded(conn, student_id, assessment_id, score, number=1, status="graded"):
    # The fixture deliberately isolates catalogue calculations from the grader.
    assignment = assign_self(conn, student_id, assessment_id)
    at = now() - timedelta(minutes=20 - number)
    conn.execute(
        db.table("attempts")
        .insert()
        .values(
            id=uuid4(),
            assignment_id=assignment["id"],
            student_id=student_id,
            assessment_id=assessment_id,
            attempt_no=number,
            status=status,
            started_at=at - timedelta(minutes=1),
            submitted_at=at if status != "in_progress" else None,
            graded_at=at if status == "graded" else None,
            total_score=score,
            max_score=10,
        )
    )


def test_discovery_scopes_grade_paginates_searches_without_accents_and_never_returns_keys(
    logged_student, conn
):
    seed(conn)
    response = logged_student.get(PATH)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["grade"] == 4 and data["page_size"] == 12
    assert len(data["items"]) == 12
    first_ids = {item["id"] for item in data["items"]}
    second = logged_student.get(PATH, params={"page": 2}).json()
    assert not first_ids & {item["id"] for item in second["items"]}
    for item in data["items"]:
        assert item["progress_status"] == "not_started"
        assert item["best_percent"] is None
        assert not {"grading", "explanation", "content", "student_id"} & item.keys()
    found = logged_student.get(
        PATH, params={"search": "dai ruy bang", "max_questions": 4, "subject_code": "MATH"}
    ).json()
    assert found["summary"]["total"] == 1
    assert found["items"][0]["id"] == str(assessment(conn))
    assert not found["items"][0]["locked"]
    assert logged_student.get(PATH, params={"search": "%"}).json()["summary"]["total"] == 0
    assert logged_student.get(PATH, params={"search": "_"}).json()["summary"]["total"] == 0
    assert logged_student.get(PATH, params={"search": "quả táo", "grade": 1}).json()["grade"] == 4
    empty = logged_student.get(PATH, params={"page": 10000}).json()
    assert empty["summary"]["total"] == data["summary"]["total"] and empty["items"] == []
    for invalid in (
        {"max_questions": 9},
        {"page": 0},
        {"search": "a" * 81},
        {"plan": "admin"},
        {"subject_code": "SQL"},
    ):
        assert logged_student.get(PATH, params=invalid).status_code == 422


def test_latest_finalized_score_drives_review_best_is_preserved_and_other_students_are_private(
    logged_student, conn
):
    seed(conn, [4])
    user_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    aid = assessment(conn)
    other = create_student(conn)
    graded(conn, other["id"], aid, 0)
    assert logged_student.get(PATH, params={"progress": "review"}).json()["summary"]["total"] == 0
    graded(conn, user_id, aid, 10)
    data = logged_student.get(PATH, params={"search": "dai ruy bang"}).json()["items"][0]
    assert data["progress_status"] == "mastered" and data["best_percent"] == 100
    graded(conn, user_id, aid, 7.5, 2)
    review = logged_student.get(PATH, params={"progress": "review"}).json()
    assert review["summary"] == {"total": 1, "review": 1, "mastered": 0, "not_started": 0}
    assert review["items"][0]["latest_percent"] == 75
    assert review["items"][0]["best_percent"] == 100
    assert review["items"][0]["graded_count"] == 2
    graded(conn, user_id, aid, 0, 3, "in_progress")
    assert (
        logged_student.get(PATH, params={"progress": "review"}).json()["items"][0]["latest_percent"]
        == 75
    )
    graded(conn, user_id, aid, 8, 4)
    assert logged_student.get(PATH, params={"progress": "review"}).json()["items"] == []
    reached = logged_student.get(PATH, params={"progress": "mastered"}).json()
    assert reached["summary"]["total"] == 1 and reached["items"][0]["latest_percent"] == 80


def test_membership_changes_are_immediate_and_vip_catalogue_does_not_grant_execution(
    logged_student, conn
):
    from tests.test_classrooms import grant

    seed(conn, [4])
    user_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    params = {"plan": "vip", "search": "hai luong cay bi mat", "max_questions": 6}
    free = logged_student.get(PATH, params=params)
    assert free.status_code == 200, free.text
    item = free.json()["items"][0]
    assert item["locked"] and item["minimum_plan_code"] == "vip"
    assert (
        logged_student.post(f"/api/v1/students/me/assessments/{item['id']}/assign-self").status_code
        == 403
    )
    grant(conn, user_id)
    assert not logged_student.get(PATH, params=params).json()["items"][0]["locked"]
    from app.schemas.memberships import MembershipRevokeInput
    from app.services.memberships import change_membership

    users = db.table("users")
    actor = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        actor,
        user_id,
        "revoke",
        MembershipRevokeInput(reason="Kiểm thử thu hồi quyền thư viện"),
        uuid4(),
    )
    assert logged_student.get(PATH, params=params).json()["items"][0]["locked"]
    assert free.headers["cache-control"] == "no-store"
    logged_student.cookies.clear()
    assert logged_student.get(PATH).status_code == 401
