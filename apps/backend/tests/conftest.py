import pytest
from fastapi.testclient import TestClient

from app.core.jwt import create_access_token
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_headers():
    token = create_access_token(
        user_id=1,
        username="admin",
        role="ADMIN",
    )

    return {
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture
def user_headers():
    token = create_access_token(
        user_id=4,
        username="user",
        role="USER",
    )

    return {
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture
def viewer_headers():
    token = create_access_token(
        user_id=5,
        username="viewer",
        role="VIEWER",
    )

    return {
        "Authorization": f"Bearer {token}",
    }
