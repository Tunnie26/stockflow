from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.material_category import MaterialCategory
from app.models.receiving_unit import ReceivingUnit
from app.models.warehouse import Warehouse

WAREHOUSES = [
    {"code": "WH-VFDL", "name": "Kho VietFarm Đà Lạt"},
    {"code": "WH-HSTC", "name": "Kho HSTC"},
]

CATEGORIES = [
    {"code": "BOX", "name": "Thùng"},
    {"code": "BAG", "name": "Túi"},
    {"code": "LABEL", "name": "Tem nhãn"},
    {"code": "PAPER", "name": "Giấy"},
    {"code": "OTHER", "name": "Khác"},
]

RECEIVING_UNITS = [
    {"code": "VH", "name": "Vận hành"},
    {"code": "HSTC", "name": "HSTC"},
    {"code": "VFBN", "name": "Bắc Ninh"},
    {"code": "OTHER", "name": "Khác"},
]


def seed_warehouses(db) -> None:
    for item in WAREHOUSES:
        existing = db.scalar(select(Warehouse).where(Warehouse.code == item["code"]))

        if existing is None:
            db.add(Warehouse(**item))


def seed_categories(db) -> None:
    for item in CATEGORIES:
        existing = db.scalar(
            select(MaterialCategory).where(MaterialCategory.code == item["code"])
        )

        if existing is None:
            db.add(MaterialCategory(**item))


def seed_receiving_units(db) -> None:
    for item in RECEIVING_UNITS:
        existing = db.scalar(
            select(ReceivingUnit).where(ReceivingUnit.code == item["code"])
        )

        if existing is None:
            db.add(ReceivingUnit(**item))


def main() -> None:
    with SessionLocal() as db:
        try:
            seed_warehouses(db)
            seed_categories(db)
            seed_receiving_units(db)

            db.commit()
            print("Seed completed successfully.")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
