from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse
from pydantic import Field
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.dialects.postgresql import insert

from app.academy import cms, learning, tutor
from app.academy.access import media_access, student_feature
from app.academy.media import ASSETS
from app.academy.safety import moderation_reason
from app.academy.schemas import (
    AssignmentInput,
    AttemptInput,
    DraftInput,
    ReviewInput,
    RevisionInput,
    StepInput,
    SubmissionInput,
    TutorInput,
)
from app.account_schemas import AdminAction
from app.core.config import settings
from app.core.security import _throttle, admin_user, current_user, now, student_user
from app.db import connection, db
from app.schemas import StrictModel

router = APIRouter(prefix="/api/v1/ai-academy", tags=["ai-academy"])


@router.get("/home")
def home(user=Depends(student_user), conn=Depends(connection)):
    profiles, progress, ledger = (
        db.table(n) for n in ("student_profiles", "ai_progress", "ai_rewards_ledger")
    )
    grade = conn.execute(
        select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
    ).scalar_one()
    assignments, targets, classrooms, enrollments, lessons, units, versions = (
        db.table(name)
        for name in (
            "ai_assignments",
            "ai_assignment_targets",
            "classes",
            "class_enrollments",
            "ai_lessons",
            "ai_units",
            "ai_lesson_versions",
        )
    )
    assigned = list(
        conn.execute(
            select(
                assignments.c.id,
                lessons.c.id.label("lesson_id"),
                lessons.c.title,
                classrooms.c.name.label("class_name"),
                assignments.c.due_at,
                progress.c.completed_at,
            )
            .select_from(
                assignments.join(targets, targets.c.assignment_id == assignments.c.id)
                .join(classrooms, classrooms.c.id == assignments.c.class_id)
                .join(enrollments, enrollments.c.class_id == classrooms.c.id)
                .join(lessons, lessons.c.id == assignments.c.lesson_id)
                .join(units, units.c.id == lessons.c.unit_id)
                .outerjoin(
                    progress,
                    (progress.c.student_id == user["id"]) & (progress.c.lesson_id == lessons.c.id),
                )
            )
            .where(
                targets.c.student_id == user["id"],
                enrollments.c.student_id == user["id"],
                enrollments.c.left_at.is_(None),
                classrooms.c.is_active.is_(True),
                units.c.grade <= grade,
                select(versions.c.id)
                .where(versions.c.lesson_id == lessons.c.id, versions.c.status == "published")
                .exists(),
            )
            .order_by(assignments.c.created_at.desc())
            .limit(50)
        ).mappings()
    )
    batches, batch_targets = (
        db.table("learning_assignment_batches"),
        db.table("learning_assignment_targets"),
    )
    assigned.extend(
        conn.execute(
            select(
                batches.c.id,
                lessons.c.id.label("lesson_id"),
                lessons.c.title,
                func.coalesce(classrooms.c.name, "Bài giao riêng").label("class_name"),
                batches.c.due_at,
                progress.c.completed_at,
            )
            .select_from(
                batches.join(batch_targets, batch_targets.c.batch_id == batches.c.id)
                .join(lessons, lessons.c.id == batches.c.resource_id)
                .join(units, units.c.id == lessons.c.unit_id)
                .outerjoin(classrooms, classrooms.c.id == batches.c.class_id)
                .outerjoin(
                    enrollments,
                    and_(
                        enrollments.c.class_id == batches.c.class_id,
                        enrollments.c.student_id == user["id"],
                        enrollments.c.left_at.is_(None),
                    ),
                )
                .outerjoin(
                    progress,
                    (progress.c.student_id == user["id"]) & (progress.c.lesson_id == lessons.c.id),
                )
            )
            .where(
                batches.c.kind == "ai_lesson",
                batch_targets.c.student_id == user["id"],
                units.c.grade <= grade,
                or_(
                    batches.c.class_id.is_(None),
                    and_(classrooms.c.is_active.is_(True), enrollments.c.student_id.is_not(None)),
                ),
                select(versions.c.id)
                .where(versions.c.lesson_id == lessons.c.id, versions.c.status == "published")
                .exists(),
            )
            .order_by(batches.c.created_at.desc())
            .limit(50)
        )
        .mappings()
        .all()
    )
    return {
        "assignments": [dict(row) for row in assigned],
        "grade": grade,
        "catalog": learning.catalog(conn, grade, user["id"]),
        "points": conn.execute(
            select(func.coalesce(func.sum(ledger.c.points), 0)).where(
                ledger.c.student_id == user["id"]
            )
        ).scalar_one(),
        "completed": conn.execute(
            select(func.count())
            .select_from(progress)
            .where(progress.c.student_id == user["id"], progress.c.completed_at.is_not(None))
        ).scalar_one(),
        "mode": "simulation",
        "flags": tutor.flags(conn),
    }


