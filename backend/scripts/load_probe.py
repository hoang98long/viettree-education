"""Real HTTP exercise workload against a dedicated test DB, never a production DB."""

import argparse
import json
import os
import platform
import secrets
import ssl
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean
from uuid import uuid4

import httpx
from sqlalchemy import func, select

from app.core.security import hasher
from app.db import db, engine
from app.schemas.memberships import MembershipGrantInput
from app.services.memberships import change_membership


def percentile(values, fraction):
    values = sorted(values)
    return (
        round(values[min(len(values) - 1, int((len(values) - 1) * fraction))], 2)
        if values
        else None
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8001")
    parser.add_argument(
        "--readiness-base-url", help="Private API URL when /ready is hidden by the HTTPS proxy"
    )
    parser.add_argument(
        "--ca-bundle",
        type=Path,
        help="Trusted CA file for local HTTPS; never disables certificate verification",
    )
    parser.add_argument("--levels", type=int, nargs="+", default=[10, 25, 50])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parallel-login", action="store_true")
    parser.add_argument("--answer-all", action="store_true")
    args = parser.parse_args()
    if engine().url.database == "viettree-education" or "test" not in engine().url.database.lower():
        raise SystemExit("Chỉ chạy load probe trên database test riêng")
    readiness_base = args.readiness_base_url or args.base_url
    for address in (args.base_url, readiness_base):
        url = httpx.URL(address)
        if (
            url.host not in {"127.0.0.1", "localhost", "backend"}
            or url.scheme not in {"http", "https"}
            or url.username
            or url.password
        ):
            raise SystemExit("Probe chỉ gọi backend/proxy local trong môi trường test/staging")
    verification = ssl.create_default_context(cafile=args.ca_bundle) if args.ca_bundle else True
    if not args.levels or min(args.levels) < 1 or max(args.levels) > 100:
        raise SystemExit("Mỗi mức phải từ 1 đến 100")
    password = secrets.token_urlsafe(32)
    password_hash = hasher.hash(password)
    learners = []
    with engine().begin() as conn:
        db.load(conn)
        users, roles, profiles, assessments, policies = (
            db.table(name)
            for name in (
                "users",
                "user_roles",
                "student_profiles",
                "assessments",
                "content_access_policies",
            )
        )
        admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
        for index in range(max(args.levels)):
            identifier, username = uuid4(), "load-" + uuid4().hex
            grade = index % 5 + 1
            plan = "vip" if (index // 5) % 2 else "free"
            conn.execute(
                users.insert().values(
                    id=identifier,
                    username=username,
                    display_name="Load test",
                    password_hash=password_hash,
                )
            )
            conn.execute(roles.insert().values(user_id=identifier, role="student"))
            conn.execute(profiles.insert().values(student_id=identifier, current_grade=grade))
            if plan == "vip":
                change_membership(
                    conn,
                    admin,
                    identifier,
                    "grant",
                    MembershipGrantInput(duration_days=30, reason="Dedicated test load probe"),
                    uuid4(),
                )
            assessment = (
                conn.execute(
                    select(assessments.c.id, assessments.c.topic_id)
                    .join(policies, policies.c.assessment_id == assessments.c.id)
                    .where(
                        assessments.c.code.like(f"VT{grade}-MATH-%"),
                        assessments.c.status == "published",
                        policies.c.minimum_plan_code == plan,
                    )
                    .order_by(assessments.c.code)
                )
                .mappings()
                .first()
            )
            if not assessment:
                raise RuntimeError("Thiếu nội dung test cho một khối/gói")
            learners.append(
                {
                    "id": identifier,
                    "username": username,
                    "grade": grade,
                    "plan": plan,
                    "assessment": str(assessment["id"]),
                    "topic": str(assessment["topic_id"]),
                }
            )
    clients = []
    report = {
        "environment": f"local {httpx.URL(args.base_url).scheme.upper()} / real PostgreSQL / synthetic learners",
        "transport": {
            "workload_scheme": httpx.URL(args.base_url).scheme,
            "private_readiness": readiness_base != args.base_url,
            "certificate_verification": True,
            "custom_ca": bool(args.ca_bundle),
        },
        "host": {"os": platform.system(), "logical_cpus": os.cpu_count()},
        "learners": len(learners),
        "plans": dict(Counter(row["plan"] for row in learners)),
        "answer_all": args.answer_all,
        "levels": [],
    }
    # Match production startup order: private /ready must succeed before Caddy
    # exposes the application. Include cold-start warm-up separately from load.
    ready_started = time.perf_counter()
    with httpx.Client(base_url=readiness_base, timeout=60, verify=verification) as readiness_client:
        readiness_response = readiness_client.get("/ready")
        readiness_response.raise_for_status()
    report["readiness"] = {
        "status": readiness_response.status_code,
        "seconds": round(time.perf_counter() - ready_started, 2),
    }
    records = []
    errors = []

    def call(client, method, path, **kwargs):
        started = time.perf_counter()
        try:
            response = client.request(method, path, **kwargs)
            records.append(
                (path.split("/")[1], (time.perf_counter() - started) * 1000, response.status_code)
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            errors.append(type(error).__name__)
            raise

    try:
        for learner in learners:
            client = httpx.Client(
                base_url=args.base_url + "/api/v1", timeout=45, verify=verification
            )
            clients.append(client)

        def signin(index):
            learner, client = learners[index], clients[index]
            data = call(
                client,
                "POST",
                "/auth/login",
                json={"username": learner["username"], "password": password},
            )
            if data["id"] != str(learner["id"]):
                raise RuntimeError("API không nối đúng database test")
            client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]

        login_started = time.perf_counter()
        with ThreadPoolExecutor(max_workers=len(learners) if args.parallel_login else 1) as pool:
            authenticated = list(pool.map(lambda i: run_safely(signin, i), range(len(learners))))
        report["authentication"] = {
            "parallel": args.parallel_login,
            "seconds": round(time.perf_counter() - login_started, 2),
            "successes": sum(authenticated),
            "p95_ms": percentile([r[1] for r in records], 0.95),
            "status_counts": dict(Counter(r[2] for r in records)),
            "errors": dict(Counter(errors)),
        }
        print(json.dumps(report["authentication"]))
        if not all(authenticated):
            raise RuntimeError("Đăng nhập test chưa thành công cho toàn bộ học sinh")
        # Authentication preparation is intentionally outside measured learning requests.
        for level in args.levels:
            records.clear()
            errors.clear()

            def journey(index):
                learner, client = learners[index], clients[index]
                call(client, "GET", f"/subjects?grade={learner['grade']}")
                call(client, "GET", f"/lessons?topic_id={learner['topic']}")
                call(client, "GET", "/students/me/dashboard")
                assignment = call(
                    client, "POST", f"/students/me/assessments/{learner['assessment']}/assign-self"
                )
                start = call(client, "POST", "/attempts", json={"assignment_id": assignment["id"]})
                path = f"/attempts/{start['id']}"
                data = call(client, "GET", path)
                selected_items = data["items"] if args.answer_all else data["items"][:2]
                for item in selected_items:
                    kind = item["question_type"]
                    answer = (
                        {"option_id": item["content"]["options"][0]["id"]}
                        if kind == "single_choice"
                        else {"text": "1"}
                        if kind == "fill_blank"
                        else {
                            "ordered_ids" if kind == "ordering" else "option_ids": [
                                o["id"] for o in item["content"]["options"]
                            ]
                        }
                    )
                    call(client, "PUT", path + "/answers/" + item["id"], json={"answer": answer})
                dashboard = call(client, "GET", "/students/me/dashboard")
                if not any(
                    item["kind"] == "practice" and item["id"] == start["id"]
                    for item in dashboard.get("resume_items", [])
                ):
                    raise RuntimeError("Học tiếp không trả đúng lượt đang làm của học sinh test")
                submitted = call(client, "POST", path + "/submit")
                repeated = call(client, "POST", path + "/submit")
                if submitted != repeated:
                    raise RuntimeError("Nộp lặp không trả cùng kết quả")
                resumed = call(client, "GET", path + "/result")
                if resumed["answered_count"] != len(selected_items):
                    raise RuntimeError("Sai số câu trả lời đã lưu")

            started = time.perf_counter()
            with ThreadPoolExecutor(max_workers=level) as pool:
                outcomes = list(pool.map(lambda i: run_safely(journey, i), range(level)))
            elapsed = time.perf_counter() - started
            durations = [row[1] for row in records]
            report["levels"].append(
                {
                    "concurrent_learners": level,
                    "seconds": round(elapsed, 2),
                    "requests": len(records),
                    "requests_per_second": round(len(records) / elapsed, 2),
                    "mean_ms": round(mean(durations), 2) if durations else None,
                    "p50_ms": percentile(durations, 0.5),
                    "p95_ms": percentile(durations, 0.95),
                    "p99_ms": percentile(durations, 0.99),
                    "max_ms": round(max(durations), 2) if durations else None,
                    "status_counts": dict(Counter(row[2] for row in records)),
                    "journeys_completed": sum(outcomes),
                    "errors": dict(Counter(errors)),
                }
            )
            print(json.dumps(report["levels"][-1]))
        with engine().connect() as conn:
            attempts, answers, stats, daily = (
                db.table(name)
                for name in (
                    "attempts",
                    "attempt_answers",
                    "question_statistics",
                    "student_daily_statistics",
                )
            )
            expected = conn.execute(
                select(
                    answers.c.question_version_id,
                    func.count(),
                    func.count().filter(answers.c.is_correct.is_(True)),
                    func.count().filter(answers.c.is_correct.is_(False)),
                )
                .select_from(answers.join(attempts, attempts.c.id == answers.c.attempt_id))
                .where(attempts.c.status == "graded")
                .group_by(answers.c.question_version_id)
            ).all()
            actual = {
                row.question_version_id: tuple(row)[1:]
                for row in conn.execute(
                    select(
                        stats.c.question_version_id,
                        stats.c.attempts_count,
                        stats.c.correct_count,
                        stats.c.incorrect_count,
                    )
                )
            }
            question_mismatches = sum(actual.get(row[0]) != tuple(row)[1:] for row in expected)
            ids = [row["id"] for row in learners]
            graded_count = conn.execute(
                select(func.count())
                .select_from(attempts)
                .where(attempts.c.student_id.in_(ids), attempts.c.status == "graded")
            ).scalar_one()
            daily_count = conn.execute(
                select(func.coalesce(func.sum(daily.c.assessments_completed), 0)).where(
                    daily.c.student_id.in_(ids)
                )
            ).scalar_one()
            report["consistency"] = {
                "question_statistic_mismatches": question_mismatches,
                "graded_attempts": graded_count,
                "daily_assessments_completed": daily_count,
                "expected_attempts": sum(args.levels),
            }
            if (
                question_mismatches
                or graded_count != sum(args.levels)
                or daily_count != graded_count
            ):
                raise RuntimeError("Thống kê sau tải không khớp lịch sử bài làm")
            print(json.dumps(report["consistency"]))
    finally:
        for client in clients:
            client.close()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    if any(row["journeys_completed"] != row["concurrent_learners"] for row in report["levels"]):
        raise SystemExit(1)


def run_safely(journey, index):
    try:
        journey(index)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
