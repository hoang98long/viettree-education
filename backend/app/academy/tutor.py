import time
from threading import Lock

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.academy.learning import allowed_lesson, event
from app.academy.safety import moderation_reason
from app.core.config import settings
from app.core.security import _throttle, digest, now
from app.db import db
from app.services.access import resolve_membership

POLICY = "ai-academy-v1"
_circuit = {"failures": 0, "until": 0.0}
_lock = Lock()


def flags(conn):
    table = db.table("ai_feature_flags")
    return {r.code: r.enabled for r in conn.execute(select(table))}


def consent(conn, student_id):
    consents, links = (db.table(n) for n in ("privacy_consents", "guardian_students"))
    # Latest consent across verified guardians/admin-authorized school records; revocation wins.
    row = (
        conn.execute(
            select(consents)
            .where(
                consents.c.student_id == student_id,
                consents.c.purpose_code == "ai_academy_provider",
                consents.c.policy_version == POLICY,
            )
            .order_by(consents.c.recorded_at.desc(), consents.c.id.desc())
            .limit(1)
        )
        .mappings()
        .first()
    )
    if not row or not row["consent_given"] or (row["expires_at"] and row["expires_at"] <= now()):
        return False
    return row["guardian_user_id"] is None or bool(
        conn.execute(
            select(links.c.student_id).where(
                links.c.student_id == student_id,
                links.c.guardian_user_id == row["guardian_user_id"],
                links.c.verified_at.is_not(None),
            )
        ).first()
    )


def reserve_quota(conn, student_id):
    usage = db.table("ai_usage_windows")
    profiles = db.table("student_profiles")
    profile = conn.execute(
        select(profiles.c.school_id).where(profiles.c.student_id == student_id)
    ).scalar()
    scopes = [("student:" + str(student_id), 20), ("school:" + str(profile or "deployment"), 2000)]
    memberships, classes = db.table("class_enrollments"), db.table("classes")
    for class_id in conn.execute(
        select(classes.c.id)
        .join(memberships)
        .where(
            memberships.c.student_id == student_id,
            memberships.c.left_at.is_(None),
            classes.c.is_active.is_(True),
        )
    ).scalars():
        scopes.append(("class:" + str(class_id), 300))
    for scope, maximum in sorted(scopes):
        statement = insert(usage).values(scope_hash=digest(scope), day=now().date(), requests=1)
        requests = conn.execute(
            statement.on_conflict_do_update(
                index_elements=[usage.c.scope_hash, usage.c.day],
                set_={"requests": usage.c.requests + 1},
            ).returning(usage.c.requests)
        ).scalar_one()
        if requests > maximum:
            raise HTTPException(
                429, "Đã đạt giới hạn trợ giảng hôm nay; em vẫn học và dùng gợi ý nội bộ được"
            )


def respond(conn, user, payload):
    row, version = allowed_lesson(conn, user, payload.lesson_id)
    if _throttle("academy-tutor:" + str(user["id"]), 10):
        raise HTTPException(429, "Em chờ một phút rồi thử lại nhé", headers={"Retry-After": "60"})
    reason = moderation_reason(payload.tried)
    if reason:
        conn.execute(
            db.table("ai_moderation_reviews")
            .insert()
            .values(student_id=user["id"], reason_code=reason)
        )
        event(conn, user["id"], row["id"], "moderation_triggered", {"reason": reason})
        return {
            "mode": "blocked",
            "message": "Em dùng dữ liệu mẫu của bài, giữ thông tin riêng và nhờ người lớn nếu cần nhé.",
        }
    data = version["payload"]
    level = (
        payload.level
        if "learning.guided_hints" in resolve_membership(conn, user["id"])["features"]
        else 1
    )
    if payload.mode == "GiveHint":
        if not payload.tried.strip():
            raise HTTPException(422, "Em thử một bước trước rồi xin gợi ý nhé")
        hints = next(
            (s["activity"].get("hints", []) for s in data["steps"] if s.get("activity")), []
        )
        fallback = hints[min(level, len(hints)) - 1] if hints else data["support"]
        event(conn, user["id"], row["id"], "hint_requested", {"level": level})
    elif payload.mode == "AskSocraticQuestion":
        fallback = "Em dựa vào chi tiết nào trong bài? Em có thể kiểm tra bằng một cách khác không?"
    elif payload.mode == "PracticeEnglish":
        fallback = "Hello! · Hi! · What is this? · This is a book. Hãy dùng nhân vật mẫu và thử một câu em đã học."
    elif payload.mode == "BrainstormStory":
        fallback = "Chọn nhân vật mẫu, bối cảnh, một vấn đề nhỏ và cách giải quyết. Em tự viết mỗi khung một câu."
    elif payload.mode == "ReviewStudentDraft":
        fallback = "Tự kiểm tra: ý đã rõ chưa, có căn cứ không, chữ đầu câu/dấu cuối và nguồn hỗ trợ đã đủ chưa? Giáo viên sẽ nhận xét bản viết của em."
    else:
        fallback = data["steps"][1]["text"]
    provider = db.table("ai_provider_configs")
    configured = conn.execute(
        select(provider).where(
            provider.c.code == "ollama",
            provider.c.enabled.is_(True),
            provider.c.policy_approved.is_(True),
        )
    ).first()
    if (
        settings().ai_training_only
        or not flags(conn).get("tutor_enabled")
        or not configured
        or settings().ai_provider != "ollama"
        or not consent(conn, user["id"])
    ):
        return {
            "mode": "simulation",
            "message": fallback,
            "notice": "Hướng dẫn biên soạn sẵn; chưa gọi mô hình AI. AI có thể sai.",
        }
    # No child free text, identity, answers or profile is sent to the model.
    reserve_quota(conn, user["id"])
    with _lock:
        blocked = _circuit["until"] > time.monotonic()
    if blocked:
        return {
            "mode": "fallback",
            "message": fallback,
            "notice": "Mô hình tạm nghỉ; dùng nội dung nội bộ đã duyệt.",
        }
    prompt_templates = db.table("ai_prompt_templates")
    template = conn.execute(
        select(prompt_templates.c.template)
        .where(prompt_templates.c.mode == payload.mode, prompt_templates.c.status == "approved")
        .order_by(prompt_templates.c.version.desc())
        .limit(1)
    ).scalar()
    prompt = {
        "grade": row["grade"],
        "mode": payload.mode,
        "approved_lesson": data["steps"][1]["text"],
        "approved_hint": fallback,
    }
    try:
        from app.academy.providers import OllamaProvider

        text = OllamaProvider().generate(prompt, template)
        if (
            not isinstance(text, str)
            or not text.strip()
            or len(text) > 1200
            or moderation_reason(text)
            or not consent(conn, user["id"])
            or not flags(conn).get("tutor_enabled")
        ):
            raise ValueError("Output did not pass policy")
        with _lock:
            _circuit.update(failures=0, until=0)
        return {
            "mode": "ollama",
            "message": text,
            "notice": "Gợi ý do mô hình tạo, có thể sai. Em kiểm tra với bài học và giáo viên.",
        }
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        with _lock:
            _circuit["failures"] += 1
            if _circuit["failures"] >= 3:
                _circuit["until"] = time.monotonic() + 60
        return {
            "mode": "fallback",
            "message": fallback,
            "notice": "Mô hình chưa phản hồi an toàn; dùng hướng dẫn nội bộ.",
        }
