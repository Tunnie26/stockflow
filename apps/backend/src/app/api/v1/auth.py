from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.response import SuccessResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=SuccessResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = AuthService(db)

    token = service.login(
        username=data.username,
        password=data.password,
    )

    return SuccessResponse(
        data=LoginResponse(
            access_token=token,
            token_type="bearer",
        )
    )


@router.get("/me", response_model=SuccessResponse)
def get_me(
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return SuccessResponse(data=UserResponse.model_validate(current_user))
