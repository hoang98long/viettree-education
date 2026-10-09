"""Membership is independent from roles. All decisions use server-side state."""

from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db


def resolve_membership(conn, student_id):
    members, plans, features = (
        db.table(name)
        for name in ("student_memberships", "membership_plans", "membership_plan_features")
    )
    row = conn.execute(select(members).where(members.c.student_id == student_id)).mappings().first()
    at = now()
    vip_enabled = conn.execute(select(plans.c.is_active).where(plans.c.code == "vip")).scalar()
    active = bool(
        row
        and row["status"] == "active"
        and row["starts_at"] <= at < row["ends_at"]
        and vip_enabled
    )
    plan = "vip" if active else "free"
    status = (
        "active"
        if active
        else "free"
        if not row
        else "revoked"
        if row["status"] == "revoked"
        else "expired"
    )
    return {
        "student_id": student_id,
        "plan_code": plan,
        "status": status,
        "subscription_plan_code": row["plan_code"] if row else None,
        "starts_at": row["starts_at"] if row else None,
        "ends_at": row["ends_at"] if row else None,
        "features": list(
            conn.execute(
                select(features.c.feature_code)
                .join(plans)
                .where(features.c.plan_code == plan, plans.c.is_active.is_(True))
                .order_by(features.c.feature_code)
            ).scalars()
        ),
    }


def denied(
    code="MEMBERSHIP_REQUIRED",
    message="Bài này nằm trong gói VIP. Em vẫn có thể học các bài miễn phí.",
):
    raise HTTPException(
        403,
        {
            "code": code,
            "message": message,
            "required_plan": "vip" if code == "MEMBERSHIP_REQUIRED" else None,
        },
    )


def require_feature(conn, student_id, feature):
    membership = resolve_membership(conn, student_id)
    if feature not in membership["features"]:
        denied()
    return membership


def policy(conn, kind, resource_id):
    policies = db.table("content_access_policies")
    row = (
        conn.execute(select(policies).where(policies.c[f"{kind}_id"] == resource_id))
        .mappings()
        .first()
    )
    if not row:
        return None
    result = dict(row)
    if kind == "assessment":
        assessments, items = db.table("assessments"), db.table("assessment_items")
        assessment = conn.execute(
            select(assessments.c.lesson_id).where(assessments.c.id == resource_id)
        ).first()
        if assessment and assessment.lesson_id:
            lesson_policy = policy(conn, "lesson", assessment.lesson_id)
            if not lesson_policy:
                return None
            if lesson_policy["minimum_plan_code"] == "vip":
                result["minimum_plan_code"] = "vip"
        # A free assessment must not leak question versions used by a VIP assessment/lesson.
        own_versions = select(items.c.question_version_id).where(
            items.c.assessment_id == resource_id
        )
        question_policies = db.table("question_version_access_policies")
        explicit_vip = conn.execute(
            select(question_policies.c.question_version_id)
            .where(
                question_policies.c.question_version_id.in_(own_versions),
                question_policies.c.minimum_plan_code == "vip",
            )
            .limit(1)
        ).first()
        unclassified = conn.execute(
            select(items.c.id)
            .outerjoin(
                question_policies,
                question_policies.c.question_version_id == items.c.question_version_id,
            )
            .where(
                items.c.assessment_id == resource_id,
                question_policies.c.question_version_id.is_(None),
            )
            .limit(1)
        ).first()
        if unclassified:
            return None
        other_items = items.alias("other_items")
        other_policy = policies.alias("other_policy")
        lesson_policy = policies.alias("linked_lesson_policy")
        premium_versions = conn.execute(
            select(other_items.c.id)
            .select_from(
                other_items.join(assessments, assessments.c.id == other_items.c.assessment_id)
                .outerjoin(other_policy, other_policy.c.assessment_id == assessments.c.id)
                .outerjoin(lesson_policy, lesson_policy.c.lesson_id == assessments.c.lesson_id)
            )
            .where(
                other_items.c.question_version_id.in_(own_versions),
                (other_policy.c.minimum_plan_code == "vip")
                | (lesson_policy.c.minimum_plan_code == "vip"),
            )
            .limit(1)
        ).first()
        lesson_questions = db.table("lesson_questions")
        premium_lesson_version = conn.execute(
            select(lesson_questions.c.lesson_id)
            .join(policies, policies.c.lesson_id == lesson_questions.c.lesson_id)
            .where(
                lesson_questions.c.question_version_id.in_(own_versions),
                policies.c.minimum_plan_code == "vip",
            )
            .limit(1)
        ).first()
        if explicit_vip or premium_versions or premium_lesson_version:
            result["minimum_plan_code"] = "vip"
    return result


