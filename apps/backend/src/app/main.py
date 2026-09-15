from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import (
    app_error_handler,
    unexpected_error_handler,
)
from app.api.v1.router import router as v1_router
from app.config import settings
from app.exceptions import AppError

app = FastAPI(
    title="StockFlow API",
    version="0.1.0",
    description="Inventory Management Platform API",
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(v1_router, prefix="/api/v1")
