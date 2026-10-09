from datetime import timedelta

from sqlalchemy import and_, func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db
from app.services.access import eligible


def evidence_update(state: dict, correct: bool, difficulty: int, weight: float, at, hint_count=0):
    count = state.get("questions_attempted", 0) + 1
    old = float(state.get("mastery_score", 0))
    alpha = min(0.5, (0.15 + 0.05 * difficulty) * weight)
    mastery = float(correct) if count == 1 else (1 - alpha) * old + alpha * float(correct)
    accuracy = (
        float(correct)
        if count == 1
        else 0.7 * float(state.get("recent_accuracy", 0)) + 0.3 * float(correct)
    )
    hints = ((float(state.get("hint_usage_rate", 0)) * (count - 1)) + int(hint_count > 0)) / count
    interval = 1 if mastery < 0.5 else 3 if mastery < 0.8 else 7
    return dict(
        mastery_score=round(mastery, 4),
        confidence=round(min(1, count / 20), 4),
        questions_attempted=count,
        correct_count=state.get("correct_count", 0) + int(correct),
        recent_accuracy=round(accuracy, 4),
        hint_usage_rate=round(hints, 4),
        last_practiced_at=at,
        next_review_at=at + timedelta(days=interval),
        model_version="rule_v1",
    )


def rebuild_student(conn, student_id):
    """Replay theo thứ tự cố định; không xóa dữ liệu gốc và không tạo sự kiện mới."""
    attempts, answers, links, versions, mastery = (
        db.table(name)
        for name in (
            "attempts",
            "attempt_answers",
            "question_skills",
            "question_versions",
            "student_skill_mastery",
        )
    )
    records = (
        conn.execute(
            select(
                answers.c.is_correct,
                answers.c.hint_count,
                links.c.skill_id,
                links.c.weight,
                versions.c.difficulty,
                attempts.c.graded_at,
            )
            .select_from(
                answers.join(attempts, answers.c.attempt_id == attempts.c.id)
                .join(links, links.c.question_version_id == answers.c.question_version_id)
                .join(versions, versions.c.id == answers.c.question_version_id)
            )
            .where(
                attempts.c.student_id == student_id,
                attempts.c.status == "graded",
                answers.c.grading_status == "graded",
                answers.c.is_correct.is_not(None),
            )
            .order_by(attempts.c.graded_at, attempts.c.id, answers.c.assessment_item_id)
        )
        .mappings()
        .all()
    )
    states = {}
    for row in records:
        skill = row["skill_id"]
        states[skill] = evidence_update(
            states.get(skill, {}),
            row["is_correct"],
            row["difficulty"],
            float(row["weight"]),
            row["graded_at"],
            row["hint_count"],
        )
    for skill_id, state in states.items():
        statement = insert(mastery).values(student_id=student_id, skill_id=skill_id, **state)
        conn.execute(
            statement.on_conflict_do_update(
                index_elements=[mastery.c.student_id, mastery.c.skill_id], set_=state
            )
        )
    return states


