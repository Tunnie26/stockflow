from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.receiving_unit import ReceivingUnit
from app.schemas.receiving_unit import (
    ReceivingUnitCreate,
    ReceivingUnitUpdate,
)


class ReceivingUnitService:
    def __init__(self, db: Session):
        self.db = db

    def create_receiving_unit(
        self,
        data: ReceivingUnitCreate,
    ) -> ReceivingUnit:
        existing_unit = self.db.scalar(
            select(ReceivingUnit).where(ReceivingUnit.code == data.code)
        )

        if existing_unit is not None:
            raise AppError(
                "Receiving unit code already exists",
                code="RECEIVING_UNIT_CODE_ALREADY_EXISTS",
            )

        unit = ReceivingUnit(
            code=data.code,
            name=data.name,
        )

        self.db.add(unit)
        self.db.flush()

        return unit

    def list_receiving_units(self) -> list[ReceivingUnit]:
        statement = select(ReceivingUnit).order_by(ReceivingUnit.id)
        return list(self.db.scalars(statement).all())

    def get_receiving_unit(
        self,
        receiving_unit_id: int,
    ) -> ReceivingUnit:
        unit = self.db.scalar(
            select(ReceivingUnit).where(ReceivingUnit.id == receiving_unit_id)
        )

        if unit is None:
            raise AppError(
                "Receiving unit not found",
                code="RECEIVING_UNIT_NOT_FOUND",
                status_code=404,
            )

        return unit

    def update_receiving_unit(
        self,
        receiving_unit_id: int,
        data: ReceivingUnitUpdate,
    ) -> ReceivingUnit:
        unit = self.get_receiving_unit(receiving_unit_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(unit, field, value)

        self.db.flush()

        return unit
