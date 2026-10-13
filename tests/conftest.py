import os
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def app(tmp_path):
    original_database = os.environ.get("FOOD_DELIVERY_DATABASE")
    database_path = tmp_path / "test_food_delivery.db"

    schema_path = (
        Path(__file__).parent.parent
        / "database"
        / "schema.sql"
    )

    os.environ["FOOD_DELIVERY_DATABASE"] = str(database_path)

    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(
                schema_path.read_text(encoding="utf-8")
            )

        from app import create_app

        flask_app = create_app()
        flask_app.config["TESTING"] = True

        yield flask_app

    finally:
        if original_database is None:
            os.environ.pop("FOOD_DELIVERY_DATABASE", None)
        else:
            os.environ["FOOD_DELIVERY_DATABASE"] = original_database


@pytest.fixture
def client(app):
    return app.test_client()


from app.repositories.database import get_connection


@pytest.fixture
def sample_records(client):
    """Create test customer and menu items in the test database."""
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
