from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select

from app.classroom import pricing, recognition, service
from app.classroom.schemas import (
    AssignmentInput,
    Category,
    ClassInput,
    EnrollmentInput,
    PriceInput,
    PromotionInput,
    RecognitionInput,
)
from app.core.dependencies import database
from app.core.security import admin_user, current_user, student_user
from app.db import db

router = APIRouter(prefix="/api/v1", tags=["classes-achievements-prices"])


@router.get("/membership/prices")
def prices(conn=database):
    return pricing.catalog(conn)


@router.get("/admin/membership/prices")
def price_admin(user=Depends(admin_user), conn=database):
    return {
        **pricing.catalog(conn),
        "price_options": [
            dict(r)
            for r in conn.execute(
                select(db.table("vip_price_options")).order_by(
                    db.table("vip_price_options").c.duration_days
                )
            ).mappings()
        ],
        "promotions": [
            dict(r)
            for r in conn.execute(
                select(db.table("vip_promotions")).order_by(db.table("vip_promotions").c.code)
            ).mappings()
        ],
    }


@router.put("/admin/membership/prices/{code}")
def update_price(code: str, payload: PriceInput, user=Depends(admin_user), conn=database):
    return pricing.save_price(conn, user, code, payload)


@router.post("/admin/membership/promotions")
def save_promotion(payload: PromotionInput, user=Depends(admin_user), conn=database):
    return pricing.save_promotion(conn, user, payload)


@router.get("/classroom/classes")
def list_classes(user=Depends(current_user), conn=database):
    classes, enrollments, settings = (
        db.table(n) for n in ("classes", "class_enrollments", "classroom_settings")
    )
    query = select(
        classes, func.coalesce(settings.c.recognition_enabled, True).label("recognition_enabled")
    ).outerjoin(settings)
    if "admin" not in user["roles"]:
        query = query.where(classes.c.is_active.is_(True))
        if "teacher" in user["roles"]:
            query = query.where(classes.c.teacher_user_id == user["id"])
        elif "student" in user["roles"]:
            query = query.join(enrollments).where(
                enrollments.c.student_id == user["id"], enrollments.c.left_at.is_(None)
            )
        else:
            raise HTTPException(403, "Dùng không gian phụ huynh để xem hồ sơ trẻ")
    counts = dict(
        conn.execute(
            select(enrollments.c.class_id, func.count())
            .where(enrollments.c.left_at.is_(None))
            .group_by(enrollments.c.class_id)
        ).all()
    )
    return [
        {**dict(row), "student_count": counts.get(row["id"], 0)}
        for row in conn.execute(
            query.order_by(classes.c.is_active.desc(), classes.c.name)
        ).mappings()
    ]


@router.get("/classroom/schools")
def schools(user=Depends(admin_user), conn=database):
    table = db.table("schools")
    return [
        dict(r)
        for r in conn.execute(
            select(table.c.id, table.c.name)
            .where(table.c.is_active.is_(True))
            .order_by(table.c.name)
        ).mappings()
    ]


@router.post("/classroom/classes")
def new_class(payload: ClassInput, user=Depends(admin_user), conn=database):
    return service.save_class(conn, user, payload)


@router.put("/classroom/classes/{identifier}")
def edit_class(identifier: UUID, payload: ClassInput, user=Depends(admin_user), conn=database):
    return service.save_class(conn, user, payload, identifier)


@router.post("/classroom/classes/{identifier}/enrollments")
def enrollment(
    identifier: UUID, payload: EnrollmentInput, user=Depends(current_user), conn=database
):
    service.staff(user)
    return service.enroll(conn, user, identifier, payload)


@router.get("/classroom/students")
def students(
    class_id: UUID | None = None,
    grade: int = Query(4, ge=1, le=5),
    free_only: bool = False,
    search: str = Query("", max_length=100),
    page: int = Query(1, ge=1),
    user=Depends(current_user),
    conn=database,
):
    service.staff(user)
    users, profiles, enrollments, roles = (
        db.table(n) for n in ("users", "student_profiles", "class_enrollments", "user_roles")
    )
    query = (
        select(users.c.id, users.c.username, users.c.display_name, profiles.c.current_grade)
        .select_from(users.join(profiles, profiles.c.student_id == users.c.id))
        .where(
            users.c.is_active.is_(True),
            profiles.c.current_grade == grade if class_id is None else True,
            select(roles.c.user_id)
            .where(roles.c.user_id == users.c.id, roles.c.role == "student")
            .exists(),
        )
    )
    if class_id:
        service.class_scope(conn, user, class_id, staff_only=True)
        query = query.join(enrollments).where(
            enrollments.c.class_id == class_id, enrollments.c.left_at.is_(None)
        )
    elif "admin" not in user["roles"]:
        raise HTTPException(403, "Giáo viên chỉ xem học sinh ở lớp được phân công")
    if free_only:
        classes = db.table("classes")
        query = query.where(
            ~select(enrollments.c.student_id)
            .select_from(enrollments.join(classes, classes.c.id == enrollments.c.class_id))
            .where(
                enrollments.c.student_id == users.c.id,
                enrollments.c.left_at.is_(None),
                classes.c.is_active.is_(True),
            )
            .correlate(users)
            .exists()
        )
    if search:
        query = query.where(
            users.c.display_name.ilike("%" + search + "%")
            | users.c.username.ilike("%" + search + "%")
        )
    total = conn.execute(select(func.count()).select_from(query.subquery())).scalar_one()
    return {
        "total": total,
        "page": page,
        "items": [
            dict(r)
            for r in conn.execute(
                query.order_by(users.c.display_name, users.c.id).offset((page - 1) * 50).limit(50)
            ).mappings()
        ],
    }


