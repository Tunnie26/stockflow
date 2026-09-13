from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.inventory_check import InventoryCheck
from app.models.inventory_check_detail import InventoryCheckDetail
from app.models.material import Material
from app.schemas.inventory_check import (
    InventoryCheckDetailResponse,
    InventoryCheckResponse,
)


class InventoryCheckQueryService:
    def __init__(self, db: Session):
        self.db = db

    def list_inventory_checks(self) -> list[InventoryCheckResponse]:
        checks = list(
            self.db.scalars(
                select(InventoryCheck).order_by(
                    InventoryCheck.created_at.desc(),
                    InventoryCheck.id.desc(),
                )
            ).all()
        )

        if not checks:
            return []

        check_ids = [check.id for check in checks]

        rows = self.db.execute(
            select(
                InventoryCheckDetail,
                Material.sku,
                Material.name,
                Material.unit,
            )
            .join(
                Material,
                Material.id == InventoryCheckDetail.material_id,
            )
            .where(InventoryCheckDetail.inventory_check_id.in_(check_ids))
            .order_by(InventoryCheckDetail.id)
        ).all()

        details_by_check: dict[int, list[InventoryCheckDetailResponse]] = defaultdict(
            list
        )

        for detail, sku, name, unit in rows:
            details_by_check[detail.inventory_check_id].append(
                InventoryCheckDetailResponse(
                    id=detail.id,
                    material_id=detail.material_id,
                    sku=sku,
                    name=name,
                    unit=unit,
                    system_quantity=detail.system_quantity,
                    actual_quantity=detail.actual_quantity,
                    difference=detail.difference,
                    note=detail.note,
                )
            )

        return [
            self._to_response(
                check,
                details_by_check.get(check.id, []),
            )
            for check in checks
        ]

    def get_inventory_check(
        self,
        inventory_check_id: int,
    ) -> InventoryCheckResponse:
        check = self.db.scalar(
            select(InventoryCheck).where(
                InventoryCheck.id == inventory_check_id,
            )
        )

        if check is None:
            raise AppError(
                "Inventory check not found",
                code="INVENTORY_CHECK_NOT_FOUND",
                status_code=404,
            )

        rows = self.db.execute(
            select(
                InventoryCheckDetail,
                Material.sku,
                Material.name,
                Material.unit,
            )
            .join(
                Material,
                Material.id == InventoryCheckDetail.material_id,
            )
            .where(
                InventoryCheckDetail.inventory_check_id == inventory_check_id,
            )
            .order_by(InventoryCheckDetail.id)
        ).all()

        details = [
            InventoryCheckDetailResponse(
                id=detail.id,
                material_id=detail.material_id,
                sku=sku,
                name=name,
                unit=unit,
                system_quantity=detail.system_quantity,
                actual_quantity=detail.actual_quantity,
                difference=detail.difference,
                note=detail.note,
            )
            for detail, sku, name, unit in rows
        ]

        return self._to_response(check, details)

    def _to_response(
        self,
        check: InventoryCheck,
        details: list[InventoryCheckDetailResponse],
    ) -> InventoryCheckResponse:
        return InventoryCheckResponse(
            id=check.id,
            check_no=check.check_no,
            warehouse_id=check.warehouse_id,
            check_date=check.check_date,
            note=check.note,
            adjustment_transaction_id=check.adjustment_transaction_id,
            created_by=check.created_by,
            created_at=check.created_at,
            details=details,
        )
