from app.repositories.database import get_connection

from app.repositories.customer_repository import get_customer
from app.repositories.menu_item_repository import get_menu_item

from app.repositories.order_item_repository import (
    create_order_item,
    get_order_items,
)

from app.repositories.order_repository import (
    create_order,
    get_all_orders,
    get_order,
    update_order_status,
    get_orders_by_status,
)
VALID_STATUS_TRANSITIONS = {
    "PENDING": {"CONFIRMED", "CANCELLED"},
    "CONFIRMED": {"PREPARING", "CANCELLED"},
    "PREPARING": {"OUT_FOR_DELIVERY", "CANCELLED"},
    "OUT_FOR_DELIVERY": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}


def create_new_order(customer_id, items):
    customer = get_customer(customer_id)

    if customer is None:
        raise ValueError("Customer not found.")

    if not items:
        raise ValueError(
            "An order must contain at least one menu item."
        )

    order_items = []
    total_amount = 0

    for item in items:
        menu_item_id = item.get("menu_item_id")
        quantity = item.get("quantity")

        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity <= 0
        ):
            raise ValueError(
                "Order item quantity must be a positive integer."
            )

        menu_item = get_menu_item(menu_item_id)

        if menu_item is None:
            raise ValueError(
                f"Menu item {menu_item_id} not found."
            )

        if not menu_item["available"]:
            raise ValueError(
                f"Menu item {menu_item_id} is not available."
            )

        price = menu_item["price"]

        total_amount += price * quantity

        order_items.append(
            (menu_item_id, quantity, price)
        )

    connection = get_connection()

    try:
        order_id = create_order(
            connection,
            customer_id,
            "PENDING",
            total_amount
        )

        for menu_item_id, quantity, price in order_items:
            create_order_item(
                connection,
                order_id,
                menu_item_id,
                quantity,
                price
            )

        connection.commit()

        return order_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def find_order(order_id):
    order = get_order(order_id)

    if order is None:
        raise ValueError("Order not found.")

    return {
        "order": order,
        "items": get_order_items(order_id),
    }


def list_orders():
    return get_all_orders()

def change_order_status(order_id, new_status):
    order = get_order(order_id)

    if order is None:
        raise ValueError("Order not found.")

    if new_status not in VALID_STATUS_TRANSITIONS:
        raise ValueError(
            f"Invalid order status: {new_status}"
        )

    current_status = order["status"]

    if new_status not in VALID_STATUS_TRANSITIONS[current_status]:
        raise ValueError(
            f"Order cannot move from "
            f"{current_status} to {new_status}."
        )

    rows_updated = update_order_status(
        order_id,
        new_status
    )

    if rows_updated == 0:
        raise ValueError("Order not found.")

    return get_order(order_id)

def list_orders_by_status(status):
    if not isinstance(status, str):
        raise ValueError("Order status must be text.")

    status = status.strip().upper()

    if status not in VALID_STATUS_TRANSITIONS:
        raise ValueError(
            f"Invalid order status: {status}"
        )

    return get_orders_by_status(status)

