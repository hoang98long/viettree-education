import hashlib
import json
from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db
from app.lesson_schemas import LessonInput
from app.lesson_support import enrich
from app.services.authoring import audit, scope, validate_stored


def base(conn, identifier, lock=False):
    lessons, topics, policies = (
        db.table(name) for name in ("lessons", "topics", "content_access_policies")
    )
    statement = select(lessons).where(lessons.c.id == identifier)
    if lock:
        statement = statement.with_for_update()
    row = conn.execute(statement).mappings().first()
    if not row:
        raise HTTPException(404, "Không tìm thấy bài học")
    topic = conn.execute(select(topics).where(topics.c.id == row["topic_id"])).mappings().one()
    policy = (
        conn.execute(select(policies).where(policies.c.lesson_id == identifier)).mappings().first()
    )
    links = db.table("lesson_skills")
    skills = list(
        conn.execute(
            select(links.c.skill_id)
            .where(links.c.lesson_id == identifier)
            .order_by(links.c.skill_id)
        ).scalars()
    )
    fingerprint = hashlib.sha256(
        json.dumps(
            jsonable_encoder(
                {"lesson": dict(row), "policy": dict(policy) if policy else None, "skills": skills}
            ),
            sort_keys=True,
        ).encode()
    ).hexdigest()
    payload = {
        "code": row["code"],
        "grade": topic["grade"],
        "subject_id": topic["subject_id"],
        "topic_id": row["topic_id"],
        "skill_ids": skills,
        "title": row["title"],
        "description": row["description"] or "",
        "estimated_minutes": row["estimated_minutes"] or 15,
        "sort_order": row["sort_order"],
        "content": enrich(row["content"], topic["code"]),
        "minimum_plan_code": policy["minimum_plan_code"] if policy else "free",
        "learning_level": policy["learning_level"] if policy else "basic",
        "preview": policy["preview"] if policy else {},
    }
    return dict(row), jsonable_encoder(payload), fingerprint


def detail(conn, identifier):
    row, payload, fingerprint = base(conn, identifier)
    drafts = db.table("lesson_drafts")
    draft = conn.execute(select(drafts).where(drafts.c.lesson_id == identifier)).mappings().first()
    logs, users = db.table("audit_logs"), db.table("users")
    history = conn.execute(
        select(
            logs.c.action,
            logs.c.created_at,
            users.c.display_name.label("actor_name"),
            logs.c.new_values,
        )
        .select_from(logs.outerjoin(users, users.c.id == logs.c.actor_user_id))
        .where(
            logs.c.entity_type == "lesson",
            logs.c.entity_id == identifier,
            logs.c.action.like("authoring.lesson.%"),
        )
        .order_by(logs.c.created_at.desc(), logs.c.id.desc())
        .limit(20)
    ).mappings()
    return {
        "id": identifier,
        "lesson_status": row["status"],
        "draft_status": draft["status"] if draft else "none",
        "edit_revision": draft["edit_revision"] if draft else 0,
        "source_fingerprint": draft["source_fingerprint"] if draft else fingerprint,
        "source_changed": bool(draft and draft["source_fingerprint"] != fingerprint),
        "payload": draft["payload"] if draft else payload,
        "history": [
            {
                "action": item["action"],
                "created_at": item["created_at"],
                "actor_name": item["actor_name"],
                "reason": item["new_values"].get("reason", ""),
            }
            for item in history
        ],
    }


def draft_locked(conn, identifier, expected):
    table = db.table("lesson_drafts")
    draft = (
        conn.execute(select(table).where(table.c.lesson_id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if (draft["edit_revision"] if draft else 0) != expected:
        raise HTTPException(409, "Bản nháp đã thay đổi. Tải lại để tránh ghi đè")
    return draft


def save(conn, actor, payload, identifier=None):
    scope(conn, payload.grade, payload.subject_id, payload.topic_id, payload.skill_ids)
    lessons, drafts = db.table("lessons"), db.table("lesson_drafts")
    created = identifier is None
    stored = payload.model_dump(mode="json", exclude={"expected_revision", "source_fingerprint"})
    if created:
        if payload.expected_revision != 0:
            raise HTTPException(422, "Bài mới chưa có revision")
        conn.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:code, 0))"),
            {"code": f"lesson:{payload.topic_id}:{payload.code}"},
        )
        if conn.execute(
            select(lessons.c.id).where(
                lessons.c.topic_id == payload.topic_id, lessons.c.code == payload.code
            )
        ).first():
            raise HTTPException(409, "Mã bài học đã tồn tại trong chủ đề")
        identifier = uuid4()
        conn.execute(
            lessons.insert().values(
                id=identifier,
                topic_id=payload.topic_id,
                code=payload.code,
                title=payload.title,
                content={},
                status="draft",
                created_by=actor,
            )
        )
        row, _, fingerprint = base(conn, identifier, True)
        draft = None
    else:
        row, current, fingerprint = base(conn, identifier, True)
        draft = draft_locked(conn, identifier, payload.expected_revision)
        if payload.source_fingerprint != fingerprint:
            raise HTTPException(
                409,
                "Bài đang xuất bản hoặc quyền truy cập đã thay đổi. Tải lại và tạo nháp từ bản hiện tại",
            )
        if any(
            str(stored[key]) != str(current[key])
            for key in ("code", "topic_id", "subject_id", "grade")
        ):
            raise HTTPException(422, "Mã, môn, lớp và chủ đề của bài đã tạo không được thay đổi")
    revision = (draft["edit_revision"] if draft else 0) + 1
    values = dict(
        payload=stored,
        source_fingerprint=fingerprint,
        edit_revision=revision,
        status="draft",
        updated_by=actor,
        reviewed_by=None,
        reviewed_at=None,
        updated_at=now(),
    )
    conn.execute(
        insert(drafts)
        .values(lesson_id=identifier, **values)
        .on_conflict_do_update(index_elements=[drafts.c.lesson_id], set_=values)
    )
    audit(
        conn,
        actor,
        "lesson.save",
        "lesson",
        identifier,
        dict(draft) if draft else None,
        {**values, "created": created},
    )
    return detail(conn, identifier)


