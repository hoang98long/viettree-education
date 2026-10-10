from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app import schemas as out
from app.core.security import (
    admin_user,
    create_session,
    current_user,
    digest,
    now,
    public_user,
    revoke_session,
    student_user,
    throttle_login,
    verify_origin,
    verify_password,
)
from app.db import connection, db
from app.lesson_support import enrich
from app.personalization.engine import recommendations
from app.schemas import (
    AnswerInput,
    AttemptResponse,
    Grade,
    LoginInput,
    StartInput,
    StudentUpdate,
    UserResponse,
)
from app.services import access, learning
from app.services import attempts as service

router = APIRouter(prefix="/api/v1")


def _user_response(user, conn):
    result = public_user(user)
    if "student" in user["roles"]:
        profiles = db.table("student_profiles")
        options = (
            conn.execute(
                select(profiles.c.accessibility_options).where(profiles.c.student_id == user["id"])
            ).scalar()
            or {}
        )
        result["text_size"] = "large" if options.get("text_size") == "large" else "comfortable"
    return result


@router.post("/auth/login", response_model=UserResponse, tags=["auth"])
def login(payload: LoginInput, request: Request, response: Response, conn=Depends(connection)):
    verify_origin(request)
    if throttle_login(request):
        raise HTTPException(
            429, "Em hãy đợi một phút rồi thử lại nhé", headers={"Retry-After": "60"}
        )
    users, roles = db.table("users"), db.table("user_roles")
    user = (
        conn.execute(
            select(users).where(func.lower(users.c.username) == payload.username.strip().lower())
        )
        .mappings()
        .first()
    )
    valid = verify_password(user["password_hash"] if user else None, payload.password)
    if not valid or not user["is_active"]:
        raise HTTPException(401, "Tên đăng nhập hoặc mật khẩu chưa đúng")
    conn.execute(users.update().where(users.c.id == user["id"]).values(last_login_at=now()))
    role_names = list(
        conn.execute(select(roles.c.role).where(roles.c.user_id == user["id"])).scalars()
    )
    expires_at = create_session(conn, user["id"], response, role_names, payload.remember_me)
    # Thay phiên trên cùng trình duyệt sau khi xác thực thành công.
    previous_token = request.cookies.get("viettree_session")
    if previous_token:
        revoke_session(conn, digest(previous_token))
    return _user_response(
        {**dict(user), "roles": role_names, "session_expires_at": expires_at}, conn
    )


@router.get("/auth/me", response_model=UserResponse, tags=["auth"])
def me(user=Depends(current_user), conn=Depends(connection)):
    return _user_response(user, conn)


