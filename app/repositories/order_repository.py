import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "food_delivery.db"


from app.repositories.database import get_connection


def create_order(connection, customer_id, status, total_amount):
    cursor = connection.execute("""
        INSERT INTO orders (customer_id, status, total_amount)
        VALUES (?, ?, ?)
    """, (customer_id, status, total_amount))

    return cursor.lastrowid


def get_order(order_id):
    connection = get_connection()

    order = connection.execute("""
        SELECT id, customer_id, status, total_amount, order_date
        FROM orders
        WHERE id = ?
    """, (order_id,)).fetchone()

    connection.close()

    return order


def get_all_orders():
    connection = get_connection()

    orders = connection.execute("""
        SELECT id, customer_id, status, total_amount, order_date
        FROM orders
        ORDER BY id
    """).fetchall()

    connection.close()

    return orders


def update_order_status(order_id, status):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (status, order_id))

    connection.commit()

    rows_updated = cursor.rowcount
    connection.close()

    return rows_updated


def delete_order(order_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM orders
        WHERE id = ?
    """, (order_id,))

    connection.commit()

    rows_deleted = cursor.rowcount
    connection.close()

    return rows_deleted

def get_orders_by_status(status):
    connection = get_connection()

    orders = connection.execute("""
        SELECT
            id,
            customer_id,
            status,
            total_amount,
            order_date
        FROM orders
        WHERE status = ?
        ORDER BY id
    """, (status,)).fetchall()

    connection.close()

    return orders