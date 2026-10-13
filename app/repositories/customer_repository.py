import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "food_delivery.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_customer(name, phone, address):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO customers (name, phone, address)
        VALUES (?, ?, ?)
    """, (name, phone, address))

    connection.commit()

    customer_id = cursor.lastrowid

    connection.close()

    return customer_id


def get_customer(customer_id):
    connection = get_connection()

    customer = connection.execute("""
        SELECT id, name, phone, address, created_at
        FROM customers
        WHERE id = ?
    """, (customer_id,)).fetchone()

    connection.close()

    return customer


def get_all_customers():
    connection = get_connection()

    customers = connection.execute("""
        SELECT id, name, phone, address, created_at
        FROM customers
        ORDER BY id
    """).fetchall()

    connection.close()

    return customers
def update_customer(customer_id, name, phone, address):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE customers
        SET name = ?, phone = ?, address = ?
        WHERE id = ?
    """, (name, phone, address, customer_id))

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated


def delete_customer(customer_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM customers
        WHERE id = ?
    """, (customer_id,))

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted

def search_customers(search_term):
    connection = get_connection()

    customers = connection.execute("""
        SELECT
            id,
            name,
            phone,
            address,
            created_at
        FROM customers
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY id
    """, (f"%{search_term}%",)).fetchall()

    connection.close()

    return customers