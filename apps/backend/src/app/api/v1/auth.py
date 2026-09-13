from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.response import SuccessResponse
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
