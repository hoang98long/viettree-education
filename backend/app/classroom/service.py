import hashlib
import json
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import func, select, text, update
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db


def audit(conn, user, action, identifier=None, details=None):
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            actor_user_id=user["id"],
            action=action,
            entity_type="classroom",
            entity_id=identifier,
            new_values=details or {},
        )
    )


def staff(user):
    if not set(user["roles"]) & {"admin", "teacher"}:
        raise HTTPException(403, "Chức năng dành cho quản trị hoặc giáo viên")


def class_scope(conn, user, identifier, staff_only=False, lock=False):
    classes = db.table("classes")
    query = select(classes).where(classes.c.id == identifier)
    if lock:
        query = query.with_for_update()
    row = conn.execute(query).mappings().first()
    if not row:
        raise HTTPException(404, "Không tìm thấy lớp")
    if "admin" in user["roles"] or (
        "teacher" in user["roles"] and row["teacher_user_id"] == user["id"] and row["is_active"]
    ):
        return dict(row)
    enrolled = db.table("class_enrollments")
    if (
        not staff_only
        and "student" in user["roles"]
        and row["is_active"]
        and conn.execute(
            select(enrolled.c.student_id).where(
                enrolled.c.class_id == identifier,
                enrolled.c.student_id == user["id"],
                enrolled.c.left_at.is_(None),
            )
        ).first()
    ):
        return dict(row)
    raise HTTPException(403, "Chưa có quyền với lớp này")


def validate_student(conn, identifier, classroom=None):
    profiles, users, roles = (db.table(n) for n in ("student_profiles", "users", "user_roles"))
    row = (
        conn.execute(
            select(profiles)
            .join(users, users.c.id == profiles.c.student_id)
            .join(roles, roles.c.user_id == users.c.id)
            .where(
                profiles.c.student_id == identifier,
                users.c.is_active.is_(True),
                roles.c.role == "student",
            )
        )
        .mappings()
        .first()
    )
    if not row or (
        classroom
        and (
            row["current_grade"] != classroom["grade"]
            or (classroom["school_id"] and row["school_id"] != classroom["school_id"])
        )
    ):
        raise HTTPException(422, "Chọn học sinh đang hoạt động, cùng khối và trường với lớp")
    return dict(row)


def save_class(conn, user, payload, identifier=None):
    classes = db.table("classes")
    old = None
    if identifier:
        old = (
            conn.execute(select(classes).where(classes.c.id == identifier).with_for_update())
            .mappings()
            .first()
        )
        if not old:
            raise HTTPException(404, "Không tìm thấy lớp")
        if payload.revision != old["edit_revision"]:
            raise HTTPException(409, "Lớp đã thay đổi, tải lại trước khi lưu")
        if payload.grade != old["grade"] or payload.school_id != old["school_id"]:
            enrollments = db.table("class_enrollments")
            if conn.execute(
                select(enrollments.c.student_id).where(
                    enrollments.c.class_id == identifier, enrollments.c.left_at.is_(None)
                )
            ).first():
                raise HTTPException(
                    409, "Lớp đang có học sinh; chuyển học sinh trước khi đổi khối/trường"
                )
    if payload.teacher_id:
        users, roles = db.table("users"), db.table("user_roles")
        if not conn.execute(
            select(users.c.id)
            .join(roles)
            .where(
                users.c.id == payload.teacher_id,
                users.c.is_active.is_(True),
                roles.c.role == "teacher",
            )
        ).first():
            raise HTTPException(422, "Giáo viên không khả dụng")
    if payload.school_id:
        schools = db.table("schools")
        if not conn.execute(
            select(schools.c.id).where(
                schools.c.id == payload.school_id, schools.c.is_active.is_(True)
            )
        ).first():
            raise HTTPException(422, "Trường không khả dụng")
    values = dict(
        name=payload.name,
        grade=payload.grade,
        teacher_user_id=payload.teacher_id,
        school_id=payload.school_id,
        academic_year=payload.academic_year,
        is_active=payload.is_active,
        updated_at=now(),
    )
    identifier = identifier or uuid4()
    if old:
        conn.execute(
            update(classes)
            .where(classes.c.id == identifier)
            .values(**values, edit_revision=old["edit_revision"] + 1)
        )
    else:
        conn.execute(
            classes.insert().values(id=identifier, code="VT-" + identifier.hex[:12], **values)
        )
    settings = db.table("classroom_settings")
    conn.execute(
        insert(settings)
        .values(
            class_id=identifier,
            recognition_enabled=payload.recognition_enabled,
            updated_by=user["id"],
        )
        .on_conflict_do_update(
            index_elements=[settings.c.class_id],
            set_={
                "recognition_enabled": payload.recognition_enabled,
                "updated_by": user["id"],
                "updated_at": now(),
            },
        )
    )
    audit(conn, user, "classroom.saved", identifier, {"active": payload.is_active})
    return {"id": identifier, "revision": old["edit_revision"] + 1 if old else 1}


