import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.repositories.database import get_connection
from app.repositories.order_repository import create_order
from app.repositories.order_item_repository import create_order_item
from app.services.customer_service import add_customer
from app.services.menu_item_service import add_menu_item


def main():
    phone = str(time.time_ns())[-10:]

    customer_id = add_customer(
        "Transaction Test Customer",
        phone,
        "Bengaluru"
    )

    menu_item_id = add_menu_item(
        "Transaction Test Burger",
        "Burger for transaction testing",
        200.00,
        True
    )

    connection = get_connection()

    try:
        order_id = create_order(
            connection,
            customer_id,
            "PENDING",
            200.00
        )

        print("Created order inside transaction:", order_id)

        create_order_item(
            connection,
            order_id,
            menu_item_id,
            1,
            200.00
        )

        print("First order item created.")

        # Deliberately use an invalid menu_item_id.
        create_order_item(
            connection,
            order_id,
            999999,
            1,
            100.00
        )

        connection.commit()

    except Exception as error:
        print("Expected error:", error)
        print("Rolling back transaction...")
        connection.rollback()

    finally:
        connection.close()

    # Verify that the order was rolled back.
    verification_connection = get_connection()

    order = verification_connection.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    items = verification_connection.execute(
        """
        SELECT *
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchall()

    verification_connection.close()

    print("\nOrder after rollback:", order)
    print("Order items after rollback:", items)

    assert order is None
    print("Order rollback: PASS")

    assert len(items) == 0
    print("Order item rollback: PASS")

    print("\nTransaction test completed successfully.")


if __name__ == "__main__":
    main()