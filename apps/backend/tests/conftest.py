import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.jwt import create_access_token
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User


def _auth_headers(username: str) -> dict[str, str]:
    db = SessionLocal()

    try:
        user = db.scalar(select(User).where(User.username == username))

        assert user is not None, f"Test user '{username}' does not exist"
        assert user.is_active, f"Test user '{username}' is inactive"

        token = create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
        )

        return {
            "Authorization": f"Bearer {token}",
        }
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_headers():
    return _auth_headers("admin")


@pytest.fixture
def user_headers():
    return _auth_headers("user")


@pytest.fixture
def viewer_headers():
    return _auth_headers("viewer")
