import hashlib
import json
from datetime import timedelta

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert

from app.core.security import now
from app.db import db
from app.services.access import resolve_membership


def change_membership(conn, actor_id, student_id, operation, payload, key):
    # Global per-actor/key advisory lock and student lock have a fixed order.
    lock_id = int.from_bytes(
        hashlib.sha256(f"{actor_id}:{key}".encode()).digest()[:8], "big", signed=True
    )
    conn.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_id})
    profiles = db.table("student_profiles")
    if not conn.execute(
        select(profiles.c.student_id).where(profiles.c.student_id == student_id).with_for_update()
    ).first():
        raise HTTPException(404, "Không tìm thấy học sinh")
    operations = db.table("membership_operations")
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "student_id": str(student_id),
                "operation": operation,
                "payload": payload.model_dump(),
            },
            sort_keys=True,
            ensure_ascii=False,
        ).encode()
    ).hexdigest()
    previous = (
        conn.execute(
            select(operations).where(
                operations.c.actor_user_id == actor_id, operations.c.idempotency_key == key
            )
        )
        .mappings()
        .first()
    )
    if previous:
        if previous["request_fingerprint"] != fingerprint:
            raise HTTPException(409, "Mã thao tác đã được dùng cho yêu cầu khác")
        return previous["response_snapshot"]
    table = db.table("student_memberships")
    old = conn.execute(select(table).where(table.c.student_id == student_id)).mappings().first()
    at = now()
    if operation == "revoke":
        if not old or old["status"] != "active":
            raise HTTPException(409, "Học sinh chưa có gói VIP để thu hồi")
        conn.execute(
            table.update()
            .where(table.c.student_id == student_id)
            .values(
                status="revoked",
                revoked_at=at,
                revoked_by=actor_id,
                revoke_reason=payload.reason,
                updated_at=at,
            )
        )
        grants = db.table("attempt_access_grants")
        conn.execute(
            grants.update()
            .where(grants.c.membership_student_id == student_id, grants.c.revoked_at.is_(None))
            .values(revoked_at=at)
        )
    else:
        active = bool(old and old["status"] == "active" and old["starts_at"] <= at < old["ends_at"])
        if operation == "grant" and active:
            raise HTTPException(409, "Học sinh đã có VIP. Hãy dùng chức năng gia hạn")
        if operation == "extend" and not old:
            raise HTTPException(409, "Học sinh chưa có gói. Hãy cấp VIP trước")
        starts = old["starts_at"] if active else at
        ends = (old["ends_at"] if active else at) + timedelta(days=payload.duration_days)
        values = dict(
            student_id=student_id,
            plan_code="vip",
            starts_at=starts,
            ends_at=ends,
            status="active",
            source="admin",
            granted_by=actor_id,
            revoked_by=None,
            revoked_at=None,
            revoke_reason=None,
            updated_at=at,
        )
        conn.execute(
            insert(table)
            .values(**values)
            .on_conflict_do_update(
                index_elements=[table.c.student_id],
                set_={k: v for k, v in values.items() if k != "student_id"},
            )
        )
    result = jsonable_encoder(resolve_membership(conn, student_id))
    conn.execute(
        operations.insert().values(
            student_id=student_id,
            actor_user_id=actor_id,
            idempotency_key=key,
            operation=operation,
            request_fingerprint=fingerprint,
            response_snapshot=result,
        )
    )
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            actor_user_id=actor_id,
            action=f"membership.{operation}",
            entity_type="student_membership",
            entity_id=student_id,
            old_values=jsonable_encoder(dict(old)) if old else {},
            new_values={**result, "reason": payload.reason},
        )
    )
    return result


def membership_history(conn, student_id):
    table, users = db.table("membership_operations"), db.table("users")
    return [
        dict(row)
        for row in conn.execute(
            select(
                table.c.id,
                table.c.operation,
                table.c.created_at,
                table.c.response_snapshot,
                users.c.display_name.label("actor_name"),
            )
            .select_from(table.join(users, table.c.actor_user_id == users.c.id))
            .where(table.c.student_id == student_id)
            .order_by(table.c.created_at.desc())
            .limit(50)
        ).mappings()
    ]
