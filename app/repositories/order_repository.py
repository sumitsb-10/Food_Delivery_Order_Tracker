
from app.repositories.database import connection_scope, get_connection, transaction


def create_order(connection, customer_id, status, total_amount):
    cursor = connection.execute(
        """
        INSERT INTO orders (customer_id, status, total_amount)
        VALUES (?, ?, ?)
        """,
        (customer_id, status, str(total_amount)),
    )

    return cursor.lastrowid


def get_order(order_id):
    with connection_scope() as connection:
        return connection.execute(
            """
            SELECT id, customer_id, status, total_amount, order_date
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        ).fetchone()


def get_all_orders():
    with connection_scope() as connection:
        return connection.execute(
            """
            SELECT id, customer_id, status, total_amount, order_date
            FROM orders
            ORDER BY id
            """
        ).fetchall()


def update_order_status(order_id, status, expected_status=None):
    with transaction() as connection:
        if expected_status is None:
            cursor = connection.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (status, order_id),
            )
        else:
            cursor = connection.execute(
                "UPDATE orders SET status = ? WHERE id = ? AND status = ?",
                (status, order_id, expected_status),
            )
        return cursor.rowcount


def delete_order(order_id):
    with transaction() as connection:
        cursor = connection.execute(
            "DELETE FROM orders WHERE id = ?",
            (order_id,),
        )
        return cursor.rowcount


def get_orders_by_status(status):
    with connection_scope() as connection:
        return connection.execute(
            """
            SELECT id, customer_id, status, total_amount, order_date
            FROM orders
            WHERE status = ?
            ORDER BY id
            """,
            (status,),
        ).fetchall()
