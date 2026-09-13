from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.config import settings
from app.exceptions import AppError


def create_access_token(
    *,
    user_id: int,
    username: str,
    role: str,
) -> str:
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.jwt_access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.InvalidTokenError as exc:
        raise AppError(
            "Invalid or expired access token",
            code="INVALID_TOKEN",
            status_code=401,
        ) from exc
