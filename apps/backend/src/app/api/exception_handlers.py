from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"error": {"code": exc.code, "message": exc.message}}
    )
