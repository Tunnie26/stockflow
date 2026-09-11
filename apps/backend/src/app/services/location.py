from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.location import Location
from app.models.warehouse import Warehouse
from app.schemas.location import LocationCreate, LocationUpdate


class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def create_location(self, data: LocationCreate) -> Location:
        warehouse = self.db.scalar(
            select(Warehouse).where(Warehouse.id == data.warehouse_id)
        )

        if warehouse is None:
            raise AppError(
                "Warehouse not found",
                code="WAREHOUSE_NOT_FOUND",
            )

        if not warehouse.is_active:
            raise AppError(
                "Warehouse is inactive",
                code="WAREHOUSE_INACTIVE",
            )

        existing_location = self.db.scalar(
            select(Location).where(
                Location.warehouse_id == data.warehouse_id,
                Location.code == data.code,
            )
        )

        if existing_location is not None:
            raise AppError(
                "Location code already exists in warehouse",
                code="LOCATION_CODE_ALREADY_EXISTS",
            )

        location = Location(
            warehouse_id=data.warehouse_id,
            code=data.code,
            name=data.name,
            description=data.description,
        )

        self.db.add(location)
        self.db.flush()

        return location

    def list_locations(self) -> list[Location]:
        statement = select(Location).order_by(Location.id)

        return list(self.db.scalars(statement).all())

    def get_location(self, location_id: int) -> Location:
        location = self.db.scalar(select(Location).where(Location.id == location_id))

        if location is None:
            raise AppError(
                "Location not found",
                code="LOCATION_NOT_FOUND",
            )

        return location

    def update_location(
        self,
        location_id: int,
        data: LocationUpdate,
    ) -> Location:
        location = self.get_location(location_id)

        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data:
            existing_location = self.db.scalar(
                select(Location).where(
                    Location.warehouse_id == location.warehouse_id,
                    Location.code == update_data["code"],
                    Location.id != location.id,
                )
            )

            if existing_location is not None:
                raise AppError(
                    "Location code already exists in warehouse",
                    code="LOCATION_CODE_ALREADY_EXISTS",
                )

        for field, value in update_data.items():
            setattr(location, field, value)

        self.db.flush()

        return location
