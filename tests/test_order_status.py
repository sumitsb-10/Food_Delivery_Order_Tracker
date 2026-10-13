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


def main():
    phone = str(time.time_ns())[-10:]

    customer_id = add_customer(
        "Status Test Customer",
        phone,
        "Bengaluru"
    )

    menu_item_id = add_menu_item(
        "Status Test Burger",
        "Burger for status testing",
        180.00,
        True
    )

    order_id = create_new_order(
        customer_id,
        [
            {
                "menu_item_id": menu_item_id,
                "quantity": 1
            }
        ]
    )

    print("Created order:", order_id)

    # PENDING → CONFIRMED
    order = change_order_status(
        order_id,
        "CONFIRMED"
    )

    assert order["status"] == "CONFIRMED"
    print("PENDING -> CONFIRMED: PASS")

    # CONFIRMED → PREPARING
    order = change_order_status(
        order_id,
        "PREPARING"
    )

    assert order["status"] == "PREPARING"
    print("CONFIRMED -> PREPARING: PASS")

    # PREPARING → OUT_FOR_DELIVERY
    order = change_order_status(
        order_id,
        "OUT_FOR_DELIVERY"
    )

    assert order["status"] == "OUT_FOR_DELIVERY"
    print("PREPARING -> OUT_FOR_DELIVERY: PASS")

    # OUT_FOR_DELIVERY → DELIVERED
    order = change_order_status(
        order_id,
        "DELIVERED"
    )

    assert order["status"] == "DELIVERED"
    print("OUT_FOR_DELIVERY -> DELIVERED: PASS")

    # DELIVERED → PENDING should fail
    try:
        change_order_status(
            order_id,
            "PENDING"
        )
        assert False, "Expected ValueError was not raised."

    except ValueError as error:
        print("DELIVERED -> PENDING: PASS")
        print("Expected error:", error)

    print("\nOrder status test completed successfully.")


if __name__ == "__main__":
    main()