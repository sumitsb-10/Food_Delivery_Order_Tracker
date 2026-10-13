
import pytest

from app.repositories.database import get_connection
from app.services.order_service import (
    create_new_order,
    find_order,
    list_orders,
)


@pytest.fixture
def sample_records(client):
    """Create test customer and menu items in the isolated test database."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO customers (name, phone, address)
            VALUES (?, ?, ?)
            """,
            ("Test Customer", "9876543210", "Test Address"),
        )
        customer_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO menu_items (id, name, description, price, available)
            VALUES (?, ?, ?, ?, ?)
            """,
            (101, "Test Burger", "Test item", 100.00, 1),
        )

        connection.execute(
            """
            INSERT INTO menu_items (id, name, description, price, available)
            VALUES (?, ?, ?, ?, ?)
            """,
            (102, "Test Pizza", "Test item", 200.00, 1),
        )

        connection.commit()

        return {
            "customer_id": customer_id,
            "burger_id": 101,
            "pizza_id": 102,
        }
    finally:
        connection.close()


def test_create_order_success(client, sample_records):
    order_id = create_new_order(
        customer_id=sample_records["customer_id"],
        items=[
            {"menu_item_id": sample_records["burger_id"], "quantity": 2},
            {"menu_item_id": sample_records["pizza_id"], "quantity": 1},
        ],
    )

    result = find_order(order_id)

    assert result["order"]["id"] == order_id
    assert result["order"]["customer_id"] == sample_records["customer_id"]
    assert result["order"]["status"] == "PENDING"
    assert float(result["order"]["total_amount"]) == pytest.approx(400.00)
    assert len(result["items"]) == 2


def test_create_order_rejects_empty_items(client, sample_records):
    with pytest.raises(ValueError, match="at least one menu item"):
        create_new_order(
            customer_id=sample_records["customer_id"],
            items=[],
        )


def test_create_order_rejects_invalid_customer(client, sample_records):
    with pytest.raises(ValueError, match="Customer not found"):
        create_new_order(
            customer_id=99999,
            items=[
                {
                    "menu_item_id": sample_records["burger_id"],
                    "quantity": 1,
                }
            ],
        )


def test_find_order_rejects_missing_order(client):
    with pytest.raises(ValueError, match="Order not found"):
        find_order(99999)


def test_list_orders_returns_created_order(client, sample_records):
    order_id = create_new_order(
        customer_id=sample_records["customer_id"],
        items=[
            {
                "menu_item_id": sample_records["burger_id"],
                "quantity": 1,
            }
        ],
    )

    orders = list_orders()

    assert any(order["id"] == order_id for order in orders)
