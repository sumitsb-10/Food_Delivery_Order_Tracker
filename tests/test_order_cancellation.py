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
)


def create_test_order():
    phone = str(time.time_ns())[-10:]

    customer_id = add_customer(
        "Cancellation Test Customer",
        phone,
        "Bengaluru"
    )

    menu_item_id = add_menu_item(
        "Cancellation Test Burger",
        "Burger for cancellation testing",
        200.00,
        True
    )

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

    # PENDING -> CANCELLED
    order_id = create_test_order()

    order = change_order_status(
        order_id,
        "CANCELLED"
    )

    assert order["status"] == "CANCELLED"

    print("PENDING -> CANCELLED: PASS")


    # CONFIRMED -> CANCELLED
    order_id = create_test_order()

    change_order_status(
        order_id,
        "CONFIRMED"
    )

    order = change_order_status(
        order_id,
        "CANCELLED"
    )

    assert order["status"] == "CANCELLED"

    print("CONFIRMED -> CANCELLED: PASS")


    # PREPARING -> CANCELLED
    order_id = create_test_order()

    change_order_status(
        order_id,
        "CONFIRMED"
    )

    change_order_status(
        order_id,
        "PREPARING"
    )

    order = change_order_status(
        order_id,
        "CANCELLED"
    )

    assert order["status"] == "CANCELLED"

    print("PREPARING -> CANCELLED: PASS")


    # OUT_FOR_DELIVERY -> CANCELLED should fail
    order_id = create_test_order()

    change_order_status(
        order_id,
        "CONFIRMED"
    )

    change_order_status(
        order_id,
        "PREPARING"
    )

    change_order_status(
        order_id,
        "OUT_FOR_DELIVERY"
    )

    try:
        change_order_status(
            order_id,
            "CANCELLED"
        )

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError as error:
        print("OUT_FOR_DELIVERY -> CANCELLED: PASS")
        print("Expected error:", error)


    # DELIVERED -> CANCELLED should fail
    order_id = create_test_order()

    change_order_status(
        order_id,
        "CONFIRMED"
    )

    change_order_status(
        order_id,
        "PREPARING"
    )

    change_order_status(
        order_id,
        "OUT_FOR_DELIVERY"
    )

    change_order_status(
        order_id,
        "DELIVERED"
    )

    try:
        change_order_status(
            order_id,
            "CANCELLED"
        )

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError as error:
        print("DELIVERED -> CANCELLED: PASS")
        print("Expected error:", error)


    print("\nOrder cancellation test completed successfully.")


if __name__ == "__main__":
    main()