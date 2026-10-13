"""Draft authoring, explicit review and immutable published content."""

from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import func, select, text

from app.core.security import now
from app.db import db
from app.schemas.authoring import AssessmentInput, QuestionInput
from app.services import access
from app.services.attempts import lock_student, published_assessment


def audit(conn, actor, action, kind, identifier, before=None, after=None):
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            actor_user_id=actor,
            action="authoring." + action,
            entity_type=kind,
            entity_id=identifier,
            old_values=jsonable_encoder(before or {}),
            new_values=jsonable_encoder(after or {}),
        )
    )


def validate_stored(model, payload):
    try:
        return model.model_validate(payload)
    except ValidationError:
        raise HTTPException(
            422, "Nội dung chưa hợp lệ. Hãy kiểm tra câu hỏi, đáp án và quyền truy cập"
        ) from None


def check_revision(row, expected):
    if expected is None or expected != row["edit_revision"]:
        raise HTTPException(409, "Nội dung đã thay đổi. Hãy tải lại trước khi lưu hoặc duyệt")


def scope(conn, grade, subject_id, topic_id, skill_ids=None, lesson_id=None):
    subjects, topics, skills, lessons = (
        db.table(name) for name in ("subjects", "topics", "skills", "lessons")
    )
    if not conn.execute(
        select(subjects.c.id).where(subjects.c.id == subject_id, subjects.c.is_active.is_(True))
    ).first():
        raise HTTPException(422, "Môn học chưa khả dụng")
    if not conn.execute(
        select(topics.c.id).where(
            topics.c.id == topic_id,
            topics.c.subject_id == subject_id,
            topics.c.grade == grade,
            topics.c.is_active.is_(True),
        )
    ).first():
        raise HTTPException(422, "Chủ đề không thuộc môn hoặc lớp đã chọn")
    if skill_ids is not None:
        valid = set(
            conn.execute(
                select(skills.c.id).where(
                    skills.c.id.in_(skill_ids),
                    skills.c.subject_id == subject_id,
                    skills.c.grade == grade,
                    skills.c.is_active.is_(True),
                )
            ).scalars()
        )
        if valid != set(skill_ids):
            raise HTTPException(422, "Kỹ năng không thuộc môn hoặc lớp đã chọn")
    if (
        lesson_id
        and not conn.execute(
            select(lessons.c.id).where(
                lessons.c.id == lesson_id,
                lessons.c.topic_id == topic_id,
                lessons.c.status == "published",
            )
        ).first()
    ):
        raise HTTPException(422, "Bài học không thuộc chủ đề hoặc chưa xuất bản")


def unique_code(conn, table, code):
    # Serialize identical creations before checking uniqueness; return a useful 409.
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:code, 0))"),
        {"code": table.name + ":" + code},
    )
    if conn.execute(select(table.c.id).where(table.c.code == code)).first():
        raise HTTPException(409, "Mã đã tồn tại. Hãy chọn mã khác")


