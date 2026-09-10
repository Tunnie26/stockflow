from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter()


@router.get("/db-check")
def database_check(db: Session = Depends(get_db)):  # noqa: B008
    result = db.execute(text("SELECT 1"))
    return {"database": result.scalar_one()}