@router.get("/grades")
def grades(user=Depends(current_user), conn=Depends(connection)):
    return [
        dict(r)
        for r in conn.execute(
            select(db.table("ai_grades")).order_by(db.table("ai_grades").c.grade)
        ).mappings()
    ]


@router.get("/catalog")
def catalog(
    grade: int = Query(4, ge=1, le=5), user=Depends(current_user), conn=Depends(connection)
):
    return learning.catalog(conn, grade, user["id"] if "student" in user["roles"] else None)


@router.post("/lessons/{identifier}/start")
def start(identifier: UUID, user=Depends(student_user), conn=Depends(connection)):
    row, progress, payload = learning.start(conn, user, identifier)
    attempts = db.table("ai_attempts")
    passed = list(
        conn.execute(
            select(attempts.c.step_id)
            .where(
                attempts.c.student_id == user["id"],
                attempts.c.version_id == progress["version_id"],
                attempts.c.score >= 0.7,
            )
            .distinct()
        ).scalars()
    )
    return {
        "lesson": row,
        "progress": progress,
        "content": learning.public_content(payload),
        "passed_steps": passed,
        "flags": tutor.flags(conn),
    }


@router.post("/lessons/{identifier}/steps")
def step(
    identifier: UUID, payload: StepInput, user=Depends(student_user), conn=Depends(connection)
):
    return learning.complete_step(conn, user, identifier, payload.step_id)


@router.post("/lessons/{identifier}/attempts")
def attempt(
    identifier: UUID, payload: AttemptInput, user=Depends(student_user), conn=Depends(connection)
):
    if _throttle("academy-attempt:" + str(user["id"]), 60):
        raise HTTPException(429, "Em nghỉ một chút rồi thử tiếp nhé", headers={"Retry-After": "60"})
    result = learning.attempt(conn, user, identifier, payload)
    return {key: result[key] for key in ["id", "score", "feedback", "level", "created_at"]}


@router.get("/portfolio")
def portfolio(user=Depends(student_user), conn=Depends(connection)):
    badges, earned = (db.table(n) for n in ("ai_badges", "ai_student_badges"))
    return {
        "badges": [
            dict(r)
            for r in conn.execute(
                select(badges, badges.c.code.label("badge_code"), earned.c.earned_at)
                .join(earned)
                .where(earned.c.student_id == user["id"])
            ).mappings()
        ],
        "submissions": [
            dict(r)
            for r in conn.execute(
                select(db.table("ai_project_submissions"))
                .where(db.table("ai_project_submissions").c.student_id == user["id"])
                .order_by(db.table("ai_project_submissions").c.updated_at.desc())
            ).mappings()
        ],
        "competencies": [
            dict(r)
            for r in conn.execute(
                select(db.table("ai_competency_progress")).where(
                    db.table("ai_competency_progress").c.student_id == user["id"]
                )
            ).mappings()
        ],
    }


@router.get("/projects")
def projects(user=Depends(student_user), conn=Depends(connection)):
    student_feature(conn, user, "academy.studio")
    profile = db.table("student_profiles")
    grade = conn.execute(
        select(profile.c.current_grade).where(profile.c.student_id == user["id"])
    ).scalar_one()
    return [
        dict(r)
        for r in conn.execute(
            select(db.table("ai_projects")).where(db.table("ai_projects").c.grade == grade)
        ).mappings()
    ]


