from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import func, select, text, update

from app.academy.learning import audit, staff
from app.core.security import now
from app.db import db


def save_draft(conn, user, payload, identifier=None):
    staff(conn, user)
    lessons, units, versions = (
        db.table(n) for n in ("ai_lessons", "ai_units", "ai_lesson_versions")
    )
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
        {"key": "ai-lesson-code:" + payload.code},
    )
    if not conn.execute(select(units.c.id).where(units.c.id == payload.unit_id)).first():
        raise HTTPException(422, "Chủ đề không tồn tại")
    if identifier:
        existing = (
            conn.execute(select(lessons).where(lessons.c.id == identifier).with_for_update())
            .mappings()
            .first()
        )
        if not existing:
            raise HTTPException(404, "Không tìm thấy bài")
        if payload.revision != existing["revision"]:
            raise HTTPException(409, "Bài đã được sửa, hãy tải lại trước khi lưu")
        if payload.code != existing["code"] or payload.unit_id != existing["unit_id"]:
            raise HTTPException(422, "Tạo bài mới khi cần đổi mã/chủ đề; giữ quan hệ lịch sử cũ")
    else:
        if conn.execute(select(lessons.c.id).where(lessons.c.code == payload.code)).first():
            raise HTTPException(409, "Mã bài đã tồn tại")
        identifier = uuid4()
        conn.execute(
            lessons.insert().values(
                id=identifier,
                unit_id=payload.unit_id,
                code=payload.code,
                title=payload.title,
                position=payload.position,
                created_by=user["id"],
            )
        )
    conflict = conn.execute(
        select(lessons.c.id).where(
            lessons.c.unit_id == payload.unit_id,
            lessons.c.position == payload.position,
            lessons.c.id != identifier,
        )
    ).first()
    if conflict:
        raise HTTPException(409, "Thứ tự này đã có bài; chọn vị trí khác")
    number = conn.execute(
        select(func.coalesce(func.max(versions.c.version), 0) + 1).where(
            versions.c.lesson_id == identifier
        )
    ).scalar_one()
    version_id = uuid4()
    conn.execute(
        versions.insert().values(
            id=version_id,
            lesson_id=identifier,
            version=number,
            status="draft",
            payload={
                **payload.content.model_dump(),
                "title_override": payload.title,
                "position_override": payload.position,
            },
            created_by=user["id"],
        )
    )
    revision = conn.execute(
        update(lessons)
        .where(lessons.c.id == identifier)
        .values(revision=lessons.c.revision + 1, updated_at=now())
        .returning(lessons.c.revision)
    ).scalar_one()
    # Published metadata stays stable until publish; draft metadata lives with its audit.
    audit(
        conn,
        user["id"],
        "academy.draft_saved",
        identifier,
        {"version": number, "title": payload.title, "position": payload.position},
    )
    return {"id": identifier, "version_id": version_id, "revision": revision}