def content_access(conn, user, kind, resource_id, grade=None, membership=None):
    record = policy(conn, kind, resource_id)
    if not record:
        return {
            "minimum_plan_code": None,
            "learning_level": "basic",
            "locked": True,
            "lock_reason": "POLICY_NOT_READY",
        }
    reason = None
    if "admin" not in user["roles"]:
        if "student" not in user["roles"]:
            reason = "ROLE_REQUIRED"
        else:
            profiles = db.table("student_profiles")
            current_grade = conn.execute(
                select(profiles.c.current_grade).where(profiles.c.student_id == user["id"])
            ).scalar()
            if grade is not None and grade != current_grade:
                reason = "GRADE_REQUIRED"
            else:
                membership = membership or resolve_membership(conn, user["id"])
                feature = ("learning" if kind == "lesson" else "practice") + (
                    ".advanced" if record["minimum_plan_code"] == "vip" else ".basic"
                )
                if feature not in membership["features"]:
                    reason = "MEMBERSHIP_REQUIRED"
                if kind == "assessment" and record["minimum_plan_code"] == "vip":
                    assessments = db.table("assessments")
                    assessment_type = conn.execute(
                        select(assessments.c.assessment_type).where(assessments.c.id == resource_id)
                    ).scalar()
                    if (
                        assessment_type == "quiz"
                        and "practice.challenge" not in membership["features"]
                    ):
                        reason = "MEMBERSHIP_REQUIRED"
    return {
        "minimum_plan_code": record["minimum_plan_code"],
        "learning_level": record["learning_level"],
        "locked": bool(reason),
        "lock_reason": reason,
    }


def authorize_content(conn, user, kind, resource_id, grade=None):
    access = content_access(conn, user, kind, resource_id, grade)
    if access["locked"]:
        code = access["lock_reason"]
        if code == "MEMBERSHIP_REQUIRED":
            denied()
        denied(code, "Bài học chưa khả dụng cho tài khoản hoặc lớp của em.")
    return access


def student_actor(student_id):
    return {"id": student_id, "roles": ["student"]}


def eligible(conn, student_id, kind, resource_id, grade):
    return not content_access(conn, student_actor(student_id), kind, resource_id, grade)["locked"]


def grant_attempt(conn, student_id, attempt_id, assessment, assignment, started_at):
    if policy(conn, "assessment", assessment["id"])["minimum_plan_code"] != "vip":
        return
    membership = resolve_membership(conn, student_id)
    if membership["plan_code"] != "vip":
        denied()
    deadlines = [membership["ends_at"] + timedelta(minutes=60)]
    if assignment["due_at"]:
        deadlines.append(assignment["due_at"])
    if assessment["time_limit_seconds"]:
        deadlines.append(started_at + timedelta(seconds=assessment["time_limit_seconds"]))
    table = db.table("attempt_access_grants")
    conn.execute(
        insert(table)
        .values(
            attempt_id=attempt_id,
            membership_student_id=student_id,
            allowed_until=min(deadlines),
            granted_at=started_at,
        )
        .on_conflict_do_nothing(index_elements=[table.c.attempt_id])
    )


def authorize_attempt(conn, attempt):
    # Result/history access is governed by owner, and stays available after membership expiry.
    if attempt["status"] == "graded":
        return
    policies = policy(conn, "assessment", attempt["assessment_id"])
    if not policies:
        denied("POLICY_NOT_READY", "Chính sách bài học chưa sẵn sàng.")
    grants = db.table("attempt_access_grants")
    grant = (
        conn.execute(
            select(grants).where(
                grants.c.attempt_id == attempt["id"],
                grants.c.membership_student_id == attempt["student_id"],
            )
        )
        .mappings()
        .first()
    )
    # Revocation is permanent for an already-started premium attempt, even after re-granting VIP.
    if grant and grant["revoked_at"]:
        denied("MEMBERSHIP_REVOKED", "Quyền VIP cho bài làm này đã được thu hồi.")
    membership = resolve_membership(conn, attempt["student_id"])
    if policies["minimum_plan_code"] == "free":
        return
    if not content_access(
        conn,
        student_actor(attempt["student_id"]),
        "assessment",
        attempt["assessment_id"],
        membership=membership,
    )["locked"]:
        return
    if (
        grant
        and membership["status"] == "expired"
        and membership["ends_at"] <= now()
        and grant["allowed_until"] > now()
    ):
        return
    denied()
