import ast
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.core.security import hasher
from app.curriculum.registry import EXPECTED, SUPPORTED_GRADES, get_pack, inventory
from app.curriculum.seeding import seed_grade_content, verify_seed
from app.db import db
from app.fixtures.learners import seed_demo_learners
from app.schemas.memberships import MembershipRevokeInput
from app.services.access import resolve_membership
from app.services.memberships import change_membership


@pytest.mark.parametrize("grade", SUPPORTED_GRADES)
def test_registered_pack_inventory_and_repeat_seed(conn, grade):
    expected_pack = get_pack(grade).expected
    assert inventory(grade) == expected_pack
    before = verify_seed(conn, grade)
    for subject, expected in expected_pack.items():
        assert all(before[subject][key] >= value for key, value in expected.items())
    seed_grade_content(conn, grade)
    assert verify_seed(conn, grade) == before
    pack = get_pack(grade)
    assert set(pack.sources) == set(EXPECTED)
    assert all(pack.topic_map[subject] for subject in EXPECTED)


def test_demo_accounts_all_grades_and_real_access(client, conn):
    rows = seed_demo_learners(conn)
    assert len(rows) == 20 and all(row["created"] for row in rows)
    users, profiles = db.table("users"), db.table("student_profiles")
    for grade in SUPPORTED_GRADES:
        for plan in ("free", "vip"):
            username = f"{plan}{grade}_01"
            user = conn.execute(select(users).where(users.c.username == username)).mappings().one()
            assert hasher.verify(user["password_hash"], settings().seed_student_password)
            assert (
                conn.execute(
                    select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
                ).scalar_one()
                == grade
            )
            membership = resolve_membership(conn, user["id"])
            assert membership["plan_code"] == plan
            if plan == "vip":
                assert (membership["ends_at"] - membership["starts_at"]).days == 90
            login = client.post(
                "/api/v1/auth/login",
                json={"username": username, "password": settings().seed_student_password},
            )
            assert login.status_code == 200
            assert client.get("/api/v1/students/me/profile").json()["current_grade"] == grade
            topics = client.get(f"/api/v1/topics?grade={grade}&subject_code=MATH").json()
            lessons = client.get(f"/api/v1/lessons?topic_id={topics[0]['id']}").json()
            free = next(row for row in lessons if row["minimum_plan_code"] == "free")
            assert len(client.get(f"/api/v1/lessons/{free['id']}").json()["content"]["hints"]) == (
                3 if plan == "vip" or grade == 4 else 1
            )
    assert all(not row["created"] for row in seed_demo_learners(conn))


def test_demo_repeat_preserves_password_grade_lock_and_vip_revoke(conn):
    seed_demo_learners(conn, [2])
    users, profiles = db.table("users"), db.table("student_profiles")
    user = conn.execute(select(users).where(users.c.username == "vip2_01")).mappings().one()
    administrator = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        administrator,
        user["id"],
        "revoke",
        MembershipRevokeInput(reason="Kiểm thử giữ nguyên VIP đã thu hồi"),
        uuid4(),
    )
    updated_hash = hasher.hash("Mat khau demo da doi 2026!")
    conn.execute(
        users.update()
        .where(users.c.id == user["id"])
        .values(password_hash=updated_hash, is_active=False)
    )
    conn.execute(
        profiles.update().where(profiles.c.student_id == user["id"]).values(current_grade=3)
    )
    result = next(row for row in seed_demo_learners(conn, [2, 2]) if row["username"] == "vip2_01")
    assert result == {"username": "vip2_01", "created": False, "grade": 3, "current_plan": "free"}
    row = conn.execute(select(users).where(users.c.id == user["id"])).mappings().one()
    assert row["password_hash"] == updated_hash and not row["is_active"]
    assert resolve_membership(conn, user["id"])["status"] == "revoked"


def test_demo_denies_production_without_writes(conn, monkeypatch):
    monkeypatch.setattr(
        "app.fixtures.learners.settings",
        lambda: SimpleNamespace(app_env="production", seed_student_password="unused"),
    )
    users = db.table("users")
    before = conn.execute(select(func.count()).select_from(users)).scalar_one()
    with pytest.raises(RuntimeError, match="development"):
        seed_demo_learners(conn)
    assert conn.execute(select(func.count()).select_from(users)).scalar_one() == before


def test_demo_refuses_role_collision(conn):
    identifier = uuid4()
    conn.execute(
        db.table("users")
        .insert()
        .values(
            id=identifier,
            username="free1_01",
            display_name="Không thay vai trò",
            password_hash="unused",
        )
    )
    conn.execute(db.table("user_roles").insert().values(user_id=identifier, role="admin"))
    with pytest.raises(RuntimeError, match="vai trò"):
        seed_demo_learners(conn, [1])


@pytest.mark.parametrize("grades", [[], [6], [0], [1, 6]])
def test_demo_rejects_unavailable_grades_before_database(grades):
    with pytest.raises(ValueError):
        seed_demo_learners(None, grades)


def test_content_packs_do_not_depend_on_runtime_or_fixtures():
    root = Path(__file__).resolve().parents[1] / "app/curriculum"
    for path in [
        root / "builders.py",
        root / "registry.py",
        *root.joinpath("grades").rglob("*.py"),
    ]:
        tree = ast.parse(path.read_text(encoding="utf8"))
        for node in ast.walk(tree):
            modules = (
                [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else []
            )
            assert not any(
                module.startswith(
                    ("app.api", "app.fixtures", "app.db", "app.services", "app.core.security")
                )
                for module in modules
            ), path