def workflow(conn, user, identifier, action, revision):
    staff(conn, user, "reviewer" if action in {"review", "publish", "archive"} else "editor")
    lessons, versions, media, usages = (
        db.table(n)
        for n in ("ai_lessons", "ai_lesson_versions", "ai_media_assets", "ai_media_usages")
    )
    row = (
        conn.execute(select(lessons).where(lessons.c.id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài")
    if row["revision"] != revision:
        raise HTTPException(409, "Bản đã thay đổi, tải lại trước khi duyệt")
    version = (
        conn.execute(
            select(versions)
            .where(
                versions.c.lesson_id == identifier,
                *([versions.c.status == "published"] if action == "archive" else []),
            )
            .order_by(versions.c.version.desc())
            .limit(1)
        )
        .mappings()
        .first()
    )
    if not version:
        raise HTTPException(409, "Không có phiên bản phù hợp để xử lý")
    expected = {"submit": "draft", "review": "review", "publish": "review", "archive": "published"}[
        action
    ]
    if version["status"] != expected or (action == "publish" and not version["reviewed_by"]):
        raise HTTPException(409, "Cần lưu nháp, gửi duyệt và duyệt trước khi xuất bản")
    data = version["payload"]
    codes = {
        data["hero"],
        *data["cards"],
        *[code for step in data["steps"] for code in step["media"]],
        *[
            item["asset"]
            for step in data["steps"]
            if step.get("activity")
            for item in step["activity"]["items"]
            if item.get("asset")
        ],
    }
    assets = list(
        conn.execute(
            select(media).where(media.c.code.in_(codes)).order_by(media.c.id).with_for_update()
        ).mappings()
    )
    if action in {"review", "publish"} and (
        len(assets) != len(codes) or any(a["status"] != "approved" for a in assets)
    ):
        raise HTTPException(422, "Cần đủ media được duyệt, có alt và giấy phép")
    values = {
        "status": {
            "submit": "review",
            "review": "review",
            "publish": "published",
            "archive": "archived",
        }[action]
    }
    if action == "review":
        values["reviewed_by"] = user["id"]
    if action == "publish":
        if (
            data.get("position_override")
            and conn.execute(
                select(lessons.c.id).where(
                    lessons.c.unit_id == row["unit_id"],
                    lessons.c.position == data["position_override"],
                    lessons.c.id != identifier,
                )
            ).first()
        ):
            raise HTTPException(409, "Vị trí bài đã được sử dụng")
        conn.execute(
            update(lessons)
            .where(lessons.c.id == identifier)
            .values(
                title=data.get("title_override") or row["title"],
                position=data.get("position_override") or row["position"],
            )
        )
        conn.execute(
            update(versions)
            .where(versions.c.lesson_id == identifier, versions.c.status == "published")
            .values(status="archived")
        )
        values["published_at"] = now()
        from sqlalchemy.dialects.postgresql import insert

        for asset in assets:
            conn.execute(
                insert(usages)
                .values(lesson_version_id=version["id"], asset_id=asset["id"], purpose="lesson")
                .on_conflict_do_nothing()
            )
    conn.execute(update(versions).where(versions.c.id == version["id"]).values(**values))
    conn.execute(
        update(lessons)
        .where(lessons.c.id == identifier)
        .values(revision=row["revision"] + 1, updated_at=now())
    )
    conn.execute(
        db.table("ai_content_approvals")
        .insert()
        .values(version_id=version["id"], actor_id=user["id"], action=action)
    )
    audit(conn, user["id"], "academy." + action, identifier, {"version": version["version"]})
    return {"revision": row["revision"] + 1, "status": values["status"]}


def class_access(conn, user, identifier):
    classes = db.table("classes")
    row = (
        conn.execute(
            select(classes).where(classes.c.id == identifier, classes.c.is_active.is_(True))
        )
        .mappings()
        .first()
    )
    if not row or (
        "admin" not in user["roles"]
        and ("teacher" not in user["roles"] or row["teacher_user_id"] != user["id"])
    ):
        raise HTTPException(403, "Chưa được phân công quản lý lớp này")
    return row


def review_submission(conn, user, identifier, payload):
    table = db.table("ai_project_submissions")
    row = (
        conn.execute(select(table).where(table.c.id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if not row or row["class_id"] is None:
        raise HTTPException(404, "Bài chưa gửi tới lớp")
    class_access(conn, user, row["class_id"])
    enrollments = db.table("class_enrollments")
    if not conn.execute(
        select(enrollments.c.student_id).where(
            enrollments.c.class_id == row["class_id"],
            enrollments.c.student_id == row["student_id"],
            enrollments.c.left_at.is_(None),
        )
    ).first():
        raise HTTPException(403, "Học sinh không còn ghi danh ở lớp được phân công")
    if row["revision"] != payload.revision or row["status"] not in {"submitted", "reviewed"}:
        raise HTTPException(409, "Bài chưa nộp hoặc đã được cập nhật")
    project = db.table("ai_projects")
    rubric = conn.execute(
        select(project.c.rubric).where(project.c.id == row["project_id"])
    ).scalar_one()
    total = sum(payload.scores[key] * rubric[key] / 4 for key in rubric)
    from sqlalchemy.dialects.postgresql import insert

    scores = db.table("ai_rubric_scores")
    conn.execute(
        insert(scores)
        .values(
            submission_id=identifier, scores=payload.scores, total=total, reviewer_id=user["id"]
        )
        .on_conflict_do_update(
            index_elements=[scores.c.submission_id],
            set_={
                "scores": payload.scores,
                "total": total,
                "reviewer_id": user["id"],
                "updated_at": now(),
            },
        )
    )
    conn.execute(
        update(table)
        .where(table.c.id == identifier)
        .values(
            status="reviewed",
            feedback=payload.feedback,
            reviewed_by=user["id"],
            revision=row["revision"] + 1,
            updated_at=now(),
        )
    )
    audit(conn, user["id"], "academy.project_reviewed", identifier, {"total": total})
    return {"total": total, "revision": row["revision"] + 1}
