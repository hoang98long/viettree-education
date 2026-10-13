from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import delete, func, null, select, text, update
from sqlalchemy.exc import IntegrityError

from app.core.security import hasher, now, throttle_sensitive, verify_password
from app.db import db
from app.services.accessibility import reading_preferences

SAFE_FIELDS = (
    "id",
    "username",
    "display_name",
    "email",
    "is_active",
    "auth_provider",
    "created_at",
    "updated_at",
    "last_login_at",
    "account_revision",
    "must_change_password",
    "password_changed_at",
)


def role_names(conn, user_id):
    roles = db.table("user_roles")
    return list(
        conn.execute(
            select(roles.c.role).where(roles.c.user_id == user_id).order_by(roles.c.role)
        ).scalars()
    )


def safe_account(conn, row):
    profiles = db.table("student_profiles")
    profile = (
        conn.execute(select(profiles).where(profiles.c.student_id == row["id"])).mappings().first()
    )
    result = {key: row[key] for key in SAFE_FIELDS}
    result.update(
        roles=role_names(conn, row["id"]),
        current_grade=profile["current_grade"] if profile else None,
        text_size=reading_preferences(profile["accessibility_options"] if profile else {})[
            "text_size"
        ],
    )
    return result


def audit(conn, actor_id, target_id, action, before, after, reason):
    conn.execute(
        db.table("audit_logs")
        .insert()
        .values(
            actor_user_id=actor_id,
            entity_type="account",
            entity_id=target_id,
            action=action,
            old_values=before if before is not None else null(),
            new_values={**after, "reason": reason},
        )
    )


def snapshot(conn, row):
    # Audit explicit fields only: never password/hash, session/CSRF secrets or contact email.
    result = safe_account(conn, row)
    return {
        key: result[key]
        for key in (
            "username",
            "display_name",
            "roles",
            "is_active",
            "current_grade",
            "text_size",
            "account_revision",
            "must_change_password",
        )
    }


def authenticate_actor(conn, actor, password):
    if throttle_sensitive(actor["id"]):
        raise HTTPException(
            429, "Hãy đợi một phút rồi xác nhận mật khẩu lại", headers={"Retry-After": "60"}
        )
    users, sessions = db.table("users"), db.table("auth_sessions")
    row = (
        conn.execute(select(users).where(users.c.id == actor["id"]).with_for_update(key_share=True))
        .mappings()
        .one()
    )
    session = conn.execute(
        select(sessions.c.token_hash).where(
            sessions.c.token_hash == actor["session_hash"],
            sessions.c.revoked_at.is_(None),
            sessions.c.expires_at > now(),
        )
    ).scalar()
    if not row["is_active"] or not session:
        raise HTTPException(401, "Phiên không còn hợp lệ. Hãy đăng nhập lại")
    if not verify_password(row["password_hash"], password):
        raise HTTPException(403, "Mật khẩu xác nhận chưa đúng")
    return row


def admin_lock(conn, actor, password, target_id=None):
    # All admin account writes serialize role/status invariants across workers.
    conn.execute(text("SELECT pg_advisory_xact_lock(78249101)"))
    users = db.table("users")
    ids = {actor["id"]}
    if target_id:
        ids.add(target_id)
    rows = {
        r["id"]: r
        for r in conn.execute(
            select(users)
            .where(users.c.id.in_(ids))
            .order_by(users.c.id)
            .with_for_update(key_share=True)
        ).mappings()
    }
    # PostgreSQL FOR NO KEY UPDATE keeps account writes exclusive but lets other
    # transactions reference the immutable user UUID (audit/session foreign keys).
    authenticate_actor(conn, actor, password)
    if "admin" not in role_names(conn, actor["id"]) or rows[actor["id"]]["must_change_password"]:
        raise HTTPException(403, "Tài khoản chưa được phép quản trị")
    if target_id and target_id not in rows:
        raise HTTPException(404, "Không tìm thấy tài khoản")
    return rows.get(target_id)


def check_revision(row, revision):
    if row["account_revision"] != revision:
        raise HTTPException(409, "Tài khoản đã thay đổi. Tải lại thông tin trước khi lưu")


def revoke_sessions(conn, user_id, except_hash=None):
    sessions = db.table("auth_sessions")
    predicates = [sessions.c.user_id == user_id, sessions.c.revoked_at.is_(None)]
    if except_hash:
        predicates.append(sessions.c.token_hash != except_hash)
    return conn.execute(update(sessions).where(*predicates).values(revoked_at=now())).rowcount


def bump(conn, user_id, **values):
    users = db.table("users")
    return (
        conn.execute(
            update(users)
            .where(users.c.id == user_id)
            .values(
                **values,
                updated_at=now(),
                account_revision=users.c.account_revision + 1,
            )
            .returning(users)
        )
        .mappings()
        .one()
    )


def unique_write(conn, operation):
    try:
        with conn.begin_nested():
            return operation()
    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            raise HTTPException(409, "Tên đăng nhập hoặc email đã được sử dụng") from None
        raise


