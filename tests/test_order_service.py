import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.order_service import (
    create_new_order,
    find_order,
    list_orders
)

from app.services.customer_service import add_customer
from app.services.menu_item_service import add_menu_item


def main():
    # Use a unique phone number so this script can be run repeatedly.
    phone = str(time.time_ns())[-10:]

    # SETUP TEST DATA
    customer_id = add_customer(
        "Order Test Customer",
        phone,
        "Bengaluru",
    )

    burger_id = add_menu_item(
        "Test Burger",
        "Burger for order testing",
        150.00,
        True,
    )

    fries_id = add_menu_item(
        "Test Fries",
        "Fries for order testing",
        80.00,
        True,
    )

    print("Test customer created:", customer_id)
    print("Test burger created:", burger_id)
    print("Test fries created:", fries_id)

    # CREATE ORDER
    order_id = create_new_order(
        customer_id,
        [
            {"menu_item_id": burger_id, "quantity": 1},
            {"menu_item_id": fries_id, "quantity": 2},
        ],
    )

    print("\nCreated order:", order_id)

    # READ ORDER
    order = find_order(order_id)

    print("\nOrder:")
    print(dict(order["order"]))

    print("\nOrder items:")
    for item in order["items"]:
        print(dict(item))

    # VERIFY TOTAL
    expected_total = 150.00 + (80.00 * 2)
    actual_total = order["order"]["total_amount"]

    print("\nExpected total:", expected_total)
    print("Actual total:", actual_total)

    assert actual_total == expected_total
    print("Total calculation: PASS")

    # VERIFY ORDER ITEMS
    assert len(order["items"]) == 2
    print("Order item count: PASS")

    # READ ALL ORDERS
    orders = list_orders()

    print("\nAll orders:")
    for existing_order in orders:
        print(dict(existing_order))

    print("\nOrder service test completed successfully.")


if __name__ == "__main__":
    main()