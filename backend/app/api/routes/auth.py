from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import func, select

from app.core.dependencies import database
from app.core.security import (
    create_session,
    current_user,
    digest,
    now,
    public_user,
    revoke_session,
    throttle_login,
    verify_origin,
    verify_password,
)
from app.db import db
from app.schemas.auth import LoginInput, UserResponse
from app.services.accessibility import reading_preferences

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
        result.update(reading_preferences(options))
    return result


@router.post("/auth/login", response_model=UserResponse, tags=["auth"])
def login(payload: LoginInput, request: Request, response: Response, conn=database):
    verify_origin(request)
    if throttle_login(request, payload.username):
        raise HTTPException(
            429, "Em hãy đợi một phút rồi thử lại nhé", headers={"Retry-After": "60"}
        )
    users, roles = db.table("users"), db.table("user_roles")
    user = (
        conn.execute(
            select(users)
            .where(func.lower(users.c.username) == payload.username.strip().lower())
            .with_for_update(key_share=True)
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
def me(user=Depends(current_user), conn=database):
    return _user_response(user, conn)


@router.post("/auth/logout", response_model=dict[str, bool], tags=["auth"])
def logout(response: Response, user=Depends(current_user), conn=database):
    revoke_session(conn, user["session_hash"])
    response.delete_cookie("viettree_session", path="/")
    response.delete_cookie("viettree_csrf", path="/")
    return {"logged_out": True}
