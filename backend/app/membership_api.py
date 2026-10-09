from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app import schemas as out
from app.core.security import admin_user, current_user, now, require_role, student_user
from app.db import connection, db
from app.services.access import content_access, resolve_membership
from app.services.memberships import change_membership, membership_history

router = APIRouter(prefix="/api/v1", tags=["membership"])


@router.get("/membership/plans", response_model=list[out.MembershipPlanResponse])
def plans(conn=Depends(connection)):
    plans, features = db.table("membership_plans"), db.table("membership_plan_features")
    return [
        {
            **dict(row),
            "features": list(
                conn.execute(
                    select(features.c.feature_code)
                    .where(features.c.plan_code == row["code"])
                    .order_by(features.c.feature_code)
                ).scalars()
            ),
        }
        for row in conn.execute(
            select(plans).where(plans.c.is_active.is_(True)).order_by(plans.c.code)
        ).mappings()
    ]


@router.get("/students/me/membership", response_model=out.MembershipResponse)
def student_membership(user=Depends(student_user), conn=Depends(connection)):
    return resolve_membership(conn, user["id"])


@router.get("/guardian/students", response_model=list[dict])
def guardian_students(user=Depends(require_role("guardian")), conn=Depends(connection)):
    links, users, profiles = (
        db.table("guardian_students"),
        db.table("users"),
        db.table("student_profiles"),
    )
    return [
        dict(row)
        for row in conn.execute(
            select(users.c.id, users.c.display_name, profiles.c.current_grade)
            .select_from(
                links.join(users, users.c.id == links.c.student_id).join(
                    profiles, profiles.c.student_id == links.c.student_id
                )
            )
            .where(links.c.guardian_user_id == user["id"], links.c.verified_at.is_not(None))
        ).mappings()
    ]


@router.get("/guardian/students/{student_id}/membership", response_model=out.MembershipResponse)
def guardian_membership(
    student_id: UUID, user=Depends(require_role("guardian")), conn=Depends(connection)
):
    links = db.table("guardian_students")
    if not conn.execute(
        select(links.c.student_id).where(
            links.c.guardian_user_id == user["id"],
            links.c.student_id == student_id,
            links.c.verified_at.is_not(None),
        )
    ).first():
        raise HTTPException(404, "Không tìm thấy học sinh được liên kết")
    return resolve_membership(conn, student_id)


@router.get("/admin/students/{student_id}/membership", response_model=out.MembershipResponse)
def admin_membership(student_id: UUID, user=Depends(admin_user), conn=Depends(connection)):
    profiles = db.table("student_profiles")
    if not conn.execute(
        select(profiles.c.student_id).where(profiles.c.student_id == student_id)
    ).first():
        raise HTTPException(404, "Không tìm thấy học sinh")
    return resolve_membership(conn, student_id)


@router.get("/admin/students/{student_id}/summary", response_model=dict)
def student_summary(student_id: UUID, user=Depends(admin_user), conn=Depends(connection)):
    users = db.table("users")
    admin_membership(student_id, user, conn)
    row = (
        conn.execute(
            select(users.c.id, users.c.username, users.c.display_name).where(
                users.c.id == student_id
            )
        )
        .mappings()
        .one()
    )
    return dict(row)


@router.get("/admin/content-access", response_model=list[dict])
def content_catalog(user=Depends(admin_user), conn=Depends(connection)):
    policies, subjects, topics = (
        db.table("content_access_policies"),
        db.table("subjects"),
        db.table("topics"),
    )
    result = []
    for kind, table in (("lesson", db.table("lessons")), ("assessment", db.table("assessments"))):
        joined = (
            table.join(topics, table.c.topic_id == topics.c.id).join(
                subjects, topics.c.subject_id == subjects.c.id
            )
            if kind == "lesson"
            else table.join(subjects, table.c.subject_id == subjects.c.id)
        )
        rows = conn.execute(
            select(
                table.c.id,
                table.c.title,
                table.c.status,
                subjects.c.name_vi.label("subject_name"),
                policies.c.preview,
            )
            .select_from(joined.outerjoin(policies, policies.c[f"{kind}_id"] == table.c.id))
            .order_by(subjects.c.sort_order, table.c.title)
        ).mappings()
        for row in rows:
            direct = conn.execute(
                select(policies.c.minimum_plan_code).where(policies.c[f"{kind}_id"] == row["id"])
            ).scalar()
            result.append(
                {
                    **dict(row),
                    "kind": kind,
                    "configured_plan_code": direct,
                    **content_access(conn, user, kind, row["id"]),
                }
            )
    return result