def action(conn, actor, identifier, name, payload):
    row, current, fingerprint = base(conn, identifier, True)
    draft = draft_locked(conn, identifier, payload.expected_revision)
    drafts = db.table("lesson_drafts")
    if name == "reset":
        values = dict(
            payload=current,
            source_fingerprint=fingerprint,
            edit_revision=payload.expected_revision + 1,
            status="draft",
            updated_by=actor,
            reviewed_by=None,
            reviewed_at=None,
            updated_at=now(),
        )
        conn.execute(
            insert(drafts)
            .values(lesson_id=identifier, **values)
            .on_conflict_do_update(index_elements=[drafts.c.lesson_id], set_=values)
        )
    else:
        if not draft or draft["status"] == "published":
            raise HTTPException(409, "Hãy lưu bản nháp mới trước")
        if draft["source_fingerprint"] != fingerprint:
            raise HTTPException(
                409, "Bài hoặc quyền truy cập đã thay đổi. Tạo nháp từ bản hiện tại trước khi duyệt"
            )
        checked = validate_stored(LessonInput, draft["payload"])
        scope(conn, checked.grade, checked.subject_id, checked.topic_id, checked.skill_ids)
        values = dict(edit_revision=draft["edit_revision"] + 1, updated_by=actor, updated_at=now())
        if name == "review":
            values.update(status="reviewed", reviewed_by=actor, reviewed_at=now())
        else:
            if draft["status"] != "reviewed":
                raise HTTPException(409, "Cần duyệt đúng bản nháp trước khi xuất bản")
            lessons, policies, links = (
                db.table(name) for name in ("lessons", "content_access_policies", "lesson_skills")
            )
            conn.execute(
                lessons.update()
                .where(lessons.c.id == identifier)
                .values(
                    title=checked.title,
                    description=checked.description,
                    content=checked.content.model_dump(),
                    sort_order=checked.sort_order,
                    estimated_minutes=checked.estimated_minutes,
                    status="published",
                    updated_at=now(),
                )
            )
            policy_values = dict(
                minimum_plan_code=checked.minimum_plan_code,
                learning_level=checked.learning_level,
                preview=checked.preview.model_dump(),
                updated_by=actor,
                updated_at=now(),
            )
            conn.execute(
                insert(policies)
                .values(lesson_id=identifier, **policy_values)
                .on_conflict_do_update(index_elements=[policies.c.lesson_id], set_=policy_values)
            )
            conn.execute(links.delete().where(links.c.lesson_id == identifier))
            conn.execute(
                links.insert(),
                [
                    {"lesson_id": identifier, "skill_id": skill, "is_primary": index == 0}
                    for index, skill in enumerate(checked.skill_ids)
                ],
            )
            _, _, new_fingerprint = base(conn, identifier)
            values.update(status="published", source_fingerprint=new_fingerprint)
        conn.execute(drafts.update().where(drafts.c.lesson_id == identifier).values(**values))
    audit(
        conn,
        actor,
        "lesson." + name,
        "lesson",
        identifier,
        {"lesson": row, "draft": dict(draft) if draft else None},
        {**values, "reason": payload.reason},
    )
    return detail(conn, identifier)


def listing(conn, grade=4, subject_code=None, status=None, search="", page=1):
    lessons, topics, subjects, drafts, policies = (
        db.table(name)
        for name in ("lessons", "topics", "subjects", "lesson_drafts", "content_access_policies")
    )
    joined = (
        lessons.join(topics)
        .join(subjects)
        .outerjoin(drafts, drafts.c.lesson_id == lessons.c.id)
        .outerjoin(policies, policies.c.lesson_id == lessons.c.id)
    )
    conditions = [topics.c.grade == grade]
    if subject_code:
        conditions.append(subjects.c.code == subject_code)
    if search:
        pattern = "%" + search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        conditions.append(
            lessons.c.title.ilike(pattern, escape="\\") | lessons.c.code.ilike(pattern, escape="\\")
        )
    if status == "pending":
        conditions.append(drafts.c.status.in_(["draft", "reviewed"]))
    elif status:
        conditions.append(lessons.c.status == status)
    total = conn.execute(select(func.count()).select_from(joined).where(*conditions)).scalar_one()
    rows = conn.execute(
        select(
            lessons.c.id,
            lessons.c.title,
            lessons.c.code,
            lessons.c.status,
            lessons.c.estimated_minutes,
            topics.c.title.label("topic_title"),
            subjects.c.name_vi.label("subject_name"),
            drafts.c.status.label("draft_status"),
            policies.c.minimum_plan_code,
        )
        .select_from(joined)
        .where(*conditions)
        .order_by(lessons.c.updated_at.desc(), lessons.c.id)
        .offset((page - 1) * 20)
        .limit(20)
    ).mappings()
    return {"total": total, "page": page, "items": list(rows)}