@router.put("/students/me/accessibility", response_model=out.AccessibilityInput, tags=["student"])
def accessibility(
    payload: out.AccessibilityInput, user=Depends(student_user), conn=Depends(connection)
):
    profile = service.lock_student(conn, user["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == user["id"])
        .values(
            accessibility_options={
                **profile["accessibility_options"],
                "text_size": payload.text_size,
            },
            updated_at=now(),
        )
    )
    return payload


@router.get(
    "/students/me/learning-plans", response_model=list[out.LearningPlanResponse], tags=["student"]
)
def learning_plans(user=Depends(student_user), conn=Depends(connection)):
    profiles = db.table("student_profiles")
    grade = conn.execute(
        select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
    ).scalar_one()
    return learning.list_plans(conn, user["id"], grade)


@router.post(
    "/students/me/learning-plans", response_model=out.LearningPlanResponse, tags=["student"]
)
def create_learning_plan(
    payload: out.LearningPlanInput, user=Depends(student_user), conn=Depends(connection)
):
    profile = service.lock_student(conn, user["id"])
    return learning.create_plan(
        conn, user["id"], profile["current_grade"], payload.subject_code, payload.mode
    )


@router.post("/auth/logout", response_model=dict[str, bool], tags=["auth"])
def logout(response: Response, user=Depends(current_user), conn=Depends(connection)):
    revoke_session(conn, user["session_hash"])
    response.delete_cookie("viettree_session", path="/")
    response.delete_cookie("viettree_csrf", path="/")
    return {"logged_out": True}


@router.get("/grades", response_model=list[out.GradeResponse], tags=["curriculum"])
def grades(user=Depends(current_user)):
    return [
        {
            "grade": grade,
            "status": "available" if grade == 4 else "building",
            "label": "Có thể học ngay" if grade == 4 else "Đang xây dựng",
        }
        for grade in range(1, 6)
    ]


@router.get("/subjects", response_model=list[out.SubjectResponse], tags=["curriculum"])
def subjects(grade: Grade = 4, user=Depends(current_user), conn=Depends(connection)):
    table, topics = db.table("subjects"), db.table("topics")
    rows = (
        conn.execute(
            select(
                table.c.id,
                table.c.code,
                table.c.name_vi,
                table.c.description,
                select(func.count())
                .where(
                    topics.c.subject_id == table.c.id,
                    topics.c.grade == grade,
                    topics.c.is_active.is_(True),
                )
                .scalar_subquery()
                .label("topic_count"),
            )
            .where(table.c.is_active.is_(True))
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )
    return [
        {**dict(row), "grade": grade, "status": "available" if row["topic_count"] else "building"}
        for row in rows
    ]


@router.get("/topics", response_model=list[out.TopicResponse], tags=["curriculum"])
def topics(
    grade: Grade = 4,
    subject_code: str = "MATH",
    user=Depends(current_user),
    conn=Depends(connection),
):
    table, subjects = db.table("topics"), db.table("subjects")
    return (
        conn.execute(
            select(table)
            .join(subjects)
            .where(
                table.c.grade == grade, subjects.c.code == subject_code, table.c.is_active.is_(True)
            )
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )


@router.get("/lessons", response_model=list[out.LessonSummaryResponse], tags=["curriculum"])
def lessons(topic_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    table = db.table("lessons")
    topics = db.table("topics")
    grade = conn.execute(select(topics.c.grade).where(topics.c.id == topic_id)).scalar()
    rows = (
        conn.execute(
            select(
                table.c.id,
                table.c.topic_id,
                table.c.code,
                table.c.title,
                table.c.description,
                table.c.estimated_minutes,
                table.c.status,
            )
            .where(table.c.topic_id == topic_id, table.c.status == "published")
            .order_by(table.c.sort_order)
        )
        .mappings()
        .all()
    )
    return [
        {**dict(row), **access.content_access(conn, user, "lesson", row["id"], grade)}
        for row in rows
    ]


@router.get("/lessons/{lesson_id}", response_model=out.LessonResponse, tags=["curriculum"])
def lesson(lesson_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    table, topics, subjects, assessments = (
        db.table(name) for name in ("lessons", "topics", "subjects", "assessments")
    )
    row = (
        conn.execute(
            select(
                table,
                topics.c.grade,
                topics.c.title.label("topic_title"),
                subjects.c.code.label("subject_code"),
                subjects.c.name_vi.label("subject_name"),
            )
            .select_from(table.join(topics).join(subjects))
            .where(
                table.c.id == lesson_id, table.c.status == "published", topics.c.is_active.is_(True)
            )
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài học")
    gate = access.authorize_content(conn, user, "lesson", lesson_id, row["grade"])
    practice = (
        conn.execute(
            select(assessments.c.id, assessments.c.title).where(
                assessments.c.topic_id == row["topic_id"], assessments.c.status == "published"
            )
        )
        .mappings()
        .all()
    )
    progress = db.table("student_lesson_progress")
    progress_status = (
        conn.execute(
            select(progress.c.status).where(
                progress.c.student_id == user["id"], progress.c.lesson_id == lesson_id
            )
        ).scalar()
        or "not_started"
    )
    practice = [
        dict(item)
        for item in practice
        if access.eligible(conn, user["id"], "assessment", item["id"], row["grade"])
        or "admin" in user["roles"]
    ]
    topic_code = conn.execute(
        select(topics.c.code).where(topics.c.id == row["topic_id"])
    ).scalar_one()
    candidates = conn.execute(
        select(table.c.id, table.c.title, progress.c.status.label("progress_status"))
        .select_from(
            table.outerjoin(
                progress,
                (progress.c.lesson_id == table.c.id) & (progress.c.student_id == user["id"]),
            )
        )
        .where(
            table.c.topic_id == row["topic_id"],
            table.c.status == "published",
            table.c.id != lesson_id,
            (progress.c.status.is_(None) | (progress.c.status != "completed")),
        )
        .order_by(table.c.sort_order, table.c.id)
    ).mappings()
    membership = access.resolve_membership(conn, user["id"]) if "student" in user["roles"] else None
    next_lessons = []
    for candidate in candidates:
        if not access.content_access(
            conn, user, "lesson", candidate["id"], row["grade"], membership
        )["locked"]:
            next_lessons.append(
                {
                    "id": candidate["id"],
                    "title": candidate["title"],
                    "reason": "Cùng chủ đề, em chưa đánh dấu đọc xong.",
                }
            )
        if len(next_lessons) == 3:
            break
    return {
        **dict(row),
        **gate,
        "content": enrich(row["content"], topic_code),
        "practice": practice,
        "progress_status": progress_status,
        "next_lessons": next_lessons,
    }


@router.post("/lessons/{lesson_id}/visit", response_model=dict[str, bool], tags=["student"])
def visit_lesson(lesson_id: UUID, user=Depends(student_user), conn=Depends(connection)):
    profile = service.lock_student(conn, user["id"])
    record = lesson(lesson_id, user, conn)
    if record["grade"] != profile["current_grade"]:
        raise HTTPException(403, "Bài học không thuộc lớp của em")
    table = db.table("student_lesson_progress")
    statement = insert(table).values(
        student_id=user["id"],
        lesson_id=lesson_id,
        status="in_progress",
        first_started_at=now(),
        last_accessed_at=now(),
    )
    conn.execute(
        statement.on_conflict_do_update(
            index_elements=[table.c.student_id, table.c.lesson_id], set_={"last_accessed_at": now()}
        )
    )
    learning.update_targets(conn, user["id"], lesson_id=lesson_id, completed=False)
    return {"visited": True}


@router.post("/lessons/{lesson_id}/complete", response_model=dict[str, bool], tags=["student"])
def complete_lesson(lesson_id: UUID, user=Depends(student_user), conn=Depends(connection)):
    profile = service.lock_student(conn, user["id"])
    record = lesson(lesson_id, user, conn)
    if record["grade"] != profile["current_grade"]:
        raise HTTPException(403, "Bài học không thuộc lớp của em")
    progress = db.table("student_lesson_progress")
    at = now()
    statement = insert(progress).values(
        student_id=user["id"],
        lesson_id=lesson_id,
        status="completed",
        completion_ratio=1,
        first_started_at=at,
        completed_at=at,
        last_accessed_at=at,
    )
    conn.execute(
        statement.on_conflict_do_update(
            index_elements=[progress.c.student_id, progress.c.lesson_id],
            set_={
                "status": "completed",
                "completion_ratio": 1,
                "completed_at": func.coalesce(progress.c.completed_at, at),
                "last_accessed_at": at,
                "updated_at": at,
            },
        )
    )
    if record["progress_status"] != "completed":
        conn.execute(
            db.table("learning_events")
            .insert()
            .values(
                student_id=user["id"],
                event_type="lesson_completed",
                properties={"source": "student_read_confirmation", "lesson_id": str(lesson_id)},
            )
        )
    learning.update_targets(conn, user["id"], lesson_id=lesson_id)
    return {"completed": True}


def assessment_list(conn, grade, subject_code=None, published_only=True):
    table, items, subjects = (
        db.table(name) for name in ("assessments", "assessment_items", "subjects")
    )
    statement = select(
        table.c.id,
        table.c.code,
        table.c.title,
        table.c.description,
        table.c.grade,
        table.c.status,
        table.c.lesson_id,
        table.c.topic_id,
        table.c.max_attempts,
        table.c.time_limit_seconds,
        table.c.assessment_type,
        subjects.c.code.label("subject_code"),
        subjects.c.name_vi.label("subject_name"),
        select(func.count())
        .where(items.c.assessment_id == table.c.id)
        .scalar_subquery()
        .label("item_count"),
    )
    statement = statement.select_from(table.join(subjects)).where(table.c.grade == grade)
    if published_only:
        statement = statement.where(table.c.status == "published")
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    return conn.execute(statement.order_by(table.c.code)).mappings().all()


@router.get("/assessments", response_model=list[out.AssessmentResponse], tags=["curriculum"])
def assessments(
    grade: Grade = 4,
    subject_code: str | None = None,
    user=Depends(current_user),
    conn=Depends(connection),
):
    return [
        {**dict(row), **access.content_access(conn, user, "assessment", row["id"], grade)}
        for row in assessment_list(conn, grade, subject_code)
    ]


@router.get(
    "/assessments/{assessment_id}", response_model=out.AssessmentResponse, tags=["curriculum"]
)
def assessment(assessment_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    row = service.published_assessment(conn, assessment_id)
    return next(
        {**dict(item), **access.content_access(conn, user, "assessment", item["id"], row["grade"])}
        for item in assessment_list(conn, row["grade"])
        if item["id"] == assessment_id
    )


@router.post(
    "/students/me/assessments/{assessment_id}/assign-self",
    response_model=out.AssignmentResponse,
    tags=["student"],
)
def assign(assessment_id: UUID, user=Depends(student_user), conn=Depends(connection)):
    return service.assign_self(conn, user["id"], assessment_id)


@router.get(
    "/students/me/assignments", response_model=list[out.AssignmentResponse], tags=["student"]
)
def assignments(user=Depends(student_user), conn=Depends(connection)):
    table, assessments = db.table("student_assignments"), db.table("assessments")
    rows = (
        conn.execute(
            select(table, assessments.c.title)
            .join(assessments)
            .where(table.c.student_id == user["id"])
            .order_by(table.c.created_at.desc())
        )
        .mappings()
        .all()
    )
    return [
        row
        for row in rows
        if access.eligible(conn, user["id"], "assessment", row["assessment_id"], None)
    ]


@router.post("/attempts", response_model=out.StartResponse, tags=["attempts"])
def start(payload: StartInput, user=Depends(student_user), conn=Depends(connection)):
    return service.start_attempt(conn, user["id"], payload.assignment_id)


@router.get("/attempts/{attempt_id}", response_model=AttemptResponse, tags=["attempts"])
def attempt(attempt_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    return service.get_attempt(conn, user, attempt_id)


@router.put(
    "/attempts/{attempt_id}/answers/{item_id}", response_model=dict[str, bool], tags=["attempts"]
)
def answer(
    attempt_id: UUID,
    item_id: UUID,
    payload: AnswerInput,
    user=Depends(student_user),
    conn=Depends(connection),
):
    return service.save_answer(conn, user, attempt_id, item_id, payload)


@router.post("/attempts/{attempt_id}/submit", response_model=out.ResultResponse, tags=["attempts"])
def submit(attempt_id: UUID, user=Depends(student_user), conn=Depends(connection)):
    return service.submit(conn, user, attempt_id)


@router.get("/attempts/{attempt_id}/result", response_model=out.ResultResponse, tags=["attempts"])
def result(attempt_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    return service.result(conn, user, attempt_id)


@router.get("/students/me/history", response_model=list[out.HistoryResponse], tags=["student"])
def history(
    subject_code: str | None = None,
    date: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    user=Depends(student_user),
    conn=Depends(connection),
):
    attempts, assessments, subjects = (
        db.table(name) for name in ("attempts", "assessments", "subjects")
    )
    statement = (
        select(
            attempts.c.id,
            attempts.c.status,
            attempts.c.total_score,
            attempts.c.max_score,
            attempts.c.started_at,
            attempts.c.graded_at,
            assessments.c.title,
            subjects.c.name_vi.label("subject_name"),
            subjects.c.code.label("subject_code"),
        )
        .select_from(
            attempts.join(assessments, attempts.c.assessment_id == assessments.c.id).join(subjects)
        )
        .where(attempts.c.student_id == user["id"])
    )
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    if date:
        statement = statement.where(
            func.to_char(func.timezone("Asia/Bangkok", attempts.c.started_at), "YYYY-MM-DD") == date
        )
    return (
        conn.execute(statement.order_by(attempts.c.started_at.desc()).limit(200)).mappings().all()
    )


@router.get("/students/me/skills", response_model=list[out.SkillResponse], tags=["student"])
def skill_progress(user=Depends(student_user), conn=Depends(connection)):
    mastery, skills, subjects = (
        db.table(name) for name in ("student_skill_mastery", "skills", "subjects")
    )
    return (
        conn.execute(
            select(mastery, skills.c.name, subjects.c.name_vi.label("subject_name"))
            .select_from(mastery.join(skills).join(subjects))
            .where(mastery.c.student_id == user["id"])
            .order_by(mastery.c.mastery_score)
        )
        .mappings()
        .all()
    )


@router.get(
    "/students/me/recommendations",
    response_model=list[out.RecommendationResponse],
    tags=["student"],
)
def recommended(user=Depends(student_user), conn=Depends(connection)):
    profile = service.lock_student(conn, user["id"])
    return recommendations(conn, user["id"], profile["current_grade"])


@router.get("/students/me/dashboard", response_model=out.DashboardResponse, tags=["student"])
def dashboard(user=Depends(student_user), conn=Depends(connection)):
    profile = service.lock_student(conn, user["id"])
    progress, lessons = db.table("student_lesson_progress"), db.table("lessons")
    continue_lesson = (
        conn.execute(
            select(lessons.c.id, lessons.c.title)
            .select_from(progress.join(lessons))
            .where(
                progress.c.student_id == user["id"],
                progress.c.status == "in_progress",
                lessons.c.status == "published",
            )
            .order_by(progress.c.last_accessed_at.desc())
            .limit(1)
        )
        .mappings()
        .first()
    )
    if continue_lesson and not access.eligible(
        conn, user["id"], "lesson", continue_lesson["id"], profile["current_grade"]
    ):
        continue_lesson = None
    return dict(
        user=public_user(user),
        grade=profile["current_grade"],
        subjects=subjects(profile["current_grade"], user, conn),
        history=history(None, None, user, conn),
        skills=skill_progress(user, conn),
        recommendations=recommendations(conn, user["id"], profile["current_grade"]),
        assignments=assignments(user, conn),
        continue_lesson=continue_lesson,
        completed_lessons=conn.execute(
            select(func.count())
            .select_from(progress)
            .where(progress.c.student_id == user["id"], progress.c.status == "completed")
        ).scalar_one(),
    )


@router.get("/students/me/profile", response_model=out.ProfileResponse, tags=["student"])
def profile(user=Depends(student_user), conn=Depends(connection)):
    table = db.table("student_profiles")
    row = (
        conn.execute(
            select(
                table.c.current_grade, table.c.learning_preferences, table.c.accessibility_options
            ).where(table.c.student_id == user["id"])
        )
        .mappings()
        .one()
    )
    return {**public_user(user), **dict(row)}


@router.get("/admin/statistics", response_model=out.StatisticsResponse, tags=["admin"])
def statistics(user=Depends(admin_user), conn=Depends(connection)):
    attempts, answers = db.table("attempts"), db.table("attempt_answers")
    stats = {
        "students": conn.execute(
            select(func.count()).select_from(db.table("student_profiles"))
        ).scalar_one()
    }
    for name in ("users", "lessons", "question_versions", "assessments"):
        table = db.table(name)
        statement = select(func.count()).select_from(table)
        if "status" in table.c:
            statement = statement.where(table.c.status == "published")
        stats[name] = conn.execute(statement).scalar_one()
    stats["attempts"] = conn.execute(
        select(func.count()).select_from(attempts).where(attempts.c.status == "graded")
    ).scalar_one()
    stats["average_percent"] = conn.execute(
        select(func.avg(attempts.c.total_score / func.nullif(attempts.c.max_score, 0) * 100)).where(
            attempts.c.status == "graded"
        )
    ).scalar()
    stats["correct_answers"] = conn.execute(
        select(func.count())
        .select_from(answers.join(attempts))
        .where(attempts.c.status == "graded", answers.c.is_correct.is_(True))
    ).scalar_one()
    return stats


@router.get("/admin/students", response_model=out.StudentPageResponse, tags=["admin"])
def students(
    search: str = "", page: int = Query(1, ge=1), user=Depends(admin_user), conn=Depends(connection)
):
    users, profiles = db.table("users"), db.table("student_profiles")
    statement = select(
        users.c.id,
        users.c.username,
        users.c.display_name,
        users.c.is_active,
        profiles.c.current_grade,
    ).join(profiles, profiles.c.student_id == users.c.id)
    if search:
        statement = statement.where(
            users.c.display_name.ilike("%" + search.replace("%", "\\%").replace("_", "\\_") + "%")
            | users.c.username.ilike("%" + search.replace("%", "\\%").replace("_", "\\_") + "%")
        )
    total = conn.execute(select(func.count()).select_from(statement.subquery())).scalar_one()
    return dict(
        total=total,
        page=page,
        items=conn.execute(statement.order_by(users.c.username).offset((page - 1) * 20).limit(20))
        .mappings()
        .all(),
    )


@router.patch("/admin/students/{student_id}", response_model=dict[str, bool], tags=["admin"])
def update_student(
    student_id: UUID, payload: StudentUpdate, user=Depends(admin_user), conn=Depends(connection)
):
    service.lock_student(conn, student_id)
    if not payload.display_name.strip():
        raise HTTPException(422, "Tên hiển thị không được để trống")
    users, profiles = db.table("users"), db.table("student_profiles")
    conn.execute(
        users.update()
        .where(users.c.id == student_id)
        .values(display_name=payload.display_name.strip())
    )
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == student_id)
        .values(current_grade=payload.current_grade)
    )
    conn.execute(
        insert(db.table("audit_logs")).values(
            actor_user_id=user["id"],
            action="student_profile_updated",
            entity_type="student_profile",
            entity_id=student_id,
            new_values={"current_grade": payload.current_grade},
        )
    )
    return {"updated": True}


@router.get("/admin/users", response_model=list[dict], tags=["admin"])
def users(page: int = Query(1, ge=1), user=Depends(admin_user), conn=Depends(connection)):
    table = db.table("users")
    return (
        conn.execute(
            select(table.c.id, table.c.username, table.c.display_name, table.c.is_active)
            .order_by(table.c.username)
            .offset((page - 1) * 20)
            .limit(20)
        )
        .mappings()
        .all()
    )


@router.get("/admin/questions", response_model=out.QuestionPageResponse, tags=["admin"])
def questions(
    grade: Grade = 4,
    subject_code: str | None = None,
    search: str = "",
    status: Literal["draft", "published", "archived"] | None = None,
    question_type: Literal["single_choice", "multiple_choice", "fill_blank", "ordering"]
    | None = None,
    minimum_plan_code: Literal["free", "vip"] | None = None,
    topic_id: UUID | None = None,
    page: int = Query(1, ge=1),
    user=Depends(admin_user),
    conn=Depends(connection),
):
    questions, versions, subjects = (
        db.table(name) for name in ("questions", "question_versions", "subjects")
    )
    policies = db.table("question_version_access_policies")
    statement = select(
        questions.c.code,
        questions.c.grade,
        versions.c.id,
        versions.c.question_id,
        versions.c.version,
        versions.c.reviewed_by,
        policies.c.minimum_plan_code,
        versions.c.question_type,
        versions.c.status,
        versions.c.difficulty,
        versions.c.content,
        subjects.c.name_vi.label("subject_name"),
    )
    statement = statement.select_from(
        questions.join(versions)
        .join(subjects)
        .outerjoin(policies, policies.c.question_version_id == versions.c.id)
    ).where(questions.c.grade == grade)
    if subject_code:
        statement = statement.where(subjects.c.code == subject_code)
    if search:
        statement = statement.where(
            questions.c.code.ilike("%" + search + "%")
            | versions.c.content["prompt"].as_string().ilike("%" + search + "%")
        )
    if status:
        statement = statement.where(versions.c.status == status)
    if question_type:
        statement = statement.where(versions.c.question_type == question_type)
    if minimum_plan_code:
        statement = statement.where(policies.c.minimum_plan_code == minimum_plan_code)
    if topic_id:
        statement = statement.where(questions.c.topic_id == topic_id)
    total = conn.execute(select(func.count()).select_from(statement.subquery())).scalar_one()
    return dict(
        total=total,
        page=page,
        items=conn.execute(statement.order_by(questions.c.code).offset((page - 1) * 20).limit(20))
        .mappings()
        .all(),
    )


@router.get("/admin/questions/{version_id}", response_model=dict, tags=["admin"])
def question_detail(version_id: UUID, user=Depends(admin_user), conn=Depends(connection)):
    from app.services.authoring import question_detail

    return question_detail(conn, version_id)


@router.get("/admin/assessments", response_model=list[out.AssessmentResponse], tags=["admin"])
def admin_assessments(grade: Grade = 4, user=Depends(admin_user), conn=Depends(connection)):
    rows = assessment_list(conn, grade, published_only=False)
    attempts = db.table("attempts")
    return [
        {
            **dict(row),
            **access.content_access(conn, user, "assessment", row["id"], grade),
            "attempt_count": conn.execute(
                select(func.count())
                .select_from(attempts)
                .where(attempts.c.assessment_id == row["id"])
            ).scalar_one(),
        }
        for row in rows
    ]


@router.get("/admin/curriculum", response_model=dict[str, list[dict]], tags=["admin"])
def curriculum(grade: Grade = 4, user=Depends(admin_user), conn=Depends(connection)):
    topics, lessons, skills, subjects = (
        db.table(name) for name in ("topics", "lessons", "skills", "subjects")
    )
    return dict(
        subjects=conn.execute(select(subjects)).mappings().all(),
        topics=conn.execute(select(topics).where(topics.c.grade == grade)).mappings().all(),
        lessons=conn.execute(select(lessons).join(topics).where(topics.c.grade == grade))
        .mappings()
        .all(),
        skills=conn.execute(select(skills).where(skills.c.grade == grade)).mappings().all(),
    )
