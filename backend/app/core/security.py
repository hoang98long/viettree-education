from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe
from uuid import UUID, uuid4
import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from app.core.config import get_settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, password_hash_value: str) -> bool:
    return password_hash.verify(password, password_hash_value)


def create_access_token(user_id: UUID, role: str) -> str:
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode(
        {"sub": str(user_id), "role": role, "type": "access", "jti": str(uuid4()), "exp": expires_at},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token() -> str:
    """Create an opaque, high-entropy token. Only its hash is persisted."""
    return token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    settings = get_settings()
    return sha256(f"{settings.jwt_secret_key}:{token}".encode()).hexdigest()


def decode_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ hoặc đã hết hạn") from error
