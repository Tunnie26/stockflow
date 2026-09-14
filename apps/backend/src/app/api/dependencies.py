from collections.abc import Callable, Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import decode_access_token
from app.db.session import SessionLocal
from app.exceptions import AppError
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> User:
    payload = decode_access_token(credentials.credentials)

    user_id = payload.get("sub")

    if user_id is None:
        raise AppError(
            "Invalid or expired access token",
            code="INVALID_TOKEN",
            status_code=401,
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError) as exc:
        raise AppError(
            "Invalid or expired access token",
            code="INVALID_TOKEN",
            status_code=401,
        ) from exc

    user = db.scalar(select(User).where(User.id == user_id))

    if user is None or not user.is_active:
        raise AppError(
            "Invalid or expired access token",
            code="INVALID_TOKEN",
            status_code=401,
        )

    return user


def require_role(*allowed_roles: str) -> Callable:
    def role_checker(
        current_user: User = Depends(get_current_user),  # noqa: B008
    ) -> User:
        if current_user.role not in allowed_roles:
            raise AppError(
                "You do not have permission to perform this action",
                code="FORBIDDEN",
                status_code=403,
            )

        return current_user

    return role_checker


def require_authenticated() -> Callable:
    return require_role("ADMIN", "USER", "VIEWER")


def require_admin() -> Callable:
    return require_role("ADMIN")


def require_user() -> Callable:
    return require_role("ADMIN", "USER")
