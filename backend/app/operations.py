"""Chẩn đoán chỉ đọc và bảo trì auth; không thay đổi lịch sử học tập."""

import time
from datetime import timedelta
from functools import lru_cache
from threading import Lock

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import delete, func, or_, select, text

from app.core.config import ROOT, settings
from app.core.security import now
from app.db import SchemaNotReady, db


@lru_cache
def expected_heads():
    config = Config(str(ROOT / "backend/alembic.ini"))
    return sorted(ScriptDirectory.from_config(config).get_heads())


def current_heads(conn):
    if not conn.execute(text("SELECT to_regclass('public.alembic_version')")).scalar_one():
        return []
    return sorted(conn.execute(text("SELECT version_num FROM public.alembic_version")).scalars())


class Readiness:
    def __init__(self):
        self._validated_at = None
        self._lock = Lock()

    def check(self, conn):
        # Kết nối và revision luôn kiểm tra trực tiếp. Chỉ cache đối chiếu cấu trúc.
        conn.execute(text("SELECT 1"))
        if current_heads(conn) != expected_heads():
            raise SchemaNotReady("Migration chưa đúng head của release")
        with self._lock:
            if self._validated_at is None or time.monotonic() - self._validated_at >= 60:
                db.validate(conn)
                self._validated_at = time.monotonic()


readiness = Readiness()


def auth_candidates(conn, retention_days=30):
    if not 1 <= retention_days <= 365:
        raise ValueError("Retention phải từ 1 đến 365 ngày")
    cutoff = now() - timedelta(days=retention_days)
    sessions, limits = db.table("auth_sessions"), db.table("auth_login_limits")
    return (
        (sessions, or_(sessions.c.expires_at < cutoff, sessions.c.revoked_at < cutoff)),
        (limits, limits.c.window_start < cutoff),
    )


def cleanup_auth(conn, retention_days=30, apply=False):
    counts = {}
    for table, predicate in auth_candidates(conn, retention_days):
        if apply:
            # Predicate được kiểm tra lại trong DELETE: cửa sổ rate limit vừa cập nhật được giữ.
            counts[table.name] = conn.execute(delete(table).where(predicate)).rowcount
        else:
            counts[table.name] = conn.execute(
                select(func.count()).select_from(table).where(predicate)
            ).scalar_one()
    return {
        "mode": "apply" if apply else "dry_run",
        "retention_days": retention_days,
        "counts": counts,
    }


def system_report(conn):
    actual, expected = current_heads(conn), expected_heads()
    lessons, assessments, policies, versions, question_policies, items, questions = (
        db.table(name)
        for name in (
            "lessons",
            "assessments",
            "content_access_policies",
            "question_versions",
            "question_version_access_policies",
            "assessment_items",
            "questions",
        )
    )
    missing_lessons = conn.execute(
        select(func.count())
        .select_from(lessons)
        .where(
            lessons.c.status == "published",
            ~select(policies.c.id).where(policies.c.lesson_id == lessons.c.id).exists(),
        )
    ).scalar_one()
    missing_assessments = conn.execute(
        select(func.count())
        .select_from(assessments)
        .where(
            assessments.c.status == "published",
            ~select(policies.c.id).where(policies.c.assessment_id == assessments.c.id).exists(),
        )
    ).scalar_one()
    missing_questions = conn.execute(
        select(func.count())
        .select_from(versions)
        .where(
            versions.c.status == "published",
            ~select(question_policies.c.question_version_id)
            .where(question_policies.c.question_version_id == versions.c.id)
            .exists(),
        )
    ).scalar_one()
    invalid_assessments = conn.execute(
        select(func.count())
        .select_from(assessments)
        .where(
            assessments.c.status == "published",
            or_(
                ~select(items.c.id).where(items.c.assessment_id == assessments.c.id).exists(),
                select(items.c.id)
                .select_from(
                    items.join(versions, items.c.question_version_id == versions.c.id).join(
                        questions, versions.c.question_id == questions.c.id
                    )
                )
                .where(
                    items.c.assessment_id == assessments.c.id,
                    or_(
                        versions.c.status == "draft",
                        questions.c.grade != assessments.c.grade,
                        questions.c.subject_id != assessments.c.subject_id,
                    ),
                )
                .exists(),
            ),
        )
    ).scalar_one()
    features = db.table("membership_plan_features")
    guided_hints = bool(
        conn.execute(
            select(features.c.feature_code).where(
                features.c.plan_code == "vip", features.c.feature_code == "learning.guided_hints"
            )
        ).first()
    )
    checks = [
        {
            "code": "migrations",
            "label": "Migration đúng phiên bản",
            "ok": actual == expected,
            "count": None,
        },
        {
            "code": "lesson_policies",
            "label": "Bài học thiếu quyền Free/VIP",
            "ok": missing_lessons == 0,
            "count": missing_lessons,
        },
        {
            "code": "assessment_policies",
            "label": "Bài tập thiếu quyền Free/VIP",
            "ok": missing_assessments == 0,
            "count": missing_assessments,
        },
        {
            "code": "question_policies",
            "label": "Câu hỏi thiếu quyền Free/VIP",
            "ok": missing_questions == 0,
            "count": missing_questions,
        },
        {
            "code": "assessment_items",
            "label": "Đề rỗng, sai môn/lớp hoặc chứa câu nháp",
            "ok": invalid_assessments == 0,
            "count": invalid_assessments,
        },
        {
            "code": "guided_hints",
            "label": "Quyền gợi ý từng bước cho VIP",
            "ok": guided_hints,
            "count": None,
        },
    ]
    return {
        "status": "ok" if all(check["ok"] for check in checks) else "attention",
        "checked_at": now(),
        "environment": settings().app_env,
        "migrations": {"current": actual, "expected": expected},
        "session": {
            "hours": settings().session_hours,
            "remember_days": settings().remember_session_days,
        },
        "checks": checks,
        "cleanup": cleanup_auth(conn),
    }
