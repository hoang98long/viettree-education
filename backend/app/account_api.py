from datetime import timedelta
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select

from app.account_schemas import (
    AccountCreate,
    AccountReset,
    AccountRevoke,
    AccountUpdate,
    ChangePassword,
    RevokeOthers,
    Role,
)
from app.core.config import settings
from app.core.security import admin_user, create_session, current_user, hasher, now, verify_password
from app.db import connection, db
from app.services import accounts

router = APIRouter(prefix="/api/v1", tags=["accounts"])


@router.get("/admin/accounts")
def list_accounts(
    search: str = Query("", max_length=160),
    role: Role | None = None,
    status: Literal["active", "inactive"] | None = None,
    grade: int | None = Query(None, ge=1, le=5),
    page: int = Query(1, ge=1, le=10000),
    user=Depends(admin_user),
    conn=Depends(connection),
):
    users, roles, profiles = (db.table(n) for n in ("users", "user_roles", "student_profiles"))
    query = select(users)
    if search.strip():
        term = (
            "%" + search.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        )
        query = query.where(
            users.c.username.ilike(term)
            | users.c.display_name.ilike(term)
            | users.c.email.ilike(term)
        )
    if role:
        query = query.where(
            select(roles.c.user_id)
            .where(roles.c.user_id == users.c.id, roles.c.role == role)
            .exists()
        )
    if status:
        query = query.where(users.c.is_active.is_(status == "active"))
    if grade:
        query = query.where(
            select(profiles.c.student_id)
            .where(
                profiles.c.student_id == users.c.id,
                profiles.c.current_grade == grade,
            )
            .exists(),
            select(roles.c.user_id)
            .where(roles.c.user_id == users.c.id, roles.c.role == "student")
            .exists(),
        )
    total = conn.execute(select(func.count()).select_from(query.subquery())).scalar_one()
    rows = conn.execute(
        query.order_by(users.c.username, users.c.id).offset((page - 1) * 20).limit(20)
    ).mappings()
    return {
        "items": [accounts.safe_account(conn, row) for row in rows],
        "total": total,
        "page": page,
    }


def account_row(conn, user_id):
    users = db.table("users")
    row = conn.execute(select(users).where(users.c.id == user_id)).mappings().first()
    if not row:
        raise HTTPException(404, "Không tìm thấy tài khoản")
    return row


def sessions_summary(conn, user_id, current_hash=None):
    sessions = db.table("auth_sessions")
    privileged = bool({"admin", "teacher"}.intersection(accounts.role_names(conn, user_id)))
    cutoff = timedelta(hours=settings().session_hours)
    rows = list(
        conn.execute(
            select(sessions.c.created_at, sessions.c.expires_at, sessions.c.token_hash)
            .where(
                sessions.c.user_id == user_id,
                sessions.c.revoked_at.is_(None),
                sessions.c.expires_at > now(),
                *([sessions.c.created_at > now() - cutoff] if privileged else []),
            )
            .order_by(sessions.c.created_at.desc())
        ).mappings()
    )
    # No session IDs, tokens, CSRF, IPs or user-agent tracking in the payload.
    return {
        "active_sessions": len(rows),
        "sessions": [
            {
                "created_at": r["created_at"],
                "expires_at": min(r["expires_at"], r["created_at"] + cutoff)
                if privileged
                else r["expires_at"],
                "is_current": r["token_hash"] == current_hash,
            }
            for r in rows[:20]
        ],
    }


@router.get("/admin/accounts/{user_id}")
def detail(user_id: UUID, user=Depends(admin_user), conn=Depends(connection)):
    result = accounts.safe_account(conn, account_row(conn, user_id))
    logs, users = db.table("audit_logs"), db.table("users")
    history = (
        conn.execute(
            select(
                logs.c.action,
                logs.c.old_values,
                logs.c.new_values,
                logs.c.created_at,
                users.c.username.label("actor_username"),
            )
            .select_from(logs.outerjoin(users, logs.c.actor_user_id == users.c.id))
            .where(
                logs.c.entity_type == "account",
                logs.c.entity_id == user_id,
            )
            .order_by(logs.c.created_at.desc(), logs.c.id.desc())
            .limit(20)
        )
        .mappings()
        .all()
    )
    return {**result, **sessions_summary(conn, user_id, user["session_hash"]), "history": history}


@router.post("/admin/accounts", status_code=201)
def create(payload: AccountCreate, user=Depends(admin_user), conn=Depends(connection)):
    return accounts.create(conn, user, payload)


@router.patch("/admin/accounts/{user_id}")
def edit(user_id: UUID, payload: AccountUpdate, user=Depends(admin_user), conn=Depends(connection)):
    return accounts.edit(conn, user, user_id, payload)


@router.post("/admin/accounts/{user_id}/reset-password")
def reset(user_id: UUID, payload: AccountReset, user=Depends(admin_user), conn=Depends(connection)):
    return accounts.reset_password(conn, user, user_id, payload)


@router.post("/admin/accounts/{user_id}/revoke-sessions")
def revoke(
    user_id: UUID, payload: AccountRevoke, user=Depends(admin_user), conn=Depends(connection)
):
    return accounts.revoke_all(conn, user, user_id, payload)


@router.get("/auth/security")
def security(user=Depends(current_user), conn=Depends(connection)):
    row = account_row(conn, user["id"])
    return {
        "username": row["username"],
        "auth_provider": row["auth_provider"],
        "password_changed_at": row["password_changed_at"],
        "must_change_password": row["must_change_password"],
        **sessions_summary(conn, user["id"], user["session_hash"]),
    }


@router.post("/auth/password")
def change_password(
    payload: ChangePassword,
    response: Response,
    user=Depends(current_user),
    conn=Depends(connection),
):
    row = accounts.authenticate_actor(conn, user, payload.current_password)
    if row["auth_provider"] != "local":
        raise HTTPException(409, "Đổi mật khẩu tại nhà cung cấp đăng nhập của bạn")
    if payload.new_password.casefold() == row["username"].casefold() or verify_password(
        row["password_hash"], payload.new_password
    ):
        raise HTTPException(422, "Mật khẩu mới phải khác tên đăng nhập và mật khẩu cũ")
    accounts.bump(
        conn,
        user["id"],
        password_hash=hasher.hash(payload.new_password),
        password_changed_at=now(),
        must_change_password=False,
    )
    revoked = accounts.revoke_sessions(conn, user["id"])
    roles = accounts.role_names(conn, user["id"])
    expires_at = create_session(conn, user["id"], response, roles)
    accounts.audit(
        conn,
        user["id"],
        user["id"],
        "account_password_changed",
        None,
        {"revoked_sessions": revoked, "must_change_password": False},
        "Người dùng tự đổi mật khẩu",
    )
    return {"changed": True, "session_expires_at": expires_at}


@router.post("/auth/sessions/revoke-others")
def revoke_others(payload: RevokeOthers, user=Depends(current_user), conn=Depends(connection)):
    accounts.authenticate_actor(conn, user, payload.current_password)
    count = accounts.revoke_sessions(conn, user["id"], user["session_hash"])
    accounts.audit(
        conn,
        user["id"],
        user["id"],
        "account_other_sessions_revoked",
        None,
        {"revoked_sessions": count},
        "Người dùng đăng xuất các phiên khác",
    )
    return {"revoked_sessions": count}
