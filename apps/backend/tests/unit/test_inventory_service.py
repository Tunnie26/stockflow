from decimal import Decimal
from unittest.mock import MagicMock

from app.models.stock_balance import StockBalance
from app.models.stock_movement import StockMovement
from app.services.inventory_service import InventoryService


def make_detail(
    material_id: int = 1,
    transaction_id: int = 1,
    detail_id: int = 1,
    quantity: str = "10",
) -> MagicMock:
    return MagicMock(
        material_id=material_id,
        transaction_id=transaction_id,
        id=detail_id,
        quantity=Decimal(quantity),
    )


def make_balance(
    material_id: int = 1,
    quantity: str = "100",
) -> MagicMock:
    return MagicMock(
        material_id=material_id,
        quantity=Decimal(quantity),
    )


def test_apply_inbound_increases_stock():
    db = MagicMock()

    detail = make_detail(quantity="50")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_inbound(detail)

    assert balance.quantity == Decimal("150")

    assert isinstance(movement, StockMovement)
    assert movement.transaction_id == detail.transaction_id
    assert movement.transaction_detail_id == detail.id
    assert movement.material_id == detail.material_id
    assert movement.quantity == Decimal("50")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_apply_outbound_decreases_stock():
    db = MagicMock()

    detail = make_detail(quantity="30")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_outbound(detail)

    assert balance.quantity == Decimal("70")

    assert isinstance(movement, StockMovement)
    assert movement.quantity == Decimal("-30")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_apply_transfer_decreases_stock_only():
    db = MagicMock()

    detail = make_detail(quantity="40")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_transfer(detail)

    assert balance.quantity == Decimal("60")

    assert isinstance(movement, StockMovement)
    assert movement.quantity == Decimal("-40")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_apply_transfer_does_not_create_destination_stock():
    db = MagicMock()

    detail = make_detail(quantity="20")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    service.apply_transfer(detail)

    assert db.scalar.call_count == 1
    assert db.add.call_count == 1


def test_apply_adjustment_decreases_stock():
    db = MagicMock()

    detail = make_detail(quantity="0")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_adjustment(
        detail,
        actual_quantity=Decimal("85"),
    )

    assert balance.quantity == Decimal("85")

    assert isinstance(movement, StockMovement)
    assert movement.quantity == Decimal("-15")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_apply_adjustment_increases_stock():
    db = MagicMock()

    detail = make_detail(quantity="0")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_adjustment(
        detail,
        actual_quantity=Decimal("120"),
    )

    assert balance.quantity == Decimal("120")

    assert isinstance(movement, StockMovement)
    assert movement.quantity == Decimal("20")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_apply_adjustment_same_quantity_creates_zero_movement():
    db = MagicMock()

    detail = make_detail(quantity="0")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_adjustment(
        detail,
        actual_quantity=Decimal("100"),
    )

    assert balance.quantity == Decimal("100")
    assert movement.quantity == Decimal("0")

    db.add.assert_called_once_with(movement)
    db.flush.assert_called_once()


def test_get_or_create_balance_creates_new_balance():
    db = MagicMock()

    db.scalar.return_value = None

    detail = make_detail(quantity="50")

    service = InventoryService(db)

    movement = service.apply_inbound(detail)

    added_objects = [call.args[0] for call in db.add.call_args_list]

    balance = next(obj for obj in added_objects if isinstance(obj, StockBalance))

    movement_obj = next(obj for obj in added_objects if isinstance(obj, StockMovement))

    assert balance.material_id == detail.material_id
    assert balance.quantity == Decimal("50")

    assert movement_obj is movement
    assert movement_obj.quantity == Decimal("50")

    assert db.add.call_count == 2
    assert db.flush.call_count == 2


def test_outbound_allows_negative_stock():
    db = MagicMock()

    detail = make_detail(quantity="150")
    balance = make_balance(quantity="100")

    db.scalar.return_value = balance

    service = InventoryService(db)

    movement = service.apply_outbound(detail)

    assert balance.quantity == Decimal("-50")
    assert movement.quantity == Decimal("-150")


def test_apply_adjustment_without_existing_balance():
    db = MagicMock()

    detail = make_detail(quantity="0")

    db.scalar.return_value = None

    service = InventoryService(db)

    movement = service.apply_adjustment(
        detail,
        actual_quantity=Decimal("25"),
    )

    added_objects = [call.args[0] for call in db.add.call_args_list]

    balance = next(obj for obj in added_objects if isinstance(obj, StockBalance))

    movement_obj = next(obj for obj in added_objects if isinstance(obj, StockMovement))

    assert balance.material_id == detail.material_id
    assert balance.quantity == Decimal("25")

    assert movement_obj is movement
    assert movement_obj.transaction_id == detail.transaction_id
    assert movement_obj.transaction_detail_id == detail.id
    assert movement_obj.material_id == detail.material_id
    assert movement_obj.quantity == Decimal("25")

    assert db.add.call_count == 2
    assert db.flush.call_count == 2
