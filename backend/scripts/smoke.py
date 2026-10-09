"""Smoke PostgreSQL thật, mặc định rollback để giữ lịch sử demo sạch."""

import argparse
import logging
import sys
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.config import settings
from app.db import connection, db, engine
from app.main import app


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--persist", action="store_true", help="Ghi lịch sử thật; mặc định rollback"
    )
    args = parser.parse_args()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    with engine().connect() as conn:
        transaction = conn.begin()
        db.load(conn)

        def override():
            with conn.begin_nested():
                yield conn

        app.dependency_overrides[connection] = override
        try:
            with TestClient(app, client=("smoke-" + str(uuid4()), 8001)) as client:
                for username, password in [
                    ("admin", settings().seed_admin_password),
                    ("longnh", settings().seed_student_password),
                ]:
                    response = client.post(
                        "/api/v1/auth/login", json={"username": username, "password": password}
                    )
                    assert response.status_code == 200, f"login {username}: {response.status_code}"
                    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
                    if username == "admin":
                        assert client.get("/api/v1/admin/statistics").status_code == 200
                        assert client.post("/api/v1/auth/logout").status_code == 200
                subjects = client.get("/api/v1/subjects?grade=4").json()
                assert all(
                    code in [s["code"] for s in subjects]
                    for code in ("MATH", "VIETNAMESE", "ENGLISH")
                )
                assessment = client.get("/api/v1/assessments?grade=4&subject_code=MATH").json()[0]
                assignment = client.post(
                    f"/api/v1/students/me/assessments/{assessment['id']}/assign-self"
                ).json()
                response = client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]})
                assert response.status_code == 200, response.text
                attempt_id = response.json()["id"]
                public = client.get(f"/api/v1/attempts/{attempt_id}")
                assert "grading" not in public.text and "explanation" not in public.text
                for item in public.json()["items"]:
                    versions = db.table("question_versions")
                    question = (
                        conn.execute(
                            select(versions).where(versions.c.id == item["question_version_id"])
                        )
                        .mappings()
                        .one()
                    )
                    key, kind = question["grading"], question["question_type"]
                    answer = (
                        {"option_id": key["correct_option_id"]}
                        if kind == "single_choice"
                        else (
                            {"option_ids": key["correct_option_ids"]}
                            if kind == "multiple_choice"
                            else (
                                {"ordered_ids": key["ordered_ids"]}
                                if kind == "ordering"
                                else {"text": key["accepted_answers"][0]}
                            )
                        )
                    )
                    assert (
                        client.put(
                            f"/api/v1/attempts/{attempt_id}/answers/{item['id']}",
                            json={"answer": answer},
                        ).status_code
                        == 200
                    )
                submitted = client.post(f"/api/v1/attempts/{attempt_id}/submit")
                assert submitted.status_code == 200, submitted.text
                assert submitted.json()["total_score"] == submitted.json()["max_score"]
                assert (
                    client.post(f"/api/v1/attempts/{attempt_id}/submit").json() == submitted.json()
                )
                assert client.get(f"/api/v1/attempts/{attempt_id}/result").status_code == 200
                assert client.get("/api/v1/students/me/history").json()
                assert client.get("/api/v1/students/me/skills").json()
                assert client.get("/api/v1/students/me/dashboard").status_code == 200
                assert client.post("/api/v1/auth/logout").status_code == 200
                assert (
                    client.post(
                        "/api/v1/auth/login",
                        json={"username": "admin", "password": settings().seed_admin_password},
                    ).status_code
                    == 200
                )
                assert client.get("/api/v1/admin/statistics").json()["attempts"] >= 1
            if args.persist:
                transaction.commit()
            else:
                transaction.rollback()
            print(
                "SMOKE PASS: admin + longnh → 3 môn → làm Toán → chấm → nộp lặp → kết quả → lịch sử → mastery → dashboard → thống kê."
            )
            print(
                "Lịch sử: "
                + ("đã ghi database" if args.persist else "rollback, giữ tài khoản demo sạch")
            )
        finally:
            app.dependency_overrides.clear()
            if transaction.is_active:
                transaction.rollback()


if __name__ == "__main__":
    main()