def recommendations(conn, student_id, grade):
    rec, assessments, items, links, mastery, skills, prereqs, attempts = (
        db.table(name)
        for name in (
            "student_recommendations",
            "assessments",
            "assessment_items",
            "question_skills",
            "student_skill_mastery",
            "skills",
            "skill_prerequisites",
            "attempts",
        )
    )
    current = now()
    completed = (
        conn.execute(
            select(attempts.c.assessment_id)
            .where(
                attempts.c.student_id == student_id,
                attempts.c.status == "graded",
                attempts.c.graded_at > current - timedelta(hours=24),
            )
            .group_by(attempts.c.assessment_id)
            .having(func.count() >= 2)
        )
        .scalars()
        .all()
    )
    candidates = (
        conn.execute(
            select(
                assessments.c.id,
                assessments.c.title,
                skills.c.id.label("skill_id"),
                skills.c.name,
                mastery.c.mastery_score,
                mastery.c.next_review_at,
                mastery.c.confidence,
            )
            .select_from(
                assessments.join(items)
                .join(links, links.c.question_version_id == items.c.question_version_id)
                .join(skills, skills.c.id == links.c.skill_id)
                .outerjoin(
                    mastery,
                    and_(mastery.c.skill_id == skills.c.id, mastery.c.student_id == student_id),
                )
            )
            .where(
                assessments.c.grade == grade,
                assessments.c.status == "published",
                assessments.c.id.not_in(completed),
                select(func.count())
                .where(
                    attempts.c.student_id == student_id,
                    attempts.c.assessment_id == assessments.c.id,
                )
                .scalar_subquery()
                < assessments.c.max_attempts,
            )
            .distinct()
        )
        .mappings()
        .all()
    )
    learned = {row["skill_id"]: row for row in candidates}
    dependencies = {}
    for row in conn.execute(select(prereqs)).mappings():
        dependencies.setdefault(row["skill_id"], []).append(row["prerequisite_skill_id"])
    urgent_prerequisites = set()
    for row in candidates:
        if (
            row["mastery_score"] is not None
            and float(row["mastery_score"]) < 0.5
            and float(row["confidence"] or 0) >= 0.25
        ):
            urgent_prerequisites.update(
                p
                for p in dependencies.get(row["skill_id"], [])
                if p in learned and float(learned[p]["mastery_score"] or 0) < 0.5
            )

    def priority(row):
        score = float(row["mastery_score"]) if row["mastery_score"] is not None else 0.5
        due = row["next_review_at"] and row["next_review_at"] <= current
        blocked = any(
            float(learned[p]["mastery_score"] or 0) < 0.5
            for p in dependencies.get(row["skill_id"], [])
            if p in learned
        )
        return (
            row["skill_id"] not in urgent_prerequisites,
            blocked,
            not bool(due),
            score,
            str(row["id"]),
        )

    selected, used = [], set()
    for row in sorted(candidates, key=priority):
        if row["id"] in used:
            continue
        used.add(row["id"])
        if not eligible(conn, student_id, "assessment", row["id"], grade):
            continue
        sparse = row["confidence"] is None or float(row["confidence"]) < 0.25
        reason = (
            "warmup"
            if sparse
            else "review_due"
            if row["next_review_at"] and row["next_review_at"] <= current
            else "practice_skill"
        )
        explanation = (
            "Bắt đầu nhẹ nhàng để khám phá kiến thức của em."
            if sparse
            else f"Cùng ôn lại kỹ năng {row['name']} để ghi nhớ vững hơn nhé."
        )
        if row["skill_id"] in urgent_prerequisites:
            reason = "prerequisite"
            explanation = (
                f"Ôn kỹ năng nền tảng {row['name']} trước để bài tiếp theo dễ hiểu hơn nhé."
            )
        existing = conn.execute(
            select(rec.c.id).where(
                rec.c.student_id == student_id,
                rec.c.assessment_id == row["id"],
                rec.c.status.in_(["pending", "shown", "accepted"]),
            )
        ).scalar()
        if existing:
            conn.execute(
                rec.update()
                .where(rec.c.id == existing)
                .values(
                    skill_id=row["skill_id"],
                    reason_code=reason,
                    explanation=explanation,
                    expires_at=current + timedelta(days=1),
                )
            )
        else:
            conn.execute(
                insert(rec).values(
                    student_id=student_id,
                    assessment_id=row["id"],
                    skill_id=row["skill_id"],
                    reason_code=reason,
                    explanation=explanation,
                    priority=80 - len(selected) * 10,
                    expires_at=current + timedelta(days=1),
                )
            )
        selected.append(
            dict(
                assessment_id=row["id"],
                title=row["title"],
                explanation=explanation,
                reason_code=reason,
            )
        )
        if len(selected) == 5:
            break
    return selected


def rebuild_statistics(conn):
    """Upsert tổng hợp từ lịch sử đã chấm; không DELETE/TRUNCATE."""
    # Tuần tự hóa snapshot + upsert để hai học sinh nộp cùng lúc không ghi đè tổng cũ.
    conn.execute(text("SELECT pg_advisory_xact_lock(78249101)"))
    attempts, answers, assessments, question_stats, daily = (
        db.table(name)
        for name in (
            "attempts",
            "attempt_answers",
            "assessments",
            "question_statistics",
            "student_daily_statistics",
        )
    )
    joined = answers.join(attempts, attempts.c.id == answers.c.attempt_id)
    rows = conn.execute(
        select(
            answers.c.question_version_id,
            func.count().label("attempts_count"),
            func.count().filter(answers.c.is_correct.is_(True)).label("correct_count"),
            func.count().filter(answers.c.is_correct.is_(False)).label("incorrect_count"),
            func.avg(answers.c.response_time_ms).label("avg_response_time_ms"),
        )
        .select_from(joined)
        .where(attempts.c.status == "graded")
        .group_by(answers.c.question_version_id)
    ).mappings()
    for row in rows:
        values = dict(row)
        statement = insert(question_stats).values(**values)
        conn.execute(
            statement.on_conflict_do_update(
                index_elements=[question_stats.c.question_version_id], set_=values
            )
        )
    stat_date = func.date(func.timezone("Asia/Bangkok", attempts.c.graded_at))
    rows = conn.execute(
        select(
            attempts.c.student_id,
            stat_date.label("stat_date"),
            assessments.c.subject_id,
            func.sum(attempts.c.answered_count).label("questions_answered"),
            func.sum(attempts.c.correct_count).label("correct_answers"),
            func.count().label("assessments_completed"),
        )
        .select_from(attempts.join(assessments, attempts.c.assessment_id == assessments.c.id))
        .where(attempts.c.status == "graded")
        .group_by(attempts.c.student_id, stat_date, assessments.c.subject_id)
    ).mappings()
    for row in rows:
        values = dict(row)
        statement = insert(daily).values(**values)
        conn.execute(
            statement.on_conflict_do_update(
                index_elements=[daily.c.student_id, daily.c.stat_date, daily.c.subject_id],
                set_=values,
            )
        )
