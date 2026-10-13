import sys
import time
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.services.order_service import create_new_order
from app.services.customer_service import add_customer
from app.services.menu_item_service import add_menu_item


def expect_error(test_name, function, expected_message):
    try:
        function()

        print(f"{test_name}: FAIL")
        print("Expected an error but no error was raised.")

    except ValueError as error:
        if str(error) == expected_message:
            print(f"{test_name}: PASS")
        else:
            print(f"{test_name}: FAIL")
            print("Expected:", expected_message)
            print("Actual:", str(error))


def main():

    # --------------------------------------------------
    # SETUP TEST DATA
    # --------------------------------------------------

    phone = str(time.time_ns())[-10:]

    customer_id = add_customer(
        "Validation Test Customer",
        phone,
        "Bengaluru"
    )

    available_item_id = add_menu_item(
        "Validation Burger",
        "Burger for validation testing",
        150.00,
        True
    )

    unavailable_item_id = add_menu_item(
        "Unavailable Burger",
        "Burger currently unavailable",
        180.00,
        False
    )

    print("Test customer:", customer_id)
    print("Available item:", available_item_id)
    print("Unavailable item:", unavailable_item_id)


    # --------------------------------------------------
    # TEST 1: CUSTOMER DOES NOT EXIST
    # --------------------------------------------------

    expect_error(
        "Nonexistent customer",
        lambda: create_new_order(
            999999,
            [
                {
                    "menu_item_id": available_item_id,
                    "quantity": 1
                }
            ]
        ),
        "Customer not found."
    )


    # --------------------------------------------------
    # TEST 2: EMPTY ORDER
    # --------------------------------------------------

    expect_error(
        "Empty order",
        lambda: create_new_order(
            customer_id,
            []
        ),
        "An order must contain at least one menu item."
    )


    # --------------------------------------------------
    # TEST 3: QUANTITY = 0
    # --------------------------------------------------

    expect_error(
        "Zero quantity",
        lambda: create_new_order(
            customer_id,
            [
                {
                    "menu_item_id": available_item_id,
                    "quantity": 0
                }
            ]
        ),
        "Order item quantity must be a positive integer."
    )


    # --------------------------------------------------
    # TEST 4: NEGATIVE QUANTITY
    # --------------------------------------------------

    expect_error(
        "Negative quantity",
        lambda: create_new_order(
            customer_id,
            [
                {
                    "menu_item_id": available_item_id,
                    "quantity": -2
                }
            ]
        ),
        "Order item quantity must be a positive integer."
    )


    # --------------------------------------------------
    # TEST 5: MENU ITEM DOES NOT EXIST
    # --------------------------------------------------

    expect_error(
        "Nonexistent menu item",
        lambda: create_new_order(
            customer_id,
            [
                {
                    "menu_item_id": 999999,
                    "quantity": 1
                }
            ]
        ),
        "Menu item 999999 not found."
    )


    # --------------------------------------------------
    # TEST 6: MENU ITEM NOT AVAILABLE
    # --------------------------------------------------

    expect_error(
        "Unavailable menu item",
        lambda: create_new_order(
            customer_id,
            [
                {
                    "menu_item_id": unavailable_item_id,
                    "quantity": 1
                }
            ]
        ),
       f"Menu item {unavailable_item_id} is not available."
    )


    print("\nOrder validation tests completed.")


if __name__ == "__main__":
    main()