@router.get("/classroom/resources")
def resources(
    kind: Literal["lesson", "assessment", "ai_lesson"],
    grade: int = Query(4, ge=1, le=5),
    user=Depends(current_user),
    conn=database,
):
    service.staff(user)
    if kind == "ai_lesson":
        from app.academy.learning import catalog

        return [
            {"id": r["id"], "title": r["title"], "minimum_plan_code": r["minimum_plan_code"]}
            for r in catalog(conn, grade)
        ]
    policies = db.table("content_access_policies")
    subjects, topics = db.table("subjects"), db.table("topics")
    table = db.table("lessons" if kind == "lesson" else "assessments")
    query = (
        select(
            table.c.id,
            table.c.title,
            policies.c.minimum_plan_code,
            subjects.c.code.label("subject_code"),
        )
        .select_from(table)
        .outerjoin(
            policies,
            policies.c.lesson_id == table.c.id
            if kind == "lesson"
            else policies.c.assessment_id == table.c.id,
        )
        .where(table.c.status == "published")
    )
    if kind == "lesson":
        query = (
            query.join(topics, topics.c.id == table.c.topic_id)
            .join(subjects, subjects.c.id == topics.c.subject_id)
            .where(topics.c.grade == grade, topics.c.is_active.is_(True))
        )
    else:
        query = query.join(subjects, subjects.c.id == table.c.subject_id).where(
            table.c.grade == grade
        )
    return [dict(r) for r in conn.execute(query.order_by(table.c.title)).mappings()]


@router.post("/classroom/assignments")
def assign(payload: AssignmentInput, user=Depends(current_user), conn=database):
    return service.assign(conn, user, payload)


@router.get("/classroom/my-assignments")
def assignments(user=Depends(student_user), conn=database):
    batches, targets, classes = (
        db.table(n)
        for n in ("learning_assignment_batches", "learning_assignment_targets", "classes")
    )
    rows = list(
        conn.execute(
            select(batches, targets.c.assignment_id, classes.c.name.label("class_name"))
            .join(targets)
            .outerjoin(classes)
            .where(targets.c.student_id == user["id"])
            .order_by(batches.c.created_at.desc())
            .limit(100)
        ).mappings()
    )
    output = []
    for row in rows:
        if row["class_id"]:
            try:
                service.class_scope(conn, user, row["class_id"])
            except HTTPException:
                continue
        table = db.table(
            {"lesson": "lessons", "assessment": "assessments", "ai_lesson": "ai_lessons"}[
                row["kind"]
            ]
        )
        resource = conn.execute(
            select(table.c.title).where(table.c.id == row["resource_id"])
        ).scalar()
        output.append({**dict(row), "title": resource or "Bài học đã ẩn"})
    return output


@router.get("/classroom/classes/{identifier}/leaderboard")
def board(
    identifier: UUID,
    category: Category = "MATH",
    period: Literal["week", "month"] = "month",
    resource_id: UUID | None = None,
    user=Depends(current_user),
    conn=database,
):
    return recognition.leaderboard(conn, user, identifier, category, period, resource_id)


@router.post("/classroom/classes/{identifier}/recognition")
def recognize(
    identifier: UUID,
    payload: RecognitionInput,
    user=Depends(current_user),
    conn=database,
):
    return recognition.publish(conn, user, identifier, payload)


@router.get("/classroom/classes/{identifier}/recognition")
def awards(identifier: UUID, user=Depends(current_user), conn=database):
    service.class_scope(conn, user, identifier)
    settings = db.table("classroom_settings")
    if (
        conn.execute(
            select(settings.c.recognition_enabled).where(settings.c.class_id == identifier)
        ).scalar()
        is False
    ):
        return []
    batches, awards = db.table("class_award_batches"), db.table("class_awards")
    return [
        {
            **dict(r),
            "winners": [
                {
                    key: value
                    for key, value in dict(w).items()
                    if key not in {"student_id", "batch_id"}
                }
                for w in conn.execute(
                    select(awards).where(awards.c.batch_id == r["id"]).order_by(awards.c.rank)
                ).mappings()
            ],
        }
        for r in conn.execute(
            select(batches)
            .where(batches.c.class_id == identifier)
            .order_by(batches.c.published_at.desc())
            .limit(20)
        ).mappings()
    ]


@router.get("/classroom/my-achievements")
def achievements(
    period: Literal["week", "month"] = "month", user=Depends(student_user), conn=database
):
    profile = db.table("student_profiles")
    grade = conn.execute(
        select(profile.c.current_grade).where(profile.c.student_id == user["id"])
    ).scalar_one()
    start, end = recognition.period_bounds(period)
    categories = []
    for category in ("MATH", "VIETNAMESE", "ENGLISH", "AI", "AI_PROJECT"):
        result = recognition.aggregate(
            recognition.score_records(conn, [user["id"]], grade, category, start, end)
        )
        categories.append(
            {
                "category": category,
                "completed": result[0]["completed"] if result else 0,
                "score": round(result[0]["score"], 3) if result else None,
            }
        )
    progress = db.table("student_lesson_progress")
    reads = conn.execute(
        select(func.count())
        .select_from(progress)
        .where(
            progress.c.student_id == user["id"],
            progress.c.status == "completed",
            progress.c.completed_at >= start,
            progress.c.completed_at < end,
        )
    ).scalar_one()
    return {
        "period": period,
        "categories": categories,
        "reading_completed": reads,
        "note": "Đọc bài được ghi nhận riêng; chỉ bài có chấm điểm mới có điểm thành tích.",
    }