@router.get("/admin/students/{student_id}/membership/history", response_model=list[dict])
def history(student_id: UUID, user=Depends(admin_user), conn=Depends(connection)):
    admin_membership(student_id, user, conn)
    return membership_history(conn, student_id)


@router.post("/admin/students/{student_id}/membership/grant", response_model=out.MembershipResponse)
def grant(
    student_id: UUID,
    payload: out.MembershipGrantInput,
    key: UUID = Header(alias="Idempotency-Key"),
    user=Depends(admin_user),
    conn=Depends(connection),
):
    return change_membership(conn, user["id"], student_id, "grant", payload, key)


@router.post(
    "/admin/students/{student_id}/membership/extend", response_model=out.MembershipResponse
)
def extend(
    student_id: UUID,
    payload: out.MembershipGrantInput,
    key: UUID = Header(alias="Idempotency-Key"),
    user=Depends(admin_user),
    conn=Depends(connection),
):
    return change_membership(conn, user["id"], student_id, "extend", payload, key)


@router.post(
    "/admin/students/{student_id}/membership/revoke", response_model=out.MembershipResponse
)
def revoke(
    student_id: UUID,
    payload: out.MembershipRevokeInput,
    key: UUID = Header(alias="Idempotency-Key"),
    user=Depends(admin_user),
    conn=Depends(connection),
):
    return change_membership(conn, user["id"], student_id, "revoke", payload, key)


@router.get("/lessons/{lesson_id}/preview", response_model=dict)
def preview(lesson_id: UUID, user=Depends(current_user), conn=Depends(connection)):
    lessons, topics, subjects, policies = (
        db.table(name) for name in ("lessons", "topics", "subjects", "content_access_policies")
    )
    row = (
        conn.execute(
            select(
                lessons.c.id,
                lessons.c.title,
                lessons.c.estimated_minutes,
                topics.c.grade,
                subjects.c.name_vi.label("subject_name"),
                policies.c.preview,
            )
            .select_from(
                lessons.join(topics)
                .join(subjects)
                .join(policies, policies.c.lesson_id == lessons.c.id)
            )
            .where(
                lessons.c.id == lesson_id,
                lessons.c.status == "published",
                topics.c.is_active.is_(True),
            )
        )
        .mappings()
        .first()
    )
    if not row:
        raise HTTPException(404, "Không tìm thấy bài học")
    safe_preview = out.PreviewInput.model_validate(
        {
            "summary": str(row["preview"].get("summary", ""))[:350],
            "goals": [str(goal)[:120] for goal in row["preview"].get("goals", [])[:5]],
        }
    ).model_dump()
    return {
        **dict(row),
        "preview": safe_preview,
        **content_access(conn, user, "lesson", lesson_id, row["grade"]),
    }


@router.put("/admin/content/{kind}/{resource_id}/policy", response_model=dict)
def update_policy(
    kind: Literal["lesson", "assessment"],
    resource_id: UUID,
    payload: out.ContentPolicyInput,
    user=Depends(admin_user),
    conn=Depends(connection),
):
    table = db.table("lessons" if kind == "lesson" else "assessments")
    if not conn.execute(
        select(table.c.id).where(table.c.id == resource_id).with_for_update()
    ).first():
        raise HTTPException(404, "Không tìm thấy nội dung")
    policies = db.table("content_access_policies")
    column = policies.c[f"{kind}_id"]
    old = conn.execute(select(policies).where(column == resource_id)).mappings().first()
    values = dict(
        minimum_plan_code=payload.minimum_plan_code,
        learning_level=payload.learning_level,
        preview=payload.preview.model_dump(),
        updated_by=user["id"],
        updated_at=now(),
    )
    conn.execute(
        insert(policies)
        .values(**{f"{kind}_id": resource_id}, **values)
        .on_conflict_do_update(
            index_elements=[column],
            set_=values,
        )
    )
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            actor_user_id=user["id"],
            action="content.policy_update",
            entity_type=kind,
            entity_id=resource_id,
            old_values={
                "minimum_plan_code": old["minimum_plan_code"],
                "learning_level": old["learning_level"],
            }
            if old
            else {},
            new_values={
                "minimum_plan_code": payload.minimum_plan_code,
                "learning_level": payload.learning_level,
                "reason": payload.reason,
            },
        )
    )
    return {"updated": True}
