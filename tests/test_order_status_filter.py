import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.services.customer_service import add_customer
from app.services.menu_item_service import add_menu_item
from app.services.order_service import (
    create_new_order,
    change_order_status,
    list_orders_by_status,
)


def create_test_order(customer_id, menu_item_id):
    return create_new_order(
        customer_id,
        [
            {
                "menu_item_id": menu_item_id,
                "quantity": 1
            }
        ]
    )


def main():
    phone = str(time.time_ns())[-10:]

    customer_id = add_customer(
        "Order Filter Customer",
        phone,
        "Bengaluru"
    )

    menu_item_id = add_menu_item(
        "Order Filter Burger",
        "Burger for order filter testing",
        200.00,
        True
    )

    # Order 1 remains PENDING.
    pending_order_id = create_test_order(
        customer_id,
        menu_item_id
    )

    # Order 2 becomes CONFIRMED.
    confirmed_order_id = create_test_order(
        customer_id,
        menu_item_id
    )

    change_order_status(
        confirmed_order_id,
        "CONFIRMED"
    )

    # Order 3 becomes PREPARING.
    preparing_order_id = create_test_order(
        customer_id,
        menu_item_id
    )

    change_order_status(
        preparing_order_id,
        "CONFIRMED"
    )

    change_order_status(
        preparing_order_id,
        "PREPARING"
    )

    print("Created orders:")
    print("Pending:", pending_order_id)
    print("Confirmed:", confirmed_order_id)
    print("Preparing:", preparing_order_id)

    # Filter PENDING orders.
    pending_orders = list_orders_by_status("PENDING")

    pending_ids = {
        order["id"]
        for order in pending_orders
    }

    assert pending_order_id in pending_ids
    assert confirmed_order_id not in pending_ids
    assert preparing_order_id not in pending_ids

    print("\nPENDING filter: PASS")

    # Filter CONFIRMED orders.
    confirmed_orders = list_orders_by_status("confirmed")

    confirmed_ids = {
        order["id"]
        for order in confirmed_orders
    }

    assert confirmed_order_id in confirmed_ids
    assert preparing_order_id not in confirmed_ids

    print("CONFIRMED filter: PASS")

    # Filter PREPARING orders.
    preparing_orders = list_orders_by_status("  preparing  ")

    preparing_ids = {
        order["id"]
        for order in preparing_orders
    }

    assert preparing_order_id in preparing_ids

    print("PREPARING filter: PASS")

    # Invalid status.
    try:
        list_orders_by_status("WAITING")

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError as error:
        print("Invalid status validation: PASS")
        print("Expected error:", error)

    print("\nOrder status filter test completed successfully.")


if __name__ == "__main__":
    main()