from sqlalchemy import text

from app.db.session import engine


def main() -> None:
    with engine.begin() as conn:
        # ---------------------------------------------------------
        # 1. Find test warehouses
        # ---------------------------------------------------------
        warehouse_rows = conn.execute(
            text(
                """
                SELECT id
                FROM warehouses
                WHERE code LIKE 'WH-ADJ-%'
                   OR code LIKE 'WH-LOCATION-%'
                   OR code LIKE 'WH-TRANSACTION-%'
                   OR code LIKE 'WH-TEST-%'
                """
            )
        ).all()

        warehouse_ids = [row[0] for row in warehouse_rows]

        print(f"Found {len(warehouse_ids)} test warehouses")

        # ---------------------------------------------------------
        # 2. Find test materials
        # ---------------------------------------------------------
        material_ids: list[int] = []

        if warehouse_ids:
            material_rows = conn.execute(
                text(
                    """
                    SELECT id
                    FROM materials
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            ).all()

            material_ids = [row[0] for row in material_rows]

        print(f"Found {len(material_ids)} test materials")

        # ---------------------------------------------------------
        # 2.1 Find RBAC test materials
        # ---------------------------------------------------------
        rbac_material_rows = conn.execute(
            text(
                """
                SELECT id
                FROM materials
                WHERE sku LIKE 'RBAC-%'
                """
            )
        ).all()

        rbac_material_ids = [row[0] for row in rbac_material_rows]

        material_ids.extend(
            material_id
            for material_id in rbac_material_ids
            if material_id not in material_ids
        )

        print(f"Found {len(rbac_material_ids)} RBAC test materials")

        # ---------------------------------------------------------
        # 3. Find transactions belonging to test warehouses
        # ---------------------------------------------------------
        transaction_ids: list[int] = []

        if warehouse_ids:
            transaction_rows = conn.execute(
                text(
                    """
                    SELECT id
                    FROM transactions
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            ).all()

            transaction_ids = [row[0] for row in transaction_rows]

        print(f"Found {len(transaction_ids)} test transactions")

        # ---------------------------------------------------------
        # 4. Delete Inventory Check Details
        # ---------------------------------------------------------
        if warehouse_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM inventory_check_details
                    WHERE inventory_check_id IN (
                        SELECT id
                        FROM inventory_checks
                        WHERE warehouse_id = ANY(:warehouse_ids)
                    )
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            )
            print(f"Deleted {result.rowcount} inventory check details")

        # ---------------------------------------------------------
        # 5. Delete Inventory Checks
        # ---------------------------------------------------------
        if warehouse_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM inventory_checks
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            )
            print(f"Deleted {result.rowcount} inventory checks")

        # ---------------------------------------------------------
        # 6. Delete Stock Movements
        # ---------------------------------------------------------
        if transaction_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM stock_movements
                    WHERE transaction_id = ANY(:transaction_ids)
                    """
                ),
                {"transaction_ids": transaction_ids},
            )
            print(f"Deleted {result.rowcount} stock movements")

        # ---------------------------------------------------------
        # 7. Delete Transaction Details
        # ---------------------------------------------------------
        if transaction_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM transaction_details
                    WHERE transaction_id = ANY(:transaction_ids)
                    """
                ),
                {"transaction_ids": transaction_ids},
            )
            print(f"Deleted {result.rowcount} transaction details")

        # ---------------------------------------------------------
        # 8. Delete Transactions
        # ---------------------------------------------------------
        if warehouse_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM transactions
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            )
            print(f"Deleted {result.rowcount} transactions")

        # ---------------------------------------------------------
        # 9. Delete Stock Balances
        # ---------------------------------------------------------
        if material_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM stock_balances
                    WHERE material_id = ANY(:material_ids)
                    """
                ),
                {"material_ids": material_ids},
            )
            print(f"Deleted {result.rowcount} stock balances")

        # ---------------------------------------------------------
        # 10. Delete Material ↔ Supplier
        # ---------------------------------------------------------
        if material_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM material_suppliers
                    WHERE material_id = ANY(:material_ids)
                    """
                ),
                {"material_ids": material_ids},
            )
            print(f"Deleted {result.rowcount} material-supplier relations")

        # ---------------------------------------------------------
        # 11. Delete Material ↔ Customer
        # ---------------------------------------------------------
        if material_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM material_customers
                    WHERE material_id = ANY(:material_ids)
                    """
                ),
                {"material_ids": material_ids},
            )
            print(f"Deleted {result.rowcount} material-customer relations")

        # ---------------------------------------------------------
        # 12. Delete Materials
        # ---------------------------------------------------------
        if warehouse_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM materials
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            )
            print(f"Deleted {result.rowcount} materials")

        if material_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM materials
                    WHERE id = ANY(:material_ids)
                    """
                ),
                {"material_ids": material_ids},
            )
            print(f"Deleted {result.rowcount} RBAC test materials")

        # ---------------------------------------------------------
        # 13. Delete test Suppliers
        # ---------------------------------------------------------
        result = conn.execute(
            text(
                """
                DELETE FROM suppliers
                WHERE code LIKE 'SUP-ADJ-%'
                   OR code LIKE 'SUP-LOCATION-%'
                   OR code LIKE 'SUP-TRANSACTION-%'
                   OR code LIKE 'SUP-TEST-%'
                """
            )
        )
        print(f"Deleted {result.rowcount} test suppliers")

        # ---------------------------------------------------------
        # 14. Delete test Customers
        # ---------------------------------------------------------
        result = conn.execute(
            text(
                """
                DELETE FROM customers
                WHERE code LIKE 'CUS-ADJ-%'
                   OR code LIKE 'CUS-LOCATION-%'
                   OR code LIKE 'CUS-TRANSACTION-%'
                   OR code LIKE 'CUS-TEST-%'
                   OR code LIKE 'CUST-%'
                """
            )
        )
        print(f"Deleted {result.rowcount} test customers")

        # ---------------------------------------------------------
        # 15. Delete test Material Categories
        # ---------------------------------------------------------
        result = conn.execute(
            text(
                """
                DELETE FROM material_categories
                WHERE code LIKE 'CAT-ADJ-%'
                   OR code LIKE 'CAT-LOCATION-%'
                   OR code LIKE 'CAT-TRANSACTION-%'
                   OR code LIKE 'CAT-TEST-%'
                """
            )
        )
        print(f"Deleted {result.rowcount} test categories")

        # ---------------------------------------------------------
        # 16. Delete Locations
        # ---------------------------------------------------------
        if warehouse_ids:
            result = conn.execute(
                text(
                    """
                    DELETE FROM locations
                    WHERE warehouse_id = ANY(:warehouse_ids)
                    """
                ),
                {"warehouse_ids": warehouse_ids},
            )
            print(f"Deleted {result.rowcount} locations")

        # ---------------------------------------------------------
        # 17. Delete test Warehouses
        # ---------------------------------------------------------
        result = conn.execute(
            text(
                """
                DELETE FROM warehouses
                WHERE code LIKE 'WH-ADJ-%'
                   OR code LIKE 'WH-LOCATION-%'
                   OR code LIKE 'WH-TRANSACTION-%'
                   OR code LIKE 'WH-TEST-%'
                """
            )
        )
        print(f"Deleted {result.rowcount} test warehouses")

    print("Test data cleanup completed.")


if __name__ == "__main__":
    main()