def question_detail(conn, version_id):
    versions, questions, policies, subjects = (
        db.table(name)
        for name in (
            "question_versions",
            "questions",
            "question_version_access_policies",
            "subjects",
        )
    )
    row = (
        conn.execute(
            select(
                versions,
                questions.c.code,
                questions.c.grade,
                questions.c.subject_id,
                questions.c.topic_id,
                subjects.c.name_vi.label("subject_name"),
                policies.c.minimum_plan_code,
            )
            .select_from(
                versions.join(questions)
                .join(subjects)
                .outerjoin(policies, policies.c.question_version_id == versions.c.id)
            )
            .where(versions.c.id == version_id)
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy câu hỏi")
    links = db.table("question_skills")
    return {
        **dict(row),
        "skill_ids": list(
            conn.execute(
                select(links.c.skill_id)
                .where(links.c.question_version_id == version_id)
                .order_by(links.c.is_primary.desc(), links.c.skill_id)
            ).scalars()
        ),
    }


def question_relations(conn, version_id, payload, actor):
    links, policies = db.table("question_skills"), db.table("question_version_access_policies")
    conn.execute(links.delete().where(links.c.question_version_id == version_id))
    conn.execute(
        links.insert(),
        [
            {
                "question_version_id": version_id,
                "skill_id": value,
                "is_primary": index == 0,
                "weight": 1,
            }
            for index, value in enumerate(payload.skill_ids)
        ],
    )
    from sqlalchemy.dialects.postgresql import insert

    conn.execute(
        insert(policies)
        .values(
            question_version_id=version_id,
            minimum_plan_code=payload.minimum_plan_code,
            updated_by=actor,
            updated_at=now(),
        )
        .on_conflict_do_update(
            index_elements=[policies.c.question_version_id],
            set_={
                "minimum_plan_code": payload.minimum_plan_code,
                "updated_by": actor,
                "updated_at": now(),
            },
        )
    )


def save_question(conn, actor, payload, version_id=None):
    scope(conn, payload.grade, payload.subject_id, payload.topic_id, payload.skill_ids)
    questions, versions = db.table("questions"), db.table("question_versions")
    before = None
    if version_id:
        original = question_detail(conn, version_id)
        conn.execute(
            select(questions.c.id)
            .where(questions.c.id == original["question_id"])
            .with_for_update()
        )
        before = (
            conn.execute(select(versions).where(versions.c.id == version_id).with_for_update())
            .mappings()
            .one()
        )
        if before["status"] != "draft":
            raise HTTPException(
                409, "Bản đã xuất bản hoặc lưu trữ không được sửa. Hãy tạo phiên bản mới"
            )
        check_revision(before, payload.expected_revision)
        if any(
            original[key] != getattr(payload, key)
            for key in ("code", "grade", "subject_id", "topic_id")
        ):
            raise HTTPException(409, "Không đổi mã/môn/lớp/chủ đề của câu hỏi đã tạo")
    else:
        unique_code(conn, questions, payload.code)
        question_id, version_id = uuid4(), uuid4()
        conn.execute(
            questions.insert().values(
                id=question_id,
                code=payload.code,
                grade=payload.grade,
                subject_id=payload.subject_id,
                topic_id=payload.topic_id,
                created_by=actor,
            )
        )
        conn.execute(
            versions.insert().values(
                id=version_id,
                question_id=question_id,
                version=1,
                question_type=payload.question_type,
                content={},
            )
        )
    values = dict(
        question_type=payload.question_type,
        difficulty=payload.difficulty,
        content=payload.content.model_dump(),
        grading=payload.grading,
        explanation={"text": payload.explanation},
        reviewed_by=None,
        edit_revision=before["edit_revision"] + 1 if before else 1,
        updated_at=now(),
    )
    conn.execute(versions.update().where(versions.c.id == version_id).values(**values))
    question_relations(conn, version_id, payload, actor)
    audit(
        conn,
        actor,
        "question.save",
        "question_version",
        version_id,
        before,
        {"code": payload.code, "plan": payload.minimum_plan_code},
    )
    return question_detail(conn, version_id)


def revise_question(conn, actor, version_id):
    original = question_detail(conn, version_id)
    questions, versions = db.table("questions"), db.table("question_versions")
    conn.execute(
        select(questions.c.id).where(questions.c.id == original["question_id"]).with_for_update()
    )
    if conn.execute(
        select(versions.c.id).where(
            versions.c.question_id == original["question_id"], versions.c.status == "draft"
        )
    ).first():
        raise HTTPException(409, "Câu hỏi đã có bản nháp. Hãy sửa bản nháp hiện tại")
    next_version = (
        conn.execute(
            select(func.max(versions.c.version)).where(
                versions.c.question_id == original["question_id"]
            )
        ).scalar_one()
        + 1
    )
    identifier = uuid4()
    conn.execute(
        versions.insert().values(
            id=identifier,
            question_id=original["question_id"],
            version=next_version,
            question_type=original["question_type"],
            difficulty=original["difficulty"],
            content=original["content"],
            grading=original["grading"],
            explanation=original["explanation"],
            max_score=original["max_score"],
            status="draft",
        )
    )
    links = db.table("question_skills")
    for link in conn.execute(
        select(links).where(links.c.question_version_id == version_id)
    ).mappings():
        conn.execute(links.insert().values(**{**dict(link), "question_version_id": identifier}))
    conn.execute(
        db.table("question_version_access_policies")
        .insert()
        .values(
            question_version_id=identifier,
            minimum_plan_code=original["minimum_plan_code"],
            updated_by=actor,
        )
    )
    audit(
        conn,
        actor,
        "question.revise",
        "question_version",
        identifier,
        after={"from_version_id": str(version_id), "version": next_version},
    )
    return question_detail(conn, identifier)


def question_action(conn, actor, version_id, action, payload):
    original = question_detail(conn, version_id)
    questions, versions = db.table("questions"), db.table("question_versions")
    conn.execute(
        select(questions.c.id).where(questions.c.id == original["question_id"]).with_for_update()
    )
    row = (
        conn.execute(select(versions).where(versions.c.id == version_id).with_for_update())
        .mappings()
        .one()
    )
    check_revision(row, payload.expected_revision)
    if action in ("review", "publish"):
        if row["status"] != "draft":
            raise HTTPException(409, "Chỉ duyệt/xuất bản nháp")
        fresh = question_detail(conn, version_id)
        validated = validate_stored(
            QuestionInput,
            {
                "code": fresh["code"],
                "grade": fresh["grade"],
                "subject_id": fresh["subject_id"],
                "topic_id": fresh["topic_id"],
                "skill_ids": fresh["skill_ids"],
                "question_type": fresh["question_type"],
                "difficulty": fresh["difficulty"],
                "content": fresh["content"],
                "grading": fresh["grading"],
                "explanation": fresh["explanation"].get("text", ""),
                "minimum_plan_code": fresh["minimum_plan_code"],
            },
        )
        scope(conn, validated.grade, validated.subject_id, validated.topic_id, validated.skill_ids)
    at = now()
    if action == "review":
        values = {"reviewed_by": actor, "updated_at": at}
    elif action == "publish":
        if not row["reviewed_by"]:
            raise HTTPException(409, "Hãy duyệt nội dung trước khi xuất bản")
        # Old versions remain immutable and usable only in previously published assessments.
        conn.execute(
            versions.update()
            .where(versions.c.question_id == row["question_id"], versions.c.status == "published")
            .values(status="archived", updated_at=at, edit_revision=versions.c.edit_revision + 1)
        )
        values = {"status": "published", "published_at": at, "updated_at": at}
    else:
        if row["status"] == "archived":
            raise HTTPException(409, "Phiên bản đã lưu trữ")
        values = {"status": "archived", "updated_at": at}
    values["edit_revision"] = row["edit_revision"] + 1
    conn.execute(versions.update().where(versions.c.id == version_id).values(**values))
    audit(
        conn,
        actor,
        "question." + action,
        "question_version",
        version_id,
        row,
        {**values, "reason": payload.reason},
    )
    return question_detail(conn, version_id)


def assessment_detail(conn, assessment_id):
    table, items, policies = (
        db.table("assessments"),
        db.table("assessment_items"),
        db.table("content_access_policies"),
    )
    row = conn.execute(select(table).where(table.c.id == assessment_id)).mappings().first()
    if not row:
        raise HTTPException(404, "Không tìm thấy đề")
    policy = (
        conn.execute(select(policies).where(policies.c.assessment_id == assessment_id))
        .mappings()
        .first()
    )
    questions = [
        dict(item)
        for item in conn.execute(
            select(items).where(items.c.assessment_id == assessment_id).order_by(items.c.position)
        ).mappings()
    ]
    for item in questions:
        item["question"] = question_detail(conn, item["question_version_id"])
    return {
        **dict(row),
        "items": questions,
        "minimum_plan_code": policy["minimum_plan_code"] if policy else None,
        "learning_level": policy["learning_level"] if policy else "basic",
        "preview": policy["preview"] if policy else {},
        "effective_access": access.content_access(
            conn, {"id": row["created_by"], "roles": ["admin"]}, "assessment", assessment_id
        ),
        "reviewed": bool(row["settings"].get("authoring_reviewed_by")),
    }


def save_assessment(conn, actor, payload, assessment_id=None):
    scope(conn, payload.grade, payload.subject_id, payload.topic_id, lesson_id=payload.lesson_id)
    table, items, policies = (
        db.table("assessments"),
        db.table("assessment_items"),
        db.table("content_access_policies"),
    )
    before = None
    if assessment_id:
        before = (
            conn.execute(select(table).where(table.c.id == assessment_id).with_for_update())
            .mappings()
            .first()
        )
        if not before:
            raise HTTPException(404, "Không tìm thấy đề")
        if before["status"] != "draft":
            raise HTTPException(
                409, "Đề đã xuất bản/lưu trữ không được sửa. Hãy sao chép thành đề mới"
            )
        check_revision(before, payload.expected_revision)
        if payload.code != before["code"]:
            raise HTTPException(409, "Không đổi mã đề đã tạo")
    else:
        unique_code(conn, table, payload.code)
        assessment_id = uuid4()
    for item in payload.items:
        question = question_detail(conn, item.question_version_id)
        if (
            question["subject_id"] != payload.subject_id
            or question["grade"] != payload.grade
            or question["status"] == "archived"
        ):
            raise HTTPException(422, "Câu hỏi phải cùng môn/lớp và chưa lưu trữ")
    values = payload.model_dump(
        exclude={"items", "minimum_plan_code", "learning_level", "preview", "expected_revision"}
    )
    values.update(
        edit_revision=before["edit_revision"] + 1 if before else 1,
        updated_at=now(),
        settings={
            **(before["settings"] if before else {}),
            "authoring_reviewed_by": None,
            "authoring_reviewed_at": None,
        },
    )
    if before:
        conn.execute(table.update().where(table.c.id == assessment_id).values(**values))
        conn.execute(items.delete().where(items.c.assessment_id == assessment_id))
    else:
        conn.execute(
            table.insert().values(id=assessment_id, created_by=actor, status="draft", **values)
        )
    conn.execute(
        items.insert(),
        [
            {
                "assessment_id": assessment_id,
                "question_version_id": item.question_version_id,
                "position": index,
                "points": item.points,
            }
            for index, item in enumerate(payload.items, 1)
        ],
    )
    from sqlalchemy.dialects.postgresql import insert

    policy_values = dict(
        minimum_plan_code=payload.minimum_plan_code,
        learning_level=payload.learning_level,
        preview=payload.preview.model_dump(),
        updated_by=actor,
        updated_at=now(),
    )
    conn.execute(
        insert(policies)
        .values(assessment_id=assessment_id, **policy_values)
        .on_conflict_do_update(index_elements=[policies.c.assessment_id], set_=policy_values)
    )
    audit(
        conn,
        actor,
        "assessment.save",
        "assessment",
        assessment_id,
        before,
        {"code": payload.code, "item_count": len(payload.items), "plan": payload.minimum_plan_code},
    )
    return assessment_detail(conn, assessment_id)


def clone_assessment(conn, actor, identifier, code):
    original = assessment_detail(conn, identifier)
    payload = validate_stored(
        AssessmentInput,
        {
            **{
                key: original[key]
                for key in (
                    "grade",
                    "subject_id",
                    "topic_id",
                    "lesson_id",
                    "title",
                    "assessment_type",
                    "time_limit_seconds",
                    "max_attempts",
                    "minimum_plan_code",
                    "learning_level",
                    "preview",
                )
            },
            "code": code,
            "description": original["description"] or "",
            "items": [
                {
                    "question_version_id": item["question_version_id"],
                    "points": float(item["points"]),
                }
                for item in original["items"]
            ],
        },
    )
    # A clone may carry older immutable versions; select current versions in the new draft.
    versions = db.table("question_versions")
    for item in payload.items:
        question_id = question_detail(conn, item.question_version_id)["question_id"]
        current = conn.execute(
            select(versions.c.id).where(
                versions.c.question_id == question_id, versions.c.status == "published"
            )
        ).scalar()
        if current:
            item.question_version_id = current
    return save_assessment(conn, actor, payload)


def assessment_action(conn, actor, identifier, action, payload):
    table = db.table("assessments")
    row = (
        conn.execute(select(table).where(table.c.id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy đề")
    check_revision(row, payload.expected_revision)
    detail = assessment_detail(conn, identifier)
    at = now()
    if action in ("review", "publish"):
        if row["status"] != "draft":
            raise HTTPException(409, "Chỉ duyệt/xuất bản đề nháp")
        scope(conn, row["grade"], row["subject_id"], row["topic_id"], lesson_id=row["lesson_id"])
        if not detail["items"] or any(
            item["question"]["status"] != "published"
            or item["question"]["grade"] != row["grade"]
            or item["question"]["subject_id"] != row["subject_id"]
            for item in detail["items"]
        ):
            raise HTTPException(422, "Mọi câu trong đề phải được xuất bản và cùng môn/lớp")
        if (
            detail["effective_access"]["minimum_plan_code"] is None
            or detail["effective_access"]["minimum_plan_code"] != detail["minimum_plan_code"]
        ):
            raise HTTPException(
                422,
                "Đề chứa nội dung VIP hoặc thiếu quyền câu hỏi. Hãy kiểm tra và chọn gói phù hợp",
            )
        if action == "publish" and not detail["reviewed"]:
            raise HTTPException(409, "Hãy duyệt đề trước khi xuất bản")
        values = {
            "settings": {
                **row["settings"],
                "authoring_reviewed_by": str(actor),
                "authoring_reviewed_at": at.isoformat(),
            },
            "updated_at": at,
        }
        if action == "publish":
            values.update(status="published", published_at=at)
    else:
        attempts = db.table("attempts")
        if conn.execute(
            select(attempts.c.id)
            .where(attempts.c.assessment_id == identifier, attempts.c.status == "in_progress")
            .limit(1)
        ).first():
            raise HTTPException(409, "Có học sinh đang làm đề. Chưa thể lưu trữ")
        if row["status"] == "archived":
            raise HTTPException(409, "Đề đã lưu trữ")
        values = {"status": "archived", "updated_at": at}
    values["edit_revision"] = row["edit_revision"] + 1
    conn.execute(table.update().where(table.c.id == identifier).values(**values))
    audit(
        conn,
        actor,
        "assessment." + action,
        "assessment",
        identifier,
        row,
        {**values, "reason": payload.reason},
    )
    return assessment_detail(conn, identifier)


def assign_students(conn, actor, assessment_id, payload):
    profiles = {
        identifier: lock_student(conn, identifier)
        for identifier in sorted(payload.student_ids, key=str)
    }
    assessment = published_assessment(conn, assessment_id)
    at = now()
    available = payload.available_at or at
    if payload.due_at and payload.due_at <= max(available, at):
        raise HTTPException(422, "Hạn nộp phải sau giờ mở và thời điểm hiện tại")
    users, roles = db.table("users"), db.table("user_roles")
    active_ids = set(
        conn.execute(
            select(users.c.id)
            .join(roles)
            .where(
                users.c.id.in_(payload.student_ids),
                users.c.is_active.is_(True),
                roles.c.role == "student",
            )
        ).scalars()
    )
    if active_ids != set(payload.student_ids):
        raise HTTPException(422, "Học sinh phải có tài khoản đang hoạt động")
    table = db.table("student_assignments")
    result = []
    for identifier, profile in profiles.items():
        access.authorize_content(
            conn, access.student_actor(identifier), "assessment", assessment_id, assessment["grade"]
        )
        if profile["current_grade"] != assessment["grade"]:
            raise HTTPException(422, "Đề không cùng lớp học sinh")
        old = (
            conn.execute(
                select(table).where(
                    table.c.student_id == identifier,
                    table.c.assessment_id == assessment_id,
                    table.c.assigned_by == actor,
                    table.c.assignment_source == "system",
                    table.c.status.in_(["assigned", "in_progress"]),
                )
            )
            .mappings()
            .first()
        )
        if old:
            if old["due_at"] != payload.due_at or (
                payload.available_at and old["available_at"] != payload.available_at
            ):
                raise HTTPException(
                    409, "Đã có nhiệm vụ với lịch khác. Không thay đổi bài đang được giao"
                )
            result.append(dict(old))
            continue
        assignment = (
            conn.execute(
                table.insert()
                .values(
                    student_id=identifier,
                    assessment_id=assessment_id,
                    assigned_by=actor,
                    assignment_source="system",
                    available_at=available,
                    due_at=payload.due_at,
                )
                .returning(table)
            )
            .mappings()
            .one()
        )
        audit(
            conn,
            actor,
            "assignment.create",
            "student_assignment",
            assignment["id"],
            after={"student_id": str(identifier), "assessment_id": str(assessment_id)},
        )
        result.append(dict(assignment))
    return {"assignments": result, "count": len(result)}
