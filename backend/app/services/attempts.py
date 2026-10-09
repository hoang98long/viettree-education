from datetime import timedelta
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db
from app.personalization.engine import rebuild_statistics, rebuild_student
from app.services import access
from app.services.grading import grade_answer, safe_content, validate_answer
from app.services.learning import update_targets


def lock_student(conn, student_id):
    table = db.table("student_profiles")
    profile = (
        conn.execute(select(table).where(table.c.student_id == student_id).with_for_update())
        .mappings()
        .first()
    )
    if not profile:
        raise HTTPException(403, "Chưa có hồ sơ học sinh")
    return profile


def published_assessment(conn, assessment_id, grade=None):
    table = db.table("assessments")
    row = (
        conn.execute(
            select(table)
            .where(table.c.id == assessment_id, table.c.status == "published")
            .with_for_update(read=True)
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài luyện tập đã xuất bản")
    if grade is not None and row["grade"] != grade:
        raise HTTPException(403, "Bài luyện tập không thuộc lớp của em")
    return row


def assign_self(conn, student_id, assessment_id):
    profile = lock_student(conn, student_id)
    assessment = published_assessment(conn, assessment_id, profile["current_grade"])
    access.authorize_content(
        conn, access.student_actor(student_id), "assessment", assessment_id, assessment["grade"]
    )
    table = db.table("student_assignments")
    existing = (
        conn.execute(
            select(table).where(
                table.c.student_id == student_id,
                table.c.assessment_id == assessment_id,
                table.c.assignment_source == "self",
                table.c.status.not_in(["cancelled", "expired"]),
            )
        )
        .mappings()
        .first()
    )
    if existing:
        return dict(existing)
    return dict(
        conn.execute(
            insert(table)
            .values(student_id=student_id, assessment_id=assessment_id, assignment_source="self")
            .returning(table)
        )
        .mappings()
        .one()
    )


def check_window(assignment, assessment, started_at=None):
    current = now()
    if assignment["status"] in ("cancelled", "expired"):
        raise HTTPException(409, "Bài được giao đã đóng")
    if assignment["available_at"] > current:
        raise HTTPException(409, "Bài được giao chưa đến giờ mở")
    deadlines = [assignment["due_at"]] if assignment["due_at"] else []
    if started_at and assessment["time_limit_seconds"]:
        deadlines.append(started_at + timedelta(seconds=assessment["time_limit_seconds"]))
    if deadlines and min(deadlines) < current:
        raise HTTPException(409, "Đã hết thời gian làm bài. Em hãy chọn một bài luyện tập khác")
    return min(deadlines).isoformat() if deadlines else None


def start_attempt(conn, student_id, assignment_id):
    profile = lock_student(conn, student_id)
    assignments, attempts, items, versions, questions = (
        db.table(name)
        for name in (
            "student_assignments",
            "attempts",
            "assessment_items",
            "question_versions",
            "questions",
        )
    )
    assignment = (
        conn.execute(
            select(assignments)
            .where(assignments.c.id == assignment_id, assignments.c.student_id == student_id)
            .with_for_update()
        )
        .mappings()
        .first()
    )
    if not assignment:
        raise HTTPException(404, "Không tìm thấy bài được giao")
    assessment = published_assessment(conn, assignment["assessment_id"], profile["current_grade"])
    check_window(assignment, assessment)
    existing = (
        conn.execute(
            select(attempts).where(
                attempts.c.student_id == student_id,
                attempts.c.assessment_id == assessment["id"],
                attempts.c.status == "in_progress",
            )
        )
        .mappings()
        .first()
    )
    if existing:
        check_window(assignment, assessment, existing["started_at"])
        access.authorize_attempt(conn, existing)
        update_targets(conn, student_id, assessment_id=assessment["id"], completed=False)
        return {"id": existing["id"], "resumed": True}
    access.authorize_content(
        conn, access.student_actor(student_id), "assessment", assessment["id"], assessment["grade"]
    )
    count = conn.execute(
        select(func.count())
        .select_from(attempts)
        .where(attempts.c.student_id == student_id, attempts.c.assessment_id == assessment["id"])
    ).scalar_one()
    if count >= assessment["max_attempts"]:
        raise HTTPException(409, "Em đã dùng hết lượt của bài này. Hãy chọn bài khác nhé")
    configured = (
        conn.execute(
            select(
                items.c.id,
                versions.c.status,
                versions.c.published_at,
                versions.c.question_type,
                questions.c.grade,
                questions.c.subject_id,
                questions.c.is_active,
            )
            .select_from(items.join(versions).join(questions))
            .where(items.c.assessment_id == assessment["id"])
        )
        .mappings()
        .all()
    )
    if not configured or any(
        row["status"] not in ("published", "archived")
        or row["published_at"] is None
        or not row["is_active"]
        or row["grade"] != assessment["grade"]
        or row["subject_id"] != assessment["subject_id"]
        or row["question_type"]
        not in ("single_choice", "multiple_choice", "fill_blank", "ordering")
        for row in configured
    ):
        raise HTTPException(409, "Bài luyện tập chưa sẵn sàng để chấm tự động")
    attempt_no = conn.execute(
        select(func.coalesce(func.max(attempts.c.attempt_no), 0) + 1).where(
            attempts.c.assignment_id == assignment_id
        )
    ).scalar_one()
    started_at = now()
    attempt_id = conn.execute(
        insert(attempts)
        .values(
            assignment_id=assignment_id,
            student_id=student_id,
            assessment_id=assessment["id"],
            attempt_no=attempt_no,
            started_at=started_at,
        )
        .returning(attempts.c.id)
    ).scalar_one()
    access.grant_attempt(conn, student_id, attempt_id, assessment, assignment, started_at)
    conn.execute(
        assignments.update().where(assignments.c.id == assignment_id).values(status="in_progress")
    )
    conn.execute(
        insert(db.table("learning_events")).values(
            student_id=student_id, event_type="attempt_started", attempt_id=attempt_id
        )
    )
    update_targets(conn, student_id, assessment_id=assessment["id"], completed=False)
    return {"id": attempt_id, "resumed": False}


def owned_attempt(conn, user, attempt_id: UUID, write=False):
    if write:
        lock_student(conn, user["id"])
    table = db.table("attempts")
    statement = select(table).where(table.c.id == attempt_id)
    if write:
        statement = statement.with_for_update()
    row = conn.execute(statement).mappings().first()
    if not row or (row["student_id"] != user["id"] and (write or "admin" not in user["roles"])):
        raise HTTPException(404, "Không tìm thấy bài làm")
    return row


def attempt_items(conn, assessment_id):
    items, versions = db.table("assessment_items"), db.table("question_versions")
    return (
        conn.execute(
            select(
                items.c.id,
                items.c.question_version_id,
                items.c.position,
                items.c.points,
                versions.c.question_type,
                versions.c.content,
                versions.c.grading,
                versions.c.explanation,
            )
            .select_from(items.join(versions))
            .where(items.c.assessment_id == assessment_id)
            .order_by(items.c.position)
        )
        .mappings()
        .all()
    )


def get_attempt(conn, user, attempt_id):
    attempt = owned_attempt(conn, user, attempt_id)
    if "admin" not in user["roles"]:
        access.authorize_attempt(conn, attempt)
    assessments, assignments, answers = (
        db.table(name) for name in ("assessments", "student_assignments", "attempt_answers")
    )
    assessment = (
        conn.execute(select(assessments).where(assessments.c.id == attempt["assessment_id"]))
        .mappings()
        .one()
    )
    assignment = (
        conn.execute(select(assignments).where(assignments.c.id == attempt["assignment_id"]))
        .mappings()
        .one()
    )
    deadlines = [assignment["due_at"]] if assignment["due_at"] else []
    if assessment["time_limit_seconds"]:
        deadlines.append(
            attempt["started_at"] + timedelta(seconds=assessment["time_limit_seconds"])
        )
    saved = {
        row["assessment_item_id"]: row["student_answer"]
        for row in conn.execute(
            select(answers.c.assessment_item_id, answers.c.student_answer).where(
                answers.c.attempt_id == attempt_id
            )
        ).mappings()
    }
    grants = db.table("attempt_access_grants")
    allowed_until = conn.execute(
        select(grants.c.allowed_until).where(grants.c.attempt_id == attempt_id)
    ).scalar()
    if (
        allowed_until
        and access.resolve_membership(conn, attempt["student_id"])["plan_code"] != "vip"
    ):
        deadlines.append(allowed_until)
    return dict(
        id=attempt["id"],
        assignment_id=attempt["assignment_id"],
        assessment_id=attempt["assessment_id"],
        title=assessment["title"],
        status=attempt["status"],
        started_at=attempt["started_at"].isoformat(),
        deadline=min(deadlines).isoformat() if deadlines else None,
        items=[
            dict(
                id=item["id"],
                question_version_id=item["question_version_id"],
                position=item["position"],
                points=item["points"],
                question_type=item["question_type"],
                content=safe_content(item["content"]),
                answer=saved.get(item["id"]),
            )
            for item in attempt_items(conn, attempt["assessment_id"])
        ],
    )


def writable_attempt(conn, user, attempt_id):
    attempt = owned_attempt(conn, user, attempt_id, write=True)
    if attempt["status"] != "in_progress":
        raise HTTPException(409, "Bài đã nộp, không thể thay đổi câu trả lời")
    access.authorize_attempt(conn, attempt)
    assessment = published_assessment(conn, attempt["assessment_id"])
    assignments = db.table("student_assignments")
    assignment = (
        conn.execute(select(assignments).where(assignments.c.id == attempt["assignment_id"]))
        .mappings()
        .one()
    )
    check_window(assignment, assessment, attempt["started_at"])
    return attempt


def save_answer(conn, user, attempt_id, item_id, payload):
    attempt = writable_attempt(conn, user, attempt_id)
    item = next(
        (row for row in attempt_items(conn, attempt["assessment_id"]) if row["id"] == item_id), None
    )
    if not item:
        raise HTTPException(404, "Câu hỏi không thuộc bài làm")
    answer = validate_answer(item["question_type"], item["content"], payload.answer)
    table = db.table("attempt_answers")
    values = dict(
        attempt_id=attempt_id,
        assessment_id=attempt["assessment_id"],
        assessment_item_id=item_id,
        question_version_id=item["question_version_id"],
        student_answer=answer,
        response_time_ms=payload.response_time_ms,
        answered_at=now(),
    )
    statement = (
        insert(table)
        .values(**values)
        .on_conflict_do_update(
            index_elements=[table.c.attempt_id, table.c.assessment_item_id, table.c.answer_no],
            set_={
                "student_answer": answer,
                "response_time_ms": payload.response_time_ms,
                "answered_at": now(),
            },
        )
    )
    conn.execute(statement)
    return {"saved": True}


def result(conn, user, attempt_id):
    attempt = owned_attempt(conn, user, attempt_id)
    if attempt["status"] != "graded":
        raise HTTPException(409, "Em cần nộp bài trước khi xem kết quả")
    answers = db.table("attempt_answers")
    saved = {
        row["assessment_item_id"]: row
        for row in conn.execute(
            select(answers).where(answers.c.attempt_id == attempt_id)
        ).mappings()
    }
    return dict(
        id=attempt_id,
        total_score=attempt["total_score"],
        max_score=attempt["max_score"],
        correct_count=attempt["correct_count"],
        answered_count=attempt["answered_count"],
        graded_at=attempt["graded_at"],
        items=[
            dict(
                id=item["id"],
                position=item["position"],
                content=safe_content(item["content"]),
                question_type=item["question_type"],
                student_answer=saved[item["id"]]["student_answer"],
                is_correct=saved[item["id"]]["is_correct"],
                score=saved[item["id"]]["score"],
                points=item["points"],
                explanation=item["explanation"],
                grading=item["grading"],
            )
            for item in attempt_items(conn, attempt["assessment_id"])
        ],
    )


def submit(conn, user, attempt_id):
    attempt = owned_attempt(conn, user, attempt_id, write=True)
    if attempt["status"] == "graded":
        return result(conn, user, attempt_id)
    writable_attempt(conn, user, attempt_id)
    answers, attempts, assignments = (
        db.table(name) for name in ("attempt_answers", "attempts", "student_assignments")
    )
    saved = {
        row["assessment_item_id"]: row
        for row in conn.execute(
            select(answers).where(answers.c.attempt_id == attempt_id)
        ).mappings()
    }
    total, maximum, correct_count, answered_count = 0, 0, 0, 0
    for item in attempt_items(conn, attempt["assessment_id"]):
        existing = saved.get(item["id"])
        answer = existing["student_answer"] if existing else None
        correct = grade_answer(item["question_type"], item["grading"], answer)
        points = item["points"] if correct else 0
        total += points
        maximum += item["points"]
        correct_count += int(bool(correct))
        answered_count += int(existing is not None)
        values = dict(
            attempt_id=attempt_id,
            assessment_id=attempt["assessment_id"],
            assessment_item_id=item["id"],
            question_version_id=item["question_version_id"],
            student_answer=answer or {},
            is_correct=correct,
            score=points,
            grading_status="graded",
            feedback={"message": "Rất tốt!" if correct else "Cùng xem lời giải để hiểu hơn nhé."},
        )
        statement = (
            insert(answers)
            .values(**values)
            .on_conflict_do_update(
                index_elements=[
                    answers.c.attempt_id,
                    answers.c.assessment_item_id,
                    answers.c.answer_no,
                ],
                set_={
                    key: values[key]
                    for key in ("is_correct", "score", "grading_status", "feedback")
                },
            )
        )
        conn.execute(statement)
    at = now()
    conn.execute(
        attempts.update()
        .where(attempts.c.id == attempt_id)
        .values(
            status="graded",
            total_score=total,
            max_score=maximum,
            correct_count=correct_count,
            answered_count=answered_count,
            submitted_at=at,
            graded_at=at,
        )
    )
    conn.execute(
        assignments.update()
        .where(assignments.c.id == attempt["assignment_id"])
        .values(status="completed", completed_at=at)
    )
    rec = db.table("student_recommendations")
    conn.execute(
        rec.update()
        .where(
            rec.c.student_id == user["id"],
            rec.c.assessment_id == attempt["assessment_id"],
            rec.c.status.in_(["pending", "shown", "accepted"]),
        )
        .values(status="completed")
    )
    assessment = published_assessment(conn, attempt["assessment_id"])
    if assessment["lesson_id"]:
        progress = db.table("student_lesson_progress")
        statement = insert(progress).values(
            student_id=user["id"],
            lesson_id=assessment["lesson_id"],
            status="completed",
            completion_ratio=1,
            first_started_at=attempt["started_at"],
            completed_at=at,
            last_accessed_at=at,
        )
        conn.execute(
            statement.on_conflict_do_update(
                index_elements=[progress.c.student_id, progress.c.lesson_id],
                set_={
                    "status": "completed",
                    "completion_ratio": 1,
                    "completed_at": at,
                    "last_accessed_at": at,
                },
            )
        )
    conn.execute(
        insert(db.table("learning_events")).values(
            student_id=user["id"],
            event_type="attempt_graded",
            attempt_id=attempt_id,
            properties={"model_version": "rule_v1"},
        )
    )
    update_targets(conn, user["id"], assessment_id=attempt["assessment_id"])
    if assessment["lesson_id"]:
        update_targets(conn, user["id"], lesson_id=assessment["lesson_id"])
    rebuild_student(conn, user["id"])
    rebuild_statistics(conn)
    return result(conn, user, attempt_id)
