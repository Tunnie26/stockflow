from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.v1.customers import router as customers_router
from app.api.v1.locations import router as locations_router
from app.api.v1.material_categories import router as material_categories_router
from app.api.v1.materials import router as materials_router
from app.api.v1.receiving_units import router as receiving_units_router
from app.api.v1.suppliers import router as suppliers_router
from app.api.v1.warehouses import router as warehouses_router

router = APIRouter()


@router.get("/db-check")
def database_check(db: Session = Depends(get_db)):  # noqa: B008
    result = db.execute(text("SELECT 1"))
    return {"database": result.scalar_one()}


router.include_router(materials_router, prefix="/materials", tags=["Materials"])

router.include_router(warehouses_router, prefix="/warehouses", tags=["Warehouses"])

router.include_router(locations_router, prefix="/locations", tags=["Locations"])

router.include_router(
    material_categories_router,
    prefix="/material-categories",
    tags=["Material Categories"],
)

router.include_router(suppliers_router, prefix="/suppliers", tags=["Suppliers"])

router.include_router(customers_router, prefix="/customers", tags=["Customers"])

router.include_router(
    receiving_units_router, prefix="/receiving-units", tags=["Receiving Units"]
)
