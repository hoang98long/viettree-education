import csv
from io import StringIO
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import Field
from sqlalchemy import func, select, text, update
from sqlalchemy.dialects.postgresql import insert

from app.academy.learning import audit, staff
from app.account_schemas import AdminAction
from app.core.security import admin_user, current_user, now
from app.db import connection, db
from app.schemas import StrictModel

router = APIRouter(prefix="/api/v1/ai-academy", tags=["ai-academy-management"])


class LessonAccessInput(AdminAction):
    minimum_plan_code: Literal["free", "vip"]
    revision: int = Field(ge=1)


@router.put("/admin/lessons/{identifier}/access")
def set_lesson_access(
    identifier: UUID, payload: LessonAccessInput, user=Depends(admin_user), conn=Depends(connection)
):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    table = db.table("ai_lessons")
    old = (
        conn.execute(select(table).where(table.c.id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if not old:
        raise HTTPException(404, "Không tìm thấy bài")
    if old["revision"] != payload.revision:
        raise HTTPException(409, "Bài đã thay đổi, tải lại trước khi đổi quyền")
    conn.execute(
        update(table)
        .where(table.c.id == identifier)
        .values(
            minimum_plan_code=payload.minimum_plan_code,
            revision=old["revision"] + 1,
            updated_at=now(),
        )
    )
    audit(
        conn,
        user["id"],
        "academy.access_policy_updated",
        identifier,
        {
            "from": old["minimum_plan_code"],
            "to": payload.minimum_plan_code,
            "reason": payload.reason,
        },
    )
    return {"minimum_plan_code": payload.minimum_plan_code, "revision": old["revision"] + 1}


@router.get("/admin/units")
def list_units(grade: int, user=Depends(current_user), conn=Depends(connection)):
    staff(conn, user, "read")
    table = db.table("ai_units")
    return [
        dict(r)
        for r in conn.execute(
            select(table).where(table.c.grade == grade).order_by(table.c.position)
        ).mappings()
    ]


@router.get("/admin/prompts")
def list_prompts(user=Depends(admin_user), conn=Depends(connection)):
    table = db.table("ai_prompt_templates")
    return [
        dict(r)
        for r in conn.execute(
            select(table).order_by(table.c.mode, table.c.version.desc())
        ).mappings()
    ]


class PromptDraft(StrictModel):
    mode: str = Field(
        pattern="^(ExplainConcept|GiveHint|AskSocraticQuestion|ReviewStudentDraft|PracticeEnglish|BrainstormStory|GenerateTeacherDraft|GenerateImagePrompt)$"
    )
    template: str = Field(min_length=30, max_length=3000)


@router.post("/admin/prompts")
def save_prompt(payload: PromptDraft, user=Depends(admin_user), conn=Depends(connection)):
    from app.academy.safety import moderation_reason

    if moderation_reason(payload.template):
        raise HTTPException(422, "Mẫu yêu cầu chứa nội dung không phù hợp")
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
        {"key": "ai-prompt:" + payload.mode},
    )
    table = db.table("ai_prompt_templates")
    version = conn.execute(
        select(func.coalesce(func.max(table.c.version), 0) + 1).where(table.c.mode == payload.mode)
    ).scalar_one()
    conn.execute(
        table.insert().values(
            mode=payload.mode, version=version, template=payload.template, status="draft"
        )
    )
    audit(
        conn, user["id"], "academy.prompt_draft", None, {"mode": payload.mode, "version": version}
    )
    return {"mode": payload.mode, "version": version, "status": "draft"}


@router.post("/admin/prompts/{mode}/{version}/approve")
def approve_prompt(
    mode: str,
    version: int,
    payload: AdminAction,
    user=Depends(admin_user),
    conn=Depends(connection),
):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"), {"key": "ai-prompt:" + mode}
    )
    table = db.table("ai_prompt_templates")
    row = (
        conn.execute(
            select(table).where(table.c.mode == mode, table.c.version == version).with_for_update()
        )
        .mappings()
        .first()
    )
    if not row or row["status"] != "draft":
        raise HTTPException(409, "Mẫu không còn là bản nháp")
    conn.execute(
        update(table)
        .where(table.c.mode == mode, table.c.status == "approved")
        .values(status="archived")
    )
    conn.execute(
        update(table)
        .where(table.c.mode == mode, table.c.version == version)
        .values(status="approved")
    )
    audit(conn, user["id"], "academy.prompt_approved", None, {"mode": mode, "version": version})
    return {"approved": True}


def child_access(conn, user, identifier):
    if "admin" in user["roles"] or user["id"] == identifier:
        return
    links = db.table("guardian_students")
    if (
        "guardian" not in user["roles"]
        or not conn.execute(
            select(links.c.student_id).where(
                links.c.guardian_user_id == user["id"],
                links.c.student_id == identifier,
                links.c.verified_at.is_not(None),
            )
        ).first()
    ):
        raise HTTPException(403, "Chưa có quyền dữ liệu của học sinh này")


@router.get("/privacy/{identifier}/export")
def export_own_data(identifier: UUID, user=Depends(current_user), conn=Depends(connection)):
    child_access(conn, user, identifier)
    output = {}
    for name in [
        "ai_progress",
        "ai_attempts",
        "ai_project_submissions",
        "ai_student_badges",
        "ai_competency_progress",
    ]:
        table = db.table(name)
        output[name] = [
            dict(r)
            for r in conn.execute(select(table).where(table.c.student_id == identifier)).mappings()
        ]
    audit(conn, user["id"], "academy.data_exported", identifier)
    return output


class RemovalRequest(StrictModel):
    student_id: UUID


@router.post("/privacy/project-text-removal")
def request_removal(payload: RemovalRequest, user=Depends(current_user), conn=Depends(connection)):
    child_access(conn, user, payload.student_id)
    audit(
        conn,
        user["id"],
        "academy.project_text_removal_requested",
        payload.student_id,
        {"state": "pending", "scope": "project_text"},
    )
    return {
        "requested": True,
        "scope": "project_text",
        "message": "Nhà trường xem xét yêu cầu gỡ phần nội dung tự viết; hồ sơ học tập/audit tối thiểu được giữ theo chính sách.",
    }


@router.get("/admin/privacy-requests")
def privacy_requests(user=Depends(admin_user), conn=Depends(connection)):
    table = db.table("ai_audit_logs")
    return [
        dict(r)
        for r in conn.execute(
            select(table)
            .where(table.c.action == "academy.project_text_removal_requested")
            .order_by(table.c.created_at.desc())
            .limit(100)
        ).mappings()
    ]


class RemovalApproval(AdminAction):
    approved: bool


@router.post("/admin/privacy-requests/{identifier}/resolve")
def resolve_removal(
    identifier: UUID, payload: RemovalApproval, user=Depends(admin_user), conn=Depends(connection)
):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    requests = db.table("ai_audit_logs")
    request = (
        conn.execute(
            select(requests)
            .where(
                requests.c.id == identifier,
                requests.c.action == "academy.project_text_removal_requested",
            )
            .with_for_update()
        )
        .mappings()
        .first()
    )
    if not request or request["metadata"].get("state") != "pending":
        raise HTTPException(409, "Yêu cầu không còn chờ xử lý")
    if payload.approved:
        table = db.table("ai_project_submissions")
        conn.execute(
            update(table)
            .where(table.c.student_id == request["entity_id"])
            .values(artifact={}, feedback=None, revision=table.c.revision + 1, updated_at=now())
        )
    conn.execute(
        update(requests)
        .where(requests.c.id == identifier)
        .values(
            metadata={
                **request["metadata"],
                "state": "approved" if payload.approved else "rejected",
            }
        )
    )
    audit(
        conn,
        user["id"],
        "academy.project_text_removal_resolved",
        request["entity_id"],
        {"approved": payload.approved},
    )
    return {"approved": payload.approved, "scope": "project_text"}


class GuardianLink(AdminAction):
    guardian_id: UUID
    student_id: UUID
    verified: bool


@router.post("/admin/guardian-links")
def link_guardian(payload: GuardianLink, user=Depends(admin_user), conn=Depends(connection)):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    roles, users = db.table("user_roles"), db.table("users")
    for identifier, role in [(payload.guardian_id, "guardian"), (payload.student_id, "student")]:
        if not conn.execute(
            select(users.c.id)
            .join(roles)
            .where(users.c.id == identifier, users.c.is_active.is_(True), roles.c.role == role)
        ).first():
            raise HTTPException(422, "Chọn phụ huynh và học sinh đang hoạt động")
    table = db.table("guardian_students")
    conn.execute(
        insert(table)
        .values(
            guardian_user_id=payload.guardian_id,
            student_id=payload.student_id,
            verified_at=now() if payload.verified else None,
        )
        .on_conflict_do_update(
            index_elements=[table.c.guardian_user_id, table.c.student_id],
            set_={"verified_at": now() if payload.verified else None},
        )
    )
    audit(
        conn,
        user["id"],
        "academy.guardian_link",
        payload.student_id,
        {"verified": payload.verified},
    )
    return {"verified": payload.verified}


@router.get("/teacher/reports/export")
def export_csv(class_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    from app.academy.api import reports

    data = reports(class_id, user, conn)
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Học sinh", "Bài đã hoàn thành"])
    for row in data["students"]:
        name = row["display_name"]
        if name.lstrip().startswith(("=", "+", "-", "@")):
            name = "'" + name
        writer.writerow([name, row["completed"]])
    return Response(
        "\ufeff" + stream.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="ai-academy-class.csv"'},
    )


@router.post("/admin/lessons/{identifier}/teacher-draft")
def teacher_draft(identifier: UUID, user=Depends(current_user), conn=Depends(connection)):
    import httpx

    from app.academy.learning import lesson_row
    from app.academy.providers import OllamaProvider, SimulationProvider
    from app.academy.safety import moderation_reason
    from app.academy.tutor import flags, reserve_quota
    from app.core.config import settings

    staff(conn, user)
    row = lesson_row(conn, identifier)
    versions = db.table("ai_lesson_versions")
    data = conn.execute(
        select(versions.c.payload).where(
            versions.c.lesson_id == identifier, versions.c.status == "published"
        )
    ).scalar()
    if not data:
        raise HTTPException(422, "Chỉ lấy ngữ liệu từ bài đã được xuất bản")
    context = {
        "grade": row["grade"],
        "mode": "GenerateTeacherDraft",
        "approved_lesson": data["steps"][1]["text"],
        "approved_hint": "Mở đầu bằng tranh: "
        + data["steps"][0]["text"]
        + " Tổ chức: "
        + data["teacher_guide"]
        + " Hỗ trợ: "
        + data["support"]
        + " Mở rộng: "
        + data["advanced"],
    }
    template = "Đề xuất giáo án ngắn từ ngữ liệu đã duyệt. Không thêm dữ liệu cá nhân hoặc căn cứ không có trong bài. Nội dung cần giáo viên kiểm tra trước khi xuất bản."
    templates = db.table("ai_prompt_templates")
    template = (
        conn.execute(
            select(templates.c.template)
            .where(templates.c.mode == "GenerateTeacherDraft", templates.c.status == "approved")
            .order_by(templates.c.version.desc())
            .limit(1)
        ).scalar()
        or template
    )
    response = SimulationProvider().generate(context, template)
    mode = "simulation"
    provider = db.table("ai_provider_configs")
    ready = conn.execute(
        select(provider.c.code).where(
            provider.c.code == "ollama",
            provider.c.enabled.is_(True),
            provider.c.policy_approved.is_(True),
        )
    ).first()
    if (
        not settings().ai_training_only
        and flags(conn).get("tutor_enabled")
        and ready
        and settings().ai_provider == "ollama"
    ):
        reserve_quota(conn, user["id"])
        try:
            generated = OllamaProvider().generate(context, template)
            if (
                not isinstance(generated, str)
                or not 30 <= len(generated) <= 3000
                or moderation_reason(generated)
            ):
                raise ValueError("Not approved")
            response, mode = generated, "ollama"
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            mode = "fallback"
    audit(conn, user["id"], "academy.teacher_guidance", identifier, {"mode": mode})
    return {
        "mode": mode,
        "teacher_guide": response,
        "notice": "Đề xuất riêng, cần người biên soạn kiểm tra, lưu nháp và duyệt trước khi xuất bản.",
    }
