from copy import deepcopy

from fastapi import HTTPException
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.academy.schemas import LessonContent
from app.core.security import now
from app.db import db


def audit(conn, actor, action, entity=None, metadata=None):
    conn.execute(
        db.table("ai_audit_logs")
        .insert()
        .values(actor_id=actor, action=action, entity_id=entity, metadata=metadata or {})
    )


def event(conn, student, lesson_id, kind, properties=None):
    conn.execute(
        db.table("ai_events")
        .insert()
        .values(
            student_id=student, lesson_id=lesson_id, event_type=kind, properties=properties or {}
        )
    )


def staff(conn, user, permission="editor"):
    if "admin" in user["roles"]:
        return
    if "teacher" not in user["roles"]:
        raise HTTPException(
            403, "Quyền biên soạn chỉ có hiệu lực với tài khoản giáo viên còn được phân quyền"
        )
    table = db.table("ai_staff_roles")
    if not conn.execute(
        select(table.c.user_id).where(
            table.c.user_id == user["id"],
            table.c.role.in_(["editor", "reviewer"])
            if permission == "read"
            else table.c.role == permission,
        )
    ).first():
        raise HTTPException(403, "Chưa có quyền biên soạn/kiểm duyệt Academy")


def lesson_row(conn, identifier):
    lessons, units = (db.table(n) for n in ("ai_lessons", "ai_units"))
    row = (
        conn.execute(select(lessons, units.c.grade).join(units).where(lessons.c.id == identifier))
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài Academy")
    return dict(row)


def allowed_lesson(conn, user, identifier):
    row = lesson_row(conn, identifier)
    from app.academy.access import lesson_access

    lesson_access(conn, user, row)
    if "admin" not in user["roles"]:
        profiles = db.table("student_profiles")
        grade = conn.execute(
            select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
        ).scalar()
        if "student" not in user["roles"] or grade is None or row["grade"] > grade:
            raise HTTPException(403, "Em chỉ học lớp hiện tại và các bài lớp dưới để ôn tập")
    versions = db.table("ai_lesson_versions")
    version = (
        conn.execute(
            select(versions).where(
                versions.c.lesson_id == identifier, versions.c.status == "published"
            )
        )
        .mappings()
        .first()
    )
    if not version:
        raise HTTPException(404, "Bài chưa được xuất bản")
    return row, dict(version)


def public_content(payload):
    data = deepcopy(payload)
    # Remove grading and teacher-only instructions before JSON reaches students.
    # The latter two are hint levels 2/3: deliver them only through the gated hint endpoint.
    for key in ("teacher_guide", "misconceptions", "standard", "advanced"):
        data.pop(key, None)
    for step in data["steps"]:
        for q in step.get("questions", []):
            q.pop("answer", None)
            q.pop("explanation", None)
        if step.get("activity"):
            step["activity"].pop("hints", None)
            step["activity"].pop("explanation", None)
            for item in step["activity"]["items"]:
                item.pop("answer", None)
    return data


def start(conn, user, identifier):
    row, version = allowed_lesson(conn, user, identifier)
    profiles = db.table("student_profiles")
    conn.execute(
        select(profiles.c.student_id).where(profiles.c.student_id == user["id"]).with_for_update()
    )
    from app.academy.access import lesson_access

    lesson_access(conn, user, row)
    progress = db.table("ai_progress")
    inserted = conn.execute(
        insert(progress)
        .values(student_id=user["id"], lesson_id=identifier, version_id=version["id"])
        .on_conflict_do_nothing()
        .returning(progress.c.student_id)
    ).first()
    if inserted:
        event(conn, user["id"], identifier, "lesson_started")
    state = (
        conn.execute(
            select(progress)
            .where(progress.c.student_id == user["id"], progress.c.lesson_id == identifier)
            .with_for_update()
        )
        .mappings()
        .one()
    )
    pinned = (
        conn.execute(
            select(db.table("ai_lesson_versions")).where(
                db.table("ai_lesson_versions").c.id == state["version_id"]
            )
        )
        .mappings()
        .one()
    )
    return row, dict(state), LessonContent.model_validate(pinned["payload"]).model_dump()


def current_step(conn, user, identifier, step_id):
    row, progress, payload = start(conn, user, identifier)
    index = next((i for i, s in enumerate(payload["steps"]) if s["id"] == step_id), None)
    if index is None:
        raise HTTPException(404, "Không tìm thấy bước học")
    if index > progress["next_step"]:
        raise HTTPException(409, "Em hoàn thành bước hiện tại trước nhé")
    return row, progress, payload, index, payload["steps"][index]


def grade_step(step, answers, level=2):
    if step["kind"] == "quiz":
        correct = {q["id"]: str(q["answer"]) for q in step["questions"]}
        explanations = {q["id"]: q["explanation"] for q in step["questions"]}
    elif step.get("activity"):
        items = step["activity"]["items"]
        items = items[: min(len(items), level + 1)] if level < 3 else items
        correct = {item["id"]: item["answer"] for item in items}
        explanations = {item["id"]: step["activity"]["explanation"] for item in items}
    else:
        raise HTTPException(422, "Bước này không chấm tự động")
    if set(answers) != set(correct):
        raise HTTPException(422, "Cần trả lời đủ và đúng các mục trong bước học")
    matches = {key: value.strip() == correct[key] for key, value in answers.items()}
    if step["kind"] == "quiz":
        valid_choices = {
            q["id"]: {str(i) for i in range(len(q["options"]))} for q in step["questions"]
        }
    else:
        valid_choices = {item["id"]: set(step["activity"]["choices"]) for item in items}
    if any(value not in valid_choices[key] for key, value in answers.items()):
        raise HTTPException(
            422, "Chỉ chọn đáp án có sẵn trong hoạt động, không nhập thông tin riêng"
        )
    score = sum(matches.values()) / len(matches)
    return score, {
        "passed": score >= 0.7,
        "items": [
            {"id": key, "correct": matches[key], "explanation": explanations[key]}
            for key in matches
        ],
        "message": "Em đã có căn cứ tốt. Hãy nêu cách kiểm tra."
        if score >= 0.7
        else "Em thử lại từng mục và đọc giải thích nhé.",
    }


def attempt(conn, user, identifier, payload):
    row, progress, content, index, step = current_step(conn, user, identifier, payload.step_id)
    attempts = db.table("ai_attempts")
    previous = (
        conn.execute(
            select(attempts).where(
                attempts.c.student_id == user["id"],
                attempts.c.idempotency_key == payload.idempotency_key,
            )
        )
        .mappings()
        .first()
    )
    if previous:
        if (
            previous["version_id"] != progress["version_id"]
            or previous["step_id"] != payload.step_id
            or previous["answers"] != payload.answers
            or previous["level"] != payload.level
        ):
            raise HTTPException(409, "Mã lượt làm đã dùng cho yêu cầu khác")
        return dict(previous)
    score, feedback = grade_step(step, payload.answers, payload.level)
    result = (
        conn.execute(
            attempts.insert()
            .values(
                student_id=user["id"],
                version_id=progress["version_id"],
                step_id=payload.step_id,
                idempotency_key=payload.idempotency_key,
                answers=payload.answers,
                level=payload.level,
                score=score,
                feedback=feedback,
            )
            .returning(attempts)
        )
        .mappings()
        .one()
    )
    event(
        conn,
        user["id"],
        identifier,
        "activity_attempted",
        {"kind": step["kind"], "score": score, "level": payload.level},
    )
    competency = db.table("ai_competency_progress")
    for code in content["competencies"]:
        conn.execute(
            insert(competency)
            .values(
                student_id=user["id"],
                competency=code,
                evidence_count=1,
                successful_count=int(score >= 0.7),
            )
            .on_conflict_do_update(
                index_elements=[competency.c.student_id, competency.c.competency],
                set_={
                    "evidence_count": competency.c.evidence_count + 1,
                    "successful_count": competency.c.successful_count + int(score >= 0.7),
                },
            )
        )
    return dict(result)


def complete_step(conn, user, identifier, step_id):
    row, state, content, index, step = current_step(conn, user, identifier, step_id)
    if index < state["next_step"]:
        return state
    if step["kind"] in {"activity", "quiz"}:
        attempts = db.table("ai_attempts")
        if not conn.execute(
            select(attempts.c.id).where(
                attempts.c.student_id == user["id"],
                attempts.c.version_id == state["version_id"],
                attempts.c.step_id == step_id,
                attempts.c.score >= 0.7,
            )
        ).first():
            raise HTTPException(409, "Em thử hoạt động/checkpoint đạt trước khi tiếp tục nhé")
    progress = db.table("ai_progress")
    finished = index + 1 == len(content["steps"])
    conn.execute(
        update(progress)
        .where(progress.c.student_id == user["id"], progress.c.lesson_id == identifier)
        .values(next_step=index + 1, completed_at=now() if finished else None, updated_at=now())
    )
    event(conn, user["id"], identifier, "step_completed", {"step": step_id})
    if finished:
        ledger = db.table("ai_rewards_ledger")
        earned = conn.execute(
            insert(ledger)
            .values(student_id=user["id"], lesson_id=identifier, points=10)
            .on_conflict_do_nothing()
            .returning(ledger.c.student_id)
        ).first()
        if earned:
            event(conn, user["id"], identifier, "lesson_completed")
        count = conn.execute(
            select(func.count()).select_from(ledger).where(ledger.c.student_id == user["id"])
        ).scalar_one()
        badges, student_badges = db.table("ai_badges"), db.table("ai_student_badges")
        for code in conn.execute(
            select(badges.c.code).where(badges.c.threshold <= count)
        ).scalars():
            inserted = conn.execute(
                insert(student_badges)
                .values(student_id=user["id"], badge_code=code)
                .on_conflict_do_nothing()
                .returning(student_badges.c.badge_code)
            ).first()
            if inserted:
                event(conn, user["id"], identifier, "badge_earned", {"badge": code})
    return {"next_step": index + 1, "completed_at": now() if finished else None}


def catalog(conn, grade, student_id=None):
    from app.services.access import resolve_membership

    vip = student_id is None or "academy.full" in resolve_membership(conn, student_id)["features"]
    media = db.table("ai_media_assets")
    covers = set(
        conn.execute(
            select(media.c.code).where(media.c.category == "cover", media.c.status == "approved")
        ).scalars()
    )
    units, lessons, versions, progress = (
        db.table(n) for n in ("ai_units", "ai_lessons", "ai_lesson_versions", "ai_progress")
    )
    query = (
        select(
            lessons.c.id,
            lessons.c.code,
            lessons.c.title,
            lessons.c.position,
            lessons.c.minimum_plan_code,
            units.c.id.label("unit_id"),
            units.c.title.label("unit_title"),
            units.c.code.label("unit_code"),
            units.c.position.label("unit_position"),
            versions.c.payload["hero"].as_string().label("hero"),
            versions.c.payload["estimated_minutes"].as_integer().label("minutes"),
        )
        .select_from(lessons.join(units).join(versions))
        .where(units.c.grade == grade, versions.c.status == "published")
        .order_by(units.c.position, lessons.c.position)
    )
    states = (
        {
            r["lesson_id"]: dict(r)
            for r in conn.execute(
                select(progress).where(
                    progress.c.student_id == student_id,
                    progress.c.lesson_id.in_(
                        select(lessons.c.id).join(units).where(units.c.grade == grade)
                    ),
                )
            ).mappings()
        }
        if student_id
        else {}
    )
    return [
        dict(
            id=r["id"],
            code=r["code"],
            title=r["title"],
            position=r["position"],
            unit_id=r["unit_id"],
            unit_title=r["unit_title"],
            unit_code=r["unit_code"],
            unit_cover=("cover-" + r["unit_code"])
            if ("cover-" + r["unit_code"]) in covers
            else r["hero"],
            unit_position=r["unit_position"],
            hero=r["hero"],
            minutes=r["minutes"],
            minimum_plan_code=r["minimum_plan_code"],
            locked=r["minimum_plan_code"] == "vip" and not vip,
            progress=states.get(r["id"]),
        )
        for r in conn.execute(query).mappings()
    ]
