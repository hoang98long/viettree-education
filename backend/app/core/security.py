import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from app.core.config import settings
from app.db import connection, db, engine

hasher = PasswordHasher()
DUMMY_HASH = hasher.hash(secrets.token_urlsafe(32))


def now():
    return datetime.now(timezone.utc)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def verify_password(encoded: str | None, password: str) -> bool:
    try:
        return hasher.verify(encoded or DUMMY_HASH, password) and encoded is not None
    except (VerificationError, InvalidHashError):
        return False


def verify_origin(request: Request):
    origin = request.headers.get("origin")
    if origin and origin.rstrip("/") not in settings().origins:
        raise HTTPException(403, "Nguồn yêu cầu không được phép")
    if request.headers.get("sec-fetch-site") == "cross-site":
        raise HTTPException(403, "Yêu cầu khác trang không được phép")


def current_user(request: Request, conn: Connection = Depends(connection)):
    raw = request.cookies.get("viettree_session", "")
    sessions, users, roles = (db.table(name) for name in ("auth_sessions", "users", "user_roles"))
    session = (
        conn.execute(
            select(sessions).where(
                sessions.c.token_hash == digest(raw),
                sessions.c.revoked_at.is_(None),
                sessions.c.expires_at > now(),
            )
        )
        .mappings()
        .first()
    )
    if not session:
        raise HTTPException(401, "Em hãy đăng nhập để tiếp tục nhé")
    user = (
        conn.execute(
            select(users.c.id, users.c.username, users.c.display_name, users.c.is_active).where(
                users.c.id == session["user_id"]
            )
        )
        .mappings()
        .first()
    )
    if not user or not user["is_active"]:
        raise HTTPException(401, "Tài khoản không khả dụng")
    role_names = list(
        conn.execute(select(roles.c.role).where(roles.c.user_id == user["id"])).scalars()
    )
    expires_at = session["expires_at"]
    if {"admin", "teacher"}.intersection(role_names):
        # Vai trò có thể được cấp sau khi học sinh đã tạo phiên ghi nhớ.
        expires_at = min(
            expires_at, session["created_at"] + timedelta(hours=settings().session_hours)
        )
        if expires_at <= now():
            raise HTTPException(401, "Phiên đã hết hạn. Hãy đăng nhập lại")
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        verify_origin(request)
        csrf = request.headers.get("x-csrf-token", "")
        if not csrf or not hmac.compare_digest(digest(csrf), session["csrf_hash"]):
            raise HTTPException(403, "Phiên bảo mật không hợp lệ. Hãy tải lại trang")
    return {
        **dict(user),
        "roles": role_names,
        "session_hash": session["token_hash"],
        "session_expires_at": expires_at,
    }


def require_role(role: str):
    def dependency(user=Depends(current_user)):
        if role not in user["roles"]:
            raise HTTPException(403, "Tài khoản không có quyền truy cập")
        return user

    return dependency


student_user = require_role("student")
admin_user = require_role("admin")


def public_user(user):
    return {
        **{key: user[key] for key in ("id", "username", "display_name", "roles")},
        "session_expires_at": user.get("session_expires_at"),
    }


def throttle_login(request: Request) -> bool:
    table = db.table("auth_login_limits")
    # Không lưu IP plaintext; không tin X-Forwarded-For từ client.
    key = digest("login:" + (request.client.host if request.client else "unknown"))
    start = now()
    statement = insert(table).values(key_hash=key, window_start=start, failures=1)
    from sqlalchemy import case

    expired = table.c.window_start < start - timedelta(minutes=1)
    statement = statement.on_conflict_do_update(
        index_elements=[table.c.key_hash],
        set_={
            "window_start": case((expired, start), else_=table.c.window_start),
            "failures": case((expired, 1), else_=table.c.failures + 1),
        },
    ).returning(table.c.failures)
    # Transaction riêng để login sai vẫn tăng giới hạn, không commit transaction API.
    with engine().begin() as conn:
        return conn.execute(statement).scalar_one() > 10


def create_session(conn, user_id, response, roles=(), remember_me=False):
    # Phiên dài chỉ dành cho học sinh không có vai trò quản trị/giáo viên.
    remembered = remember_me and "student" in roles and not {"admin", "teacher"}.intersection(roles)
    duration = (
        timedelta(days=settings().remember_session_days)
        if remembered
        else timedelta(hours=settings().session_hours)
    )
    expires_at = now() + duration
    token, csrf = secrets.token_urlsafe(48), secrets.token_urlsafe(32)
    conn.execute(
        insert(db.table("auth_sessions")).values(
            token_hash=digest(token),
            csrf_hash=digest(csrf),
            user_id=user_id,
            expires_at=expires_at,
        )
    )
    cookie = dict(
        secure=settings().cookie_secure,
        samesite="lax",
        path="/",
        max_age=int(duration.total_seconds()),
        expires=expires_at,
    )
    response.set_cookie("viettree_session", token, httponly=True, **cookie)
    response.set_cookie("viettree_csrf", csrf, httponly=False, **cookie)
    return expires_at


def revoke_session(conn, token_hash):
    table = db.table("auth_sessions")
    conn.execute(update(table).where(table.c.token_hash == token_hash).values(revoked_at=now()))
