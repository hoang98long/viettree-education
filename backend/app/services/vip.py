"""VIP tools use only the student's own graded history and live membership checks."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import Date, func, select

from app.core.security import now
from app.db import db
from app.services import access
from app.services.grading import grade_answer, safe_content, validate_answer


def profile(conn, student_id):
    profiles = db.table("student_profiles")
    row = conn.execute(
        select(profiles.c.current_grade).where(profiles.c.student_id == student_id)
    ).first()
    if not row:
        raise HTTPException(404, "Không tìm thấy hồ sơ học sinh")
    return row.current_grade


def subject_filter(conn, code):
    if not code:
        return None
    subjects = db.table("subjects")
    identifier = conn.execute(
        select(subjects.c.id).where(subjects.c.code == code, subjects.c.is_active.is_(True))
    ).scalar()
    if identifier is None:
        raise HTTPException(404, "Không tìm thấy môn học")
    return identifier


def library(conn, user):
    membership = access.require_feature(conn, user["id"], "vip.library")
    grade = profile(conn, user["id"])
    lessons, topics, subjects, policies, progress = (
        db.table(name)
        for name in (
            "lessons",
            "topics",
            "subjects",
            "content_access_policies",
            "student_lesson_progress",
        )
    )
    rows = conn.execute(
        select(
            lessons.c.id,
            lessons.c.title,
            lessons.c.estimated_minutes,
            subjects.c.code.label("subject_code"),
            subjects.c.name_vi.label("subject_name"),
            topics.c.title.label("topic_title"),
            func.coalesce(progress.c.status, "not_started").label("progress_status"),
        )
        .select_from(
            lessons.join(topics)
            .join(subjects)
            .join(policies, policies.c.lesson_id == lessons.c.id)
            .outerjoin(
                progress,
                (progress.c.lesson_id == lessons.c.id) & (progress.c.student_id == user["id"]),
            )
        )
        .where(
            lessons.c.status == "published",
            topics.c.grade == grade,
            topics.c.is_active.is_(True),
            subjects.c.is_active.is_(True),
            policies.c.minimum_plan_code == "vip",
        )
        .order_by(subjects.c.sort_order, topics.c.sort_order, lessons.c.sort_order, lessons.c.id)
    ).mappings()
    return {
        "grade": grade,
        "membership": membership,
        "lessons": [
            dict(row)
            for row in rows
            if not access.content_access(conn, user, "lesson", row["id"], grade, membership)[
                "locked"
            ]
        ],
    }


def mistake_query(conn, student_id, subject_code=None):
    grade = profile(conn, student_id)
    subject_id = subject_filter(conn, subject_code)
    answers, attempts, versions, questions, assessments, subjects = (
        db.table(name)
        for name in (
            "attempt_answers",
            "attempts",
            "question_versions",
            "questions",
            "assessments",
            "subjects",
        )
    )
    # Rank before selecting incorrect answers: a later correct attempt removes an old mistake.
    latest = (
        select(
            answers.c.id,
            func.row_number()
            .over(
                partition_by=answers.c.question_version_id,
                order_by=(
                    attempts.c.graded_at.desc(),
                    attempts.c.id.desc(),
                    answers.c.answer_no.desc(),
                    answers.c.id.desc(),
                ),
            )
            .label("position"),
        )
        .select_from(answers.join(attempts, attempts.c.id == answers.c.attempt_id))
        .where(
            attempts.c.student_id == student_id,
            attempts.c.status == "graded",
            answers.c.grading_status == "graded",
        )
        .subquery()
    )
    statement = (
        select(
            answers.c.id,
            answers.c.attempt_id,
            answers.c.question_version_id,
            answers.c.student_answer,
            versions.c.content,
            versions.c.question_type,
            versions.c.grading,
            versions.c.explanation,
            attempts.c.graded_at,
            assessments.c.title.label("assessment_title"),
            subjects.c.code.label("subject_code"),
            subjects.c.name_vi.label("subject_name"),
        )
        .select_from(
            answers.join(latest, latest.c.id == answers.c.id)
            .join(attempts, attempts.c.id == answers.c.attempt_id)
            .join(versions, versions.c.id == answers.c.question_version_id)
            .join(questions, questions.c.id == versions.c.question_id)
            .join(assessments, assessments.c.id == attempts.c.assessment_id)
            .join(subjects, subjects.c.id == questions.c.subject_id)
        )
        .where(latest.c.position == 1, answers.c.is_correct.is_(False), questions.c.grade == grade)
    )
    if subject_id:
        statement = statement.where(questions.c.subject_id == subject_id)
    return statement


def mistakes(conn, student_id, subject_code=None, page=1):
    access.require_feature(conn, student_id, "review.mistakes")
    statement = mistake_query(conn, student_id, subject_code)
    total = conn.execute(select(func.count()).select_from(statement.subquery())).scalar_one()
    rows = conn.execute(
        statement.order_by(
            statement.selected_columns.graded_at.desc(), statement.selected_columns.id
        )
        .offset((page - 1) * 20)
        .limit(20)
    ).mappings()
    return {
        "total": total,
        "page": page,
        "page_size": 20,
        "items": [
            {
                key: (safe_content(value) if key == "content" else value)
                for key, value in row.items()
                if key not in ("grading", "explanation")
            }
            for row in rows
        ],
    }


def check_mistake(conn, student_id, answer_id, payload):
    access.require_feature(conn, student_id, "review.mistakes")
    statement = mistake_query(conn, student_id)
    row = (
        conn.execute(statement.where(db.table("attempt_answers").c.id == answer_id))
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy câu cần ôn của em")
    answer = validate_answer(row["question_type"], row["content"], payload.answer)
    return {
        "is_correct": bool(grade_answer(row["question_type"], row["grading"], answer)),
        "explanation": row["explanation"],
        # Already graded own question. Never exposes another student's answer or new bank items.
        "grading": row["grading"],
        "affects_score": False,
    }


def report(conn, student_id, days=7):
    access.require_feature(conn, student_id, "reports.personal")
    grade = profile(conn, student_id)
    at = now()
    local_today = at.astimezone(ZoneInfo("Asia/Bangkok")).date()
    start = datetime.combine(
        local_today - timedelta(days=days - 1), time.min, ZoneInfo("Asia/Bangkok")
    )
    attempts, assessments, subjects, progress, lessons, topics = (
        db.table(name)
        for name in (
            "attempts",
            "assessments",
            "subjects",
            "student_lesson_progress",
            "lessons",
            "topics",
        )
    )
    own = attempts.join(assessments, assessments.c.id == attempts.c.assessment_id)
    conditions = (
        attempts.c.student_id == student_id,
        attempts.c.status == "graded",
        assessments.c.grade == grade,
    )

    def totals(begin, end):
        row = (
            conn.execute(
                select(
                    func.count().label("attempt_count"),
                    func.coalesce(func.sum(attempts.c.total_score), 0).label("earned"),
                    func.coalesce(func.sum(attempts.c.max_score), 0).label("possible"),
                )
                .select_from(own)
                .where(*conditions, attempts.c.graded_at >= begin, attempts.c.graded_at < end)
            )
            .mappings()
            .one()
        )
        return {
            "attempt_count": row["attempt_count"],
            "score_percent": round(float(row["earned"] / row["possible"] * 100), 1)
            if row["possible"]
            else None,
        }

    current = totals(start, at)
    previous = totals(start - timedelta(days=days), start)
    completed = conn.execute(
        select(func.count())
        .select_from(progress.join(lessons).join(topics))
        .where(
            progress.c.student_id == student_id,
            topics.c.grade == grade,
            progress.c.status == "completed",
            progress.c.completed_at >= start,
            progress.c.completed_at < at,
        )
    ).scalar_one()
    day = func.timezone("Asia/Bangkok", attempts.c.graded_at).cast(Date)
    daily_rows = conn.execute(
        select(
            day.label("date"),
            func.count().label("attempt_count"),
            func.sum(attempts.c.total_score).label("earned"),
            func.sum(attempts.c.max_score).label("possible"),
        )
        .select_from(own)
        .where(*conditions, attempts.c.graded_at >= start, attempts.c.graded_at < at)
        .group_by(day)
    ).mappings()
    daily_map = {row["date"]: row for row in daily_rows}
    daily = []
    for offset in range(days):
        date = start.date() + timedelta(days=offset)
        row = daily_map.get(date)
        daily.append(
            {
                "date": date,
                "attempt_count": row["attempt_count"] if row else 0,
                "score_percent": round(float(row["earned"] / row["possible"] * 100), 1)
                if row and row["possible"]
                else None,
            }
        )
    subject_rows = conn.execute(
        select(
            subjects.c.code.label("subject_code"),
            subjects.c.name_vi.label("subject_name"),
            func.count().label("attempt_count"),
            func.sum(attempts.c.total_score).label("earned"),
            func.sum(attempts.c.max_score).label("possible"),
        )
        .select_from(own.join(subjects, subjects.c.id == assessments.c.subject_id))
        .where(
            *conditions,
            attempts.c.graded_at >= start,
            attempts.c.graded_at < at,
        )
        .group_by(subjects.c.code, subjects.c.name_vi)
        .order_by(subjects.c.code)
    ).mappings()
    mastery, skills = db.table("student_skill_mastery"), db.table("skills")
    weak = conn.execute(
        select(
            skills.c.id.label("skill_id"),
            skills.c.name,
            subjects.c.name_vi.label("subject_name"),
            mastery.c.mastery_score,
            mastery.c.confidence,
            mastery.c.questions_attempted,
        )
        .select_from(mastery.join(skills).join(subjects, subjects.c.id == skills.c.subject_id))
        .where(
            mastery.c.student_id == student_id,
            skills.c.grade == grade,
            mastery.c.questions_attempted >= 5,
            mastery.c.mastery_score < 0.7,
        )
        .order_by(mastery.c.mastery_score, skills.c.id)
        .limit(5)
    ).mappings()
    users = db.table("users")
    name = conn.execute(select(users.c.display_name).where(users.c.id == student_id)).scalar_one()
    return {
        "student_name": name,
        "grade": grade,
        "days": days,
        "starts_at": start,
        "ends_at": at,
        **current,
        "previous": previous,
        "completed_lessons": completed,
        "active_days": sum(row["attempt_count"] > 0 for row in daily),
        "daily": daily,
        "subjects": [
            {key: value for key, value in row.items() if key not in ("earned", "possible")}
            | {
                "score_percent": round(float(row["earned"] / row["possible"] * 100), 1)
                if row["possible"]
                else None,
            }
            for row in subject_rows
        ],
        "weak_skills": [dict(row) for row in weak],
    }