@router.post("/projects/submissions")
def submission(payload: SubmissionInput, user=Depends(student_user), conn=Depends(connection)):
    student_feature(conn, user, "academy.studio")
    if not tutor.flags(conn).get("student_creative_enabled"):
        raise HTTPException(403, "Xưởng sáng tạo đang tạm đóng")
    project = db.table("ai_projects")
    profile = db.table("student_profiles")
    grade = conn.execute(
        select(profile.c.current_grade).where(profile.c.student_id == user["id"]).with_for_update()
    ).scalar_one()
    row = (
        conn.execute(
            select(project).where(project.c.id == payload.project_id, project.c.grade == grade)
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy dự án của lớp em")
    reason = moderation_reason(" ".join(payload.artifact.values()))
    if reason:
        # Record only the reason; never store the unsafe original text.
        conn.execute(
            db.table("ai_moderation_reviews")
            .insert()
            .values(student_id=user["id"], reason_code=reason)
        )
        return {
            "blocked": True,
            "message": "Dùng nhân vật và dữ liệu mẫu; không nhập thông tin riêng hoặc nội dung nguy hiểm.",
        }
    if payload.class_id:
        classes, enrollments = (db.table(n) for n in ("classes", "class_enrollments"))
        if not conn.execute(
            select(classes.c.id)
            .join(enrollments)
            .where(
                classes.c.id == payload.class_id,
                classes.c.is_active.is_(True),
                classes.c.grade == grade,
                enrollments.c.student_id == user["id"],
                enrollments.c.left_at.is_(None),
            )
        ).first():
            raise HTTPException(403, "Em chưa thuộc lớp này")
    if payload.submit and (
        not payload.class_id
        or len(payload.artifact.get("title", "").strip()) < 3
        or not payload.artifact.get("reflection", "").strip()
    ):
        raise HTTPException(
            422, "Cần lớp được ghi danh, tên sản phẩm và lời tự đánh giá trước khi nộp"
        )
    table = db.table("ai_project_submissions")
    old = (
        conn.execute(
            select(table)
            .where(table.c.project_id == payload.project_id, table.c.student_id == user["id"])
            .with_for_update()
        )
        .mappings()
        .first()
    )
    values = dict(
        artifact=payload.artifact,
        class_id=payload.class_id,
        status="submitted" if payload.submit else "draft",
        updated_at=now(),
    )
    if old:
        if old["revision"] != payload.revision:
            raise HTTPException(
                409, "Sản phẩm đã được cập nhật ở nơi khác; tải lại để giữ phần sửa"
            )
        values.update(revision=old["revision"] + 1, feedback=None, reviewed_by=None)
        result = (
            conn.execute(
                update(table).where(table.c.id == old["id"]).values(**values).returning(table)
            )
            .mappings()
            .one()
        )
    else:
        result = (
            conn.execute(
                table.insert()
                .values(student_id=user["id"], project_id=payload.project_id, **values)
                .returning(table)
            )
            .mappings()
            .one()
        )
    if payload.submit:
        learning.event(conn, user["id"], None, "project_submitted")
    return dict(result)


@router.post("/tutor")
def ai_tutor(payload: TutorInput, user=Depends(student_user), conn=Depends(connection)):
    return tutor.respond(conn, user, payload)


@router.get("/media")
def media(
    page: int = Query(1, ge=1),
    category: str = "",
    user=Depends(current_user),
    conn=Depends(connection),
):
    table = db.table("ai_media_assets")
    query = select(table).where(table.c.status == "approved")
    if category:
        query = query.where(table.c.category == category)
    return [
        dict(r)
        for r in conn.execute(
            query.order_by(table.c.code).offset((page - 1) * 60).limit(60)
        ).mappings()
    ]


@router.get("/media/{code}")
def media_file(
    code: str,
    request: Request,
    variant: str = Query("original", pattern="^(original|responsive|thumbnail)$"),
    user=Depends(current_user),
    conn=Depends(connection),
):
    media, variants = (db.table(n) for n in ("ai_media_assets", "ai_media_variants"))
    row = (
        conn.execute(
            select(media, variants.c.object_key, variants.c.mime_type, variants.c.sha256)
            .join(variants)
            .where(media.c.code == code, variants.c.kind == variant)
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Hình chưa sẵn sàng")
    if row["status"] != "approved" and "admin" not in user["roles"]:
        learning.staff(conn, user, "read")
    media_access(conn, user, row)
    root = ASSETS if row["bundled"] else settings().ai_media_root
    path = (root / row["object_key"]).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise HTTPException(404, "Không tìm thấy hình")
    cache_allowed = row["bundled"] and row["category"] in {
        "hero",
        "cover",
        "mascot",
        "card",
        "badge",
        "ui",
    }
    if cache_allowed:
        request.state.academy_asset_cache = True
    return FileResponse(
        path,
        media_type=row["mime_type"],
        headers={
            "ETag": '"' + row["sha256"] + '"',
            "Cache-Control": "private, max-age=300" if cache_allowed else "no-store",
            "Vary": "Cookie",
        },
    )


class LabInput(StrictModel):
    training_ids: list[str] = Field(min_length=1, max_length=16)
    test_ids: list[str] = Field(min_length=1, max_length=8)
    features: list[int] = Field(default_factory=lambda: [0, 1, 2, 3], min_length=1, max_length=5)


@router.get("/lab")
def lab(user=Depends(student_user), conn=Depends(connection)):
    student_feature(conn, user, "academy.lab")
    from app.academy.games import DATASET

    return {
        "mode": "simulation",
        "algorithm": "So khớp đặc điểm và bỏ phiếu nhãn gần nhất",
        "samples": DATASET,
    }


@router.post("/lab")
def lab_try(payload: LabInput, user=Depends(student_user), conn=Depends(connection)):
    student_feature(conn, user, "academy.lab")
    from app.academy.games import predict

    try:
        result = predict(payload.training_ids, payload.test_ids, tuple(payload.features))
    except ValueError:
        raise HTTPException(422, "Chọn tập học/tập thử khác nhau và đặc điểm hợp lệ") from None
    learning.event(
        conn,
        user["id"],
        None,
        "activity_attempted",
        {"kind": "lab", "accuracy": sum(r["correct"] for r in result) / len(result)},
    )
    return {"mode": "simulation", "results": result}


@router.get("/classes")
def own_classes(user=Depends(current_user), conn=Depends(connection)):
    classes, enrollments = (db.table(n) for n in ("classes", "class_enrollments"))
    query = select(classes).where(classes.c.is_active.is_(True))
    if "admin" not in user["roles"]:
        query = (
            query.where(classes.c.teacher_user_id == user["id"])
            if "teacher" in user["roles"]
            else query.join(enrollments).where(
                enrollments.c.student_id == user["id"], enrollments.c.left_at.is_(None)
            )
        )
    return [dict(r) for r in conn.execute(query.order_by(classes.c.name)).mappings()]


@router.post("/teacher/assignments")
def assign(payload: AssignmentInput, user=Depends(current_user), conn=Depends(connection)):
    from app.classroom.service import class_scope, validate_student

    classroom = class_scope(conn, user, payload.class_id, staff_only=True, lock=True)
    if not classroom["is_active"]:
        raise HTTPException(409, "Lớp đã đóng")
    lesson = learning.lesson_row(conn, payload.lesson_id)
    if lesson["grade"] != classroom["grade"]:
        raise HTTPException(422, "Bài phải phù hợp lớp được giao")
    versions = db.table("ai_lesson_versions")
    if not conn.execute(
        select(versions.c.id).where(
            versions.c.lesson_id == payload.lesson_id, versions.c.status == "published"
        )
    ).first():
        raise HTTPException(422, "Chỉ giao bài đã xuất bản")
    assignments, targets, enrollments = (
        db.table(n) for n in ("ai_assignments", "ai_assignment_targets", "class_enrollments")
    )
    result = conn.execute(
        insert(assignments)
        .values(class_id=payload.class_id, lesson_id=payload.lesson_id, assigned_by=user["id"])
        .on_conflict_do_nothing()
        .returning(assignments.c.id)
    ).scalar()
    if not result:
        result = conn.execute(
            select(assignments.c.id).where(
                assignments.c.class_id == payload.class_id,
                assignments.c.lesson_id == payload.lesson_id,
            )
        ).scalar_one()
    students = list(
        conn.execute(
            select(enrollments.c.student_id).where(
                enrollments.c.class_id == payload.class_id, enrollments.c.left_at.is_(None)
            )
        ).scalars()
    )
    for identifier in students:
        validate_student(conn, identifier, classroom)
        learning.allowed_lesson(conn, {"id": identifier, "roles": ["student"]}, payload.lesson_id)
    for identifier in students:
        conn.execute(
            insert(targets)
            .values(assignment_id=result, student_id=identifier)
            .on_conflict_do_nothing()
        )
    learning.audit(conn, user["id"], "academy.assigned", result, {"targets": len(students)})
    return {"id": result, "targets": len(students)}


@router.get("/teacher/reports")
def reports(class_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    cms.class_access(conn, user, class_id)
    enrollments, users, progress, submissions = (
        db.table(n) for n in ("class_enrollments", "users", "ai_progress", "ai_project_submissions")
    )
    students = list(
        conn.execute(
            select(users.c.id, users.c.display_name)
            .select_from(users.join(enrollments, users.c.id == enrollments.c.student_id))
            .where(enrollments.c.class_id == class_id, enrollments.c.left_at.is_(None))
        ).mappings()
    )
    ids = [r["id"] for r in students]
    counts = {
        r.student_id: r.total
        for r in conn.execute(
            select(progress.c.student_id, func.count().label("total"))
            .where(progress.c.student_id.in_(ids), progress.c.completed_at.is_not(None))
            .group_by(progress.c.student_id)
        )
    }
    return {
        "students": [dict(r, completed=counts.get(r["id"], 0)) for r in students],
        "submissions": [
            dict(r)
            for r in conn.execute(
                select(submissions).where(
                    submissions.c.class_id == class_id,
                    submissions.c.student_id.in_(ids),
                    submissions.c.status.in_(["submitted", "reviewed"]),
                )
            ).mappings()
        ],
    }


@router.post("/teacher/submissions/{identifier}/review")
def review_submission(
    identifier: UUID, payload: ReviewInput, user=Depends(current_user), conn=Depends(connection)
):
    if moderation_reason(payload.feedback):
        raise HTTPException(422, "Nhận xét cần dùng nội dung học, không có thông tin riêng")
    return cms.review_submission(conn, user, identifier, payload)


@router.get("/guardian")
def guardian(user=Depends(current_user), conn=Depends(connection)):
    if "guardian" not in user["roles"]:
        raise HTTPException(403, "Trang dành cho phụ huynh đã liên kết")
    links, users, profiles = (
        db.table(n) for n in ("guardian_students", "users", "student_profiles")
    )
    rows = conn.execute(
        select(users.c.id, users.c.display_name, profiles.c.current_grade)
        .join(profiles, profiles.c.student_id == users.c.id)
        .join(links, links.c.student_id == users.c.id)
        .where(links.c.guardian_user_id == user["id"], links.c.verified_at.is_not(None))
    ).mappings()
    return [
        dict(
            r,
            lessons=learning.catalog(conn, r["current_grade"], r["id"]),
            consent=tutor.consent(conn, r["id"]),
        )
        for r in rows
    ]


class ConsentInput(StrictModel):
    student_id: UUID
    given: bool


@router.post("/guardian/consent")
def record_consent(payload: ConsentInput, user=Depends(current_user), conn=Depends(connection)):
    links = db.table("guardian_students")
    if (
        "guardian" not in user["roles"]
        or not conn.execute(
            select(links.c.student_id).where(
                links.c.student_id == payload.student_id,
                links.c.guardian_user_id == user["id"],
                links.c.verified_at.is_not(None),
            )
        ).first()
    ):
        raise HTTPException(403, "Chưa có liên kết phụ huynh được xác minh")
    conn.execute(
        db.table("privacy_consents")
        .insert()
        .values(
            student_id=payload.student_id,
            guardian_user_id=user["id"],
            purpose_code="ai_academy_provider",
            policy_version=tutor.POLICY,
            consent_given=payload.given,
        )
    )
    learning.audit(
        conn,
        user["id"],
        "academy.consent",
        payload.student_id,
        {"given": payload.given, "policy": tutor.POLICY},
    )
    return {"given": payload.given}


@router.get("/admin/overview")
def overview(user=Depends(current_user), conn=Depends(connection)):
    from app.academy.quality import report

    learning.staff(conn, user, "read")
    tables = [
        "ai_lessons",
        "ai_media_assets",
        "ai_attempts",
        "ai_progress",
        "ai_project_submissions",
        "ai_moderation_reviews",
    ]
    return {
        "quality": report(conn),
        "training_only": settings().ai_training_only,
        "counts": {
            name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
            for name in tables
        },
        "flags": tutor.flags(conn),
        "providers": [
            dict(r) for r in conn.execute(select(db.table("ai_provider_configs"))).mappings()
        ],
        "units": [
            dict(r)
            for r in conn.execute(
                select(db.table("ai_units")).order_by(
                    db.table("ai_units").c.grade, db.table("ai_units").c.position
                )
            ).mappings()
        ],
    }


@router.get("/admin/lessons")
def admin_lessons(
    grade: int = Query(4, ge=1, le=5), user=Depends(current_user), conn=Depends(connection)
):
    learning.staff(conn, user, "read")
    lessons, units = (db.table(n) for n in ("ai_lessons", "ai_units"))
    return [
        dict(r)
        for r in conn.execute(
            select(lessons, units.c.grade)
            .join(units)
            .where(units.c.grade == grade)
            .order_by(lessons.c.position)
        ).mappings()
    ]


@router.get("/admin/lessons/{identifier}")
def draft(identifier: UUID, user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user, "read")
    row = learning.lesson_row(conn, identifier)
    versions = db.table("ai_lesson_versions")
    return {
        "lesson": row,
        "versions": [
            dict(r)
            for r in conn.execute(
                select(versions)
                .where(versions.c.lesson_id == identifier)
                .order_by(versions.c.version.desc())
            ).mappings()
        ],
    }


@router.post("/admin/lessons")
def create(payload: DraftInput, user=Depends(current_user), conn=Depends(connection)):
    return cms.save_draft(conn, user, payload)


@router.put("/admin/lessons/{identifier}")
def edit(
    identifier: UUID, payload: DraftInput, user=Depends(current_user), conn=Depends(connection)
):
    return cms.save_draft(conn, user, payload, identifier)


@router.post("/admin/lessons/{identifier}/{action}")
def workflow(
    identifier: UUID,
    action: str,
    payload: RevisionInput,
    user=Depends(current_user),
    conn=Depends(connection),
):
    if action not in {"submit", "review", "publish", "archive"}:
        raise HTTPException(404, "Không tìm thấy thao tác")
    return cms.workflow(conn, user, identifier, action, payload.revision)


class UploadInput(StrictModel):
    data: str = Field(max_length=700000)
    alt: str = Field(min_length=5, max_length=500)
    license: str = Field(min_length=5, max_length=500)
    source: str = Field(min_length=5, max_length=500)


@router.post("/admin/media")
def upload(payload: UploadInput, user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user)
    if _throttle("academy-upload:" + str(user["id"]), 10):
        raise HTTPException(429, "Đợi một phút trước khi tải thêm ảnh")
    from app.academy.uploads import upload

    return upload(conn, user, payload.model_dump())


@router.get("/admin/media")
def admin_media(page: int = Query(1, ge=1), user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user, "read")
    table = db.table("ai_media_assets")
    return [
        dict(r)
        for r in conn.execute(
            select(table)
            .order_by(table.c.created_at.desc(), table.c.code)
            .offset((page - 1) * 60)
            .limit(60)
        ).mappings()
    ]


class MediaReview(StrictModel):
    approved: bool


@router.post("/admin/media/{identifier}/review")
def media_review(
    identifier: UUID, payload: MediaReview, user=Depends(current_user), conn=Depends(connection)
):
    learning.staff(conn, user, "reviewer")
    table = db.table("ai_media_assets")
    if not conn.execute(
        select(table.c.id).where(table.c.id == identifier).with_for_update()
    ).first():
        raise HTTPException(404, "Không có hình này")
    if not payload.approved:
        usages, versions = db.table("ai_media_usages"), db.table("ai_lesson_versions")
        if conn.execute(
            select(usages.c.asset_id)
            .join(versions)
            .where(usages.c.asset_id == identifier, versions.c.status == "published")
        ).first():
            raise HTTPException(
                409, "Hình đang dùng trong bài published; ẩn bài hoặc thay media trước khi thu hồi"
            )
    result = conn.execute(
        update(table)
        .where(table.c.id == identifier)
        .values(status="approved" if payload.approved else "archived", reviewed_by=user["id"])
    ).rowcount
    if not result:
        raise HTTPException(404, "Không có hình này")
    jobs = db.table("ai_generation_jobs")
    conn.execute(
        update(jobs)
        .where(jobs.c.asset_id == identifier)
        .values(status="approved" if payload.approved else "failed", updated_at=now())
    )
    learning.audit(
        conn, user["id"], "academy.media_reviewed", identifier, {"approved": payload.approved}
    )
    return {"approved": payload.approved}


class UnitInput(StrictModel):
    grade: int = Field(ge=1, le=5)
    title: str = Field(min_length=3, max_length=180)
    code: str = Field(pattern=r"^[A-Za-z0-9_-]{3,80}$")
    description: str = Field(min_length=10, max_length=2000)


@router.post("/admin/units")
def new_unit(payload: UnitInput, user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user)
    grades, units = db.table("ai_grades"), db.table("ai_units")
    conn.execute(select(grades.c.grade).where(grades.c.grade == payload.grade).with_for_update())
    if conn.execute(select(units.c.id).where(units.c.code == payload.code)).first():
        raise HTTPException(409, "Mã chủ đề đã tồn tại")
    position = conn.execute(
        select(func.coalesce(func.max(units.c.position), 0) + 1).where(
            units.c.grade == payload.grade
        )
    ).scalar_one()
    result = (
        conn.execute(
            units.insert()
            .values(
                grade=payload.grade,
                title=payload.title,
                code=payload.code,
                description=payload.description,
                position=position,
            )
            .returning(units)
        )
        .mappings()
        .one()
    )
    learning.audit(conn, user["id"], "academy.unit_created", result["id"])
    return dict(result)


@router.get("/admin/moderation")
def moderation(user=Depends(admin_user), conn=Depends(connection)):
    table = db.table("ai_moderation_reviews")
    return [
        dict(r)
        for r in conn.execute(
            select(table).order_by(table.c.created_at.desc()).limit(100)
        ).mappings()
    ]


@router.post("/admin/moderation/{identifier}/review")
def moderate(identifier: UUID, user=Depends(admin_user), conn=Depends(connection)):
    table = db.table("ai_moderation_reviews")
    if not conn.execute(
        update(table)
        .where(table.c.id == identifier)
        .values(status="reviewed", reviewed_by=user["id"])
    ).rowcount:
        raise HTTPException(404, "Không có cảnh báo này")
    learning.audit(conn, user["id"], "academy.moderation_reviewed", identifier)
    return {"reviewed": True}


class PolicyInput(AdminAction):
    code: str = Field(
        pattern="^(tutor_enabled|voice_enabled|image_generation_enabled|student_creative_enabled)$"
    )
    enabled: bool
    approve_local_model: bool = False


@router.post("/admin/policy")
def policy(payload: PolicyInput, user=Depends(admin_user), conn=Depends(connection)):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    if (
        settings().ai_training_only
        and payload.enabled
        and payload.code in {"tutor_enabled", "image_generation_enabled"}
    ):
        raise HTTPException(
            422, "Đang ưu tiên đào tạo lý thuyết và bài tập; chức năng gọi mô hình tạm tắt"
        )
    if payload.code == "tutor_enabled" and payload.enabled:
        if (
            not payload.approve_local_model
            or settings().ai_provider != "ollama"
            or not settings().ai_ollama_model
        ):
            raise HTTPException(
                422,
                "Cần cấu hình mô hình local, kiểm tra chính sách và xác nhận người vận hành trước khi bật",
            )
        provider = db.table("ai_provider_configs")
        conn.execute(
            update(provider)
            .where(provider.c.code == "ollama")
            .values(enabled=True, policy_approved=True, updated_by=user["id"], updated_at=now())
        )
    if payload.code == "image_generation_enabled" and payload.enabled:
        raise HTTPException(
            422, "Chưa có adapter tạo ảnh bằng mô hình đã được duyệt; hàng đợi SVG hoạt động riêng"
        )
    table = db.table("ai_feature_flags")
    conn.execute(
        update(table)
        .where(table.c.code == payload.code)
        .values(enabled=payload.enabled, updated_by=user["id"])
    )
    learning.audit(
        conn,
        user["id"],
        "academy.policy_changed",
        metadata={"flag": payload.code, "enabled": payload.enabled},
    )
    return tutor.flags(conn)


class ClassInput(AdminAction):
    name: str = Field(min_length=3, max_length=160)
    grade: int = Field(ge=1, le=5)
    teacher_id: UUID
    school_id: UUID | None = None


@router.post("/admin/classes")
def class_create(payload: ClassInput, user=Depends(admin_user), conn=Depends(connection)):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    roles, users = db.table("user_roles"), db.table("users")
    if not conn.execute(
        select(users.c.id)
        .join(roles)
        .where(
            users.c.id == payload.teacher_id, users.c.is_active.is_(True), roles.c.role == "teacher"
        )
    ).first():
        raise HTTPException(422, "Chọn giáo viên đang hoạt động")
    if (
        payload.school_id
        and not conn.execute(
            select(db.table("schools").c.id).where(
                db.table("schools").c.id == payload.school_id,
                db.table("schools").c.is_active.is_(True),
            )
        ).first()
    ):
        raise HTTPException(422, "Trường không hợp lệ")
    from uuid import uuid4

    identifier = uuid4()
    conn.execute(
        db.table("classes")
        .insert()
        .values(
            id=identifier,
            code="AI-" + identifier.hex[:12],
            name=payload.name,
            grade=payload.grade,
            teacher_user_id=payload.teacher_id,
            school_id=payload.school_id,
        )
    )
    learning.audit(conn, user["id"], "academy.class_created", identifier)
    return {"id": identifier}


class EnrollInput(AdminAction):
    student_id: UUID


@router.post("/admin/classes/{identifier}/enroll")
def enroll(
    identifier: UUID, payload: EnrollInput, user=Depends(admin_user), conn=Depends(connection)
):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    classroom = cms.class_access(conn, user, identifier)
    profiles = db.table("student_profiles")
    profile = (
        conn.execute(select(profiles).where(profiles.c.student_id == payload.student_id))
        .mappings()
        .first()
    )
    if (
        not profile
        or profile["current_grade"] != classroom["grade"]
        or (classroom["school_id"] and profile["school_id"] != classroom["school_id"])
    ):
        raise HTTPException(422, "Học sinh phải cùng lớp khối và trường của lớp được ghi danh")
    table = db.table("class_enrollments")
    conn.execute(
        insert(table)
        .values(class_id=identifier, student_id=payload.student_id)
        .on_conflict_do_update(
            index_elements=[table.c.class_id, table.c.student_id], set_={"left_at": None}
        )
    )
    learning.audit(conn, user["id"], "academy.enrolled", identifier)
    return {"enrolled": True}


class RoleInput(AdminAction):
    user_id: UUID
    role: str = Field(pattern="^(editor|reviewer)$")
    grant: bool


@router.post("/admin/staff")
def staff_role(payload: RoleInput, user=Depends(admin_user), conn=Depends(connection)):
    from app.services.accounts import authenticate_actor

    authenticate_actor(conn, user, payload.actor_password)
    if payload.grant:
        roles = db.table("user_roles")
        if not conn.execute(
            select(roles.c.user_id).where(
                roles.c.user_id == payload.user_id, roles.c.role == "teacher"
            )
        ).first():
            raise HTTPException(422, "Chỉ cấp quyền biên soạn/kiểm duyệt cho giáo viên")
    if not conn.execute(
        select(db.table("users").c.id).where(
            db.table("users").c.id == payload.user_id, db.table("users").c.is_active.is_(True)
        )
    ).first():
        raise HTTPException(422, "Tài khoản không khả dụng")
    table = db.table("ai_staff_roles")
    if payload.grant:
        conn.execute(
            insert(table)
            .values(user_id=payload.user_id, role=payload.role, assigned_by=user["id"])
            .on_conflict_do_nothing()
        )
    else:
        conn.execute(
            table.delete().where(table.c.user_id == payload.user_id, table.c.role == payload.role)
        )
    learning.audit(
        conn,
        user["id"],
        "academy.staff_changed",
        payload.user_id,
        {"role": payload.role, "granted": payload.grant},
    )
    return {"granted": payload.grant}


class JobInput(StrictModel):
    template: str = Field(pattern="^(robot|poster|comic)$")
    palette: int = Field(default=0, ge=0, le=5)


@router.get("/admin/jobs")
def jobs(user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user, "read")
    table = db.table("ai_generation_jobs")
    return [
        dict(r)
        for r in conn.execute(
            select(table).order_by(table.c.created_at.desc()).limit(50)
        ).mappings()
    ]


@router.post("/admin/jobs")
def job_create(payload: JobInput, user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user)
    result = conn.execute(
        db.table("ai_generation_jobs")
        .insert()
        .values(
            requested_by=user["id"],
            template=payload.template,
            parameters={"palette": payload.palette, "mode": "svg_template"},
            status="queued",
        )
        .returning(db.table("ai_generation_jobs").c.id)
    ).scalar_one()
    return {"id": result, "mode": "svg_template"}


@router.post("/admin/jobs/{identifier}/run")
def run_job(identifier: UUID, user=Depends(current_user), conn=Depends(connection)):
    learning.staff(conn, user)
    if _throttle("academy-svg-job:" + str(user["id"]), 10):
        raise HTTPException(429, "Đợi một phút trước khi tạo thêm hình")
    from hashlib import sha256
    from uuid import uuid4

    from app.academy.providers import ApprovedSVGProvider

    jobs = db.table("ai_generation_jobs")
    job = (
        conn.execute(select(jobs).where(jobs.c.id == identifier).with_for_update())
        .mappings()
        .first()
    )
    if not job or job["status"] != "queued":
        raise HTTPException(409, "Job đã chạy hoặc không tồn tại")
    data = ApprovedSVGProvider().generate(job["template"], job["parameters"]["palette"])
    asset_id = uuid4()
    key = str(asset_id) + ".svg"
    root = settings().ai_media_root
    root.mkdir(parents=True, exist_ok=True)
    (root / key).write_bytes(data)
    conn.execute(
        db.table("media_assets")
        .insert()
        .values(
            id=asset_id,
            bucket_name="ai-academy-local",
            object_key=key,
            mime_type="image/svg+xml",
            sha256=sha256(data).hexdigest(),
            file_size_bytes=len(data),
            visibility="private",
            uploaded_by=user["id"],
        )
    )
    conn.execute(
        db.table("ai_media_assets")
        .insert()
        .values(
            id=asset_id,
            code="generated-" + str(asset_id),
            category="generated",
            alt="Minh họa " + job["template"] + " tạo từ template SVG đã duyệt",
            license="CC BY 4.0 · VietTree",
            source="SVG template; không phải ảnh sinh từ mô hình AI",
            status="review",
            width=600,
            height=360,
        )
    )
    conn.execute(
        db.table("ai_media_variants")
        .insert()
        .values(
            asset_id=asset_id,
            kind="original",
            object_key=key,
            mime_type="image/svg+xml",
            sha256=sha256(data).hexdigest(),
            file_size_bytes=len(data),
            width=600,
            height=360,
        )
    )
    conn.execute(
        update(jobs)
        .where(jobs.c.id == identifier)
        .values(status="review", asset_id=asset_id, updated_at=now())
    )
    return {"asset_id": asset_id, "status": "review", "mode": "svg_template"}