def enroll(conn, user, identifier, payload):
    classroom = class_scope(conn, user, identifier, staff_only=True, lock=True)
    classes = db.table("classes")
    conn.execute(select(classes.c.id).where(classes.c.id == identifier).with_for_update())
    if payload.enrolled:
        if not classroom["is_active"]:
            raise HTTPException(409, "Mở lại lớp trước khi ghi danh")
        validate_student(conn, payload.student_id, classroom)
    table = db.table("class_enrollments")
    if payload.enrolled:
        conn.execute(
            insert(table)
            .values(
                class_id=identifier,
                student_id=payload.student_id,
                recognition_alias="Bạn " + payload.student_id.hex[:6],
            )
            .on_conflict_do_update(
                index_elements=[table.c.class_id, table.c.student_id], set_={"left_at": None}
            )
        )
    elif not conn.execute(
        update(table)
        .where(
            table.c.class_id == identifier,
            table.c.student_id == payload.student_id,
            table.c.left_at.is_(None),
        )
        .values(left_at=now())
    ).rowcount:
        raise HTTPException(409, "Học sinh không còn ở lớp này")
    audit(
        conn,
        user,
        "classroom.enrollment",
        identifier,
        {"student_id": str(payload.student_id), "enrolled": payload.enrolled},
    )
    return {"enrolled": payload.enrolled}


def assign(conn, user, payload):
    staff(user)
    fingerprint = hashlib.sha256(
        json.dumps(
            payload.model_dump(mode="json", exclude={"idempotency_key"}), sort_keys=True
        ).encode()
    ).hexdigest()
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
        {"key": f"classroom-assign:{user['id']}:{payload.idempotency_key}"},
    )
    batches, targets = (
        db.table("learning_assignment_batches"),
        db.table("learning_assignment_targets"),
    )
    old = (
        conn.execute(
            select(batches).where(
                batches.c.actor_id == user["id"],
                batches.c.idempotency_key == payload.idempotency_key,
            )
        )
        .mappings()
        .first()
    )
    if old:
        if old["fingerprint"] != fingerprint:
            raise HTTPException(409, "Mã thao tác đã dùng cho nội dung khác")
        return {
            "id": old["id"],
            "count": conn.execute(
                select(func.count()).select_from(targets).where(targets.c.batch_id == old["id"])
            ).scalar_one(),
            "replayed": True,
        }
    if payload.due_at and payload.due_at <= now():
        raise HTTPException(422, "Hạn nộp phải ở tương lai")
    enrollments, classes = db.table("class_enrollments"), db.table("classes")
    if payload.class_id:
        classroom = class_scope(conn, user, payload.class_id, staff_only=True, lock=True)
        if not classroom["is_active"]:
            raise HTTPException(409, "Lớp đã đóng")
        conn.execute(select(classes.c.id).where(classes.c.id == payload.class_id).with_for_update())
        identifiers = list(
            conn.execute(
                select(enrollments.c.student_id)
                .where(enrollments.c.class_id == payload.class_id, enrollments.c.left_at.is_(None))
                .order_by(enrollments.c.student_id)
            ).scalars()
        )
    else:
        identifiers = sorted(payload.student_ids, key=str)
        classroom = None
    if not identifiers or len(identifiers) > 50:
        raise HTTPException(422, "Chọn từ 1 đến 50 học sinh; lớp lớn chia nhóm để giao")
    for identifier in identifiers:
        validate_student(conn, identifier, classroom)
        if (
            "admin" not in user["roles"]
            and not conn.execute(
                select(enrollments.c.student_id)
                .join(classes)
                .where(
                    enrollments.c.student_id == identifier,
                    enrollments.c.left_at.is_(None),
                    classes.c.teacher_user_id == user["id"],
                    classes.c.is_active.is_(True),
                )
            ).first()
        ):
            raise HTTPException(403, "Chỉ giao cho học sinh ở lớp được phân công")
    linked = {}
    if payload.kind == "assessment":
        from app.schemas.authoring import AssignmentInput
        from app.services.authoring import assign_students

        assigned = assign_students(
            conn,
            user["id"],
            payload.resource_id,
            AssignmentInput(student_ids=identifiers, due_at=payload.due_at),
        )
        for row in assigned["assignments"]:
            linked[row["student_id"]] = row["id"]
    elif payload.kind == "ai_lesson":
        from app.academy.learning import allowed_lesson

        for identifier in identifiers:
            allowed_lesson(conn, {"id": identifier, "roles": ["student"]}, payload.resource_id)
    else:
        from app.services.access import authorize_content

        lessons, topics = db.table("lessons"), db.table("topics")
        row = conn.execute(
            select(topics.c.grade)
            .join(lessons)
            .where(
                lessons.c.id == payload.resource_id,
                lessons.c.status == "published",
                topics.c.is_active.is_(True),
            )
        ).first()
        if not row:
            raise HTTPException(404, "Bài học chưa xuất bản")
        for identifier in identifiers:
            authorize_content(
                conn,
                {"id": identifier, "roles": ["student"]},
                "lesson",
                payload.resource_id,
                row.grade,
            )
    batch_id = uuid4()
    conn.execute(
        batches.insert().values(
            id=batch_id,
            actor_id=user["id"],
            class_id=payload.class_id,
            kind=payload.kind,
            resource_id=payload.resource_id,
            idempotency_key=payload.idempotency_key,
            fingerprint=fingerprint,
            due_at=payload.due_at,
        )
    )
    for identifier in identifiers:
        conn.execute(
            targets.insert().values(
                batch_id=batch_id, student_id=identifier, assignment_id=linked.get(identifier)
            )
        )
    audit(
        conn,
        user,
        "classroom.assigned",
        batch_id,
        {"kind": payload.kind, "count": len(identifiers)},
    )
    return {"id": batch_id, "count": len(identifiers), "replayed": False}
