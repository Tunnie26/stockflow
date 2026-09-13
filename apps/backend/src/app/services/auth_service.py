from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.exceptions import AppError
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate(self, username: str, password: str) -> User:
        user = self.db.scalar(select(User).where(User.username == username))

        if user is None:
            raise AppError(
                "Invalid username or password",
                code="INVALID_CREDENTIALS",
                status_code=401,
            )

        if not user.is_active:
            raise AppError(
                "User account is inactive",
                code="USER_INACTIVE",
                status_code=401,
            )

        if not verify_password(password, user.password_hash):
            raise AppError(
                "Invalid username or password",
                code="INVALID_CREDENTIALS",
                status_code=401,
            )

        return user

    def login(self, username: str, password: str) -> str:
        user = self.authenticate(username, password)

        return create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
        )