def write_profile(conn, user_id, payload):
    if "student" not in payload.roles:
        return  # Retain historical profile, memberships, results and relationships.
    profiles = db.table("student_profiles")
    row = (
        conn.execute(select(profiles).where(profiles.c.student_id == user_id).with_for_update())
        .mappings()
        .first()
    )
    options = {**(row["accessibility_options"] if row else {}), "text_size": payload.text_size}
    if row:
        conn.execute(
            update(profiles)
            .where(profiles.c.student_id == user_id)
            .values(
                current_grade=payload.current_grade,
                accessibility_options=options,
                updated_at=now(),
            )
        )
    else:
        conn.execute(
            profiles.insert().values(
                student_id=user_id,
                current_grade=payload.current_grade,
                accessibility_options=options,
            )
        )


def create(conn, actor, payload):
    admin_lock(conn, actor, payload.actor_password)
    users, roles = db.table("users"), db.table("user_roles")
    if payload.password.casefold() == payload.username.casefold():
        raise HTTPException(422, "Mật khẩu phải khác tên đăng nhập")
    row = unique_write(
        conn,
        lambda: (
            conn.execute(
                users.insert()
                .values(
                    id=uuid4(),
                    username=payload.username,
                    display_name=payload.display_name,
                    email=payload.email,
                    password_hash=hasher.hash(payload.password),
                    must_change_password=payload.must_change_password,
                    password_changed_at=now(),
                )
                .returning(users)
            )
            .mappings()
            .one()
        ),
    )
    conn.execute(roles.insert(), [{"user_id": row["id"], "role": role} for role in payload.roles])
    write_profile(conn, row["id"], payload)
    audit(
        conn, actor["id"], row["id"], "account_created", None, snapshot(conn, row), payload.reason
    )
    return safe_account(conn, row)


def edit(conn, actor, target_id, payload):
    row = admin_lock(conn, actor, payload.actor_password, target_id)
    check_revision(row, payload.revision)
    before, previous_roles = snapshot(conn, row), role_names(conn, target_id)
    if target_id == actor["id"] and (not payload.is_active or payload.roles != previous_roles):
        raise HTTPException(409, "Không tự khóa hoặc thay vai trò của chính mình")
    if (
        row["is_active"]
        and "admin" in previous_roles
        and (not payload.is_active or "admin" not in payload.roles)
    ):
        users, roles = db.table("users"), db.table("user_roles")
        remaining = conn.execute(
            select(func.count())
            .select_from(users.join(roles))
            .where(
                users.c.is_active.is_(True),
                roles.c.role == "admin",
                users.c.id != target_id,
            )
        ).scalar_one()
        if not remaining:
            raise HTTPException(409, "Cần giữ ít nhất một quản trị viên hoạt động")
    changed = unique_write(
        conn,
        lambda: bump(
            conn,
            target_id,
            username=payload.username,
            display_name=payload.display_name,
            email=payload.email,
            is_active=payload.is_active,
        ),
    )
    roles = db.table("user_roles")
    removed, added = (
        set(previous_roles) - set(payload.roles),
        set(payload.roles) - set(previous_roles),
    )
    if removed:
        conn.execute(delete(roles).where(roles.c.user_id == target_id, roles.c.role.in_(removed)))
    if added:
        conn.execute(roles.insert(), [{"user_id": target_id, "role": role} for role in added])
    write_profile(conn, target_id, payload)
    security_change = bool(
        removed
        or added
        or row["is_active"] != payload.is_active
        or row["username"] != payload.username
    )
    if security_change:
        revoke_sessions(conn, target_id)
    after = snapshot(conn, changed)
    after["email_changed"] = row["email"] != payload.email
    after["sessions_revoked"] = security_change
    audit(conn, actor["id"], target_id, "account_updated", before, after, payload.reason)
    return safe_account(conn, changed)


def reset_password(conn, actor, target_id, payload):
    row = admin_lock(conn, actor, payload.actor_password, target_id)
    check_revision(row, payload.revision)
    if target_id == actor["id"]:
        raise HTTPException(409, "Dùng trang Bảo mật tài khoản để đổi mật khẩu của mình")
    if row["auth_provider"] != "local":
        raise HTTPException(409, "Tài khoản dùng nhà cung cấp đăng nhập ngoài")
    if payload.new_password.casefold() == row["username"].casefold() or verify_password(
        row["password_hash"], payload.new_password
    ):
        raise HTTPException(422, "Mật khẩu mới phải khác tên đăng nhập và mật khẩu cũ")
    before = snapshot(conn, row)
    changed = bump(
        conn,
        target_id,
        password_hash=hasher.hash(payload.new_password),
        password_changed_at=now(),
        must_change_password=True,
    )
    revoked = revoke_sessions(conn, target_id)
    audit(
        conn,
        actor["id"],
        target_id,
        "account_password_reset",
        before,
        {**snapshot(conn, changed), "revoked_sessions": revoked},
        payload.reason,
    )
    return safe_account(conn, changed)


def revoke_all(conn, actor, target_id, payload):
    row = admin_lock(conn, actor, payload.actor_password, target_id)
    check_revision(row, payload.revision)
    before = snapshot(conn, row)
    count = revoke_sessions(conn, target_id)
    changed = bump(conn, target_id)
    audit(
        conn,
        actor["id"],
        target_id,
        "account_sessions_revoked",
        before,
        {**snapshot(conn, changed), "revoked_sessions": count},
        payload.reason,
    )
    return {"revoked_sessions": count, "account_revision": changed["account_revision"]}
