
from app.repositories.database import get_connection


def create_order_item(
    connection,
    order_id,
    menu_item_id,
    quantity,
    price,
):
    cursor = connection.execute(
        """
        INSERT INTO order_items (
            order_id,
            menu_item_id,
            quantity,
            price
        )
        VALUES (?, ?, ?, ?)
        """,
        (order_id, menu_item_id, quantity, price),
    )

    return cursor.lastrowid


def get_order_items(order_id):
    connection = get_connection()

    try:
        items = connection.execute(
            """
            SELECT
                order_items.id,
                order_items.order_id,
                order_items.menu_item_id,
                menu_items.name,
                order_items.quantity,
                order_items.price
            FROM order_items
            JOIN menu_items
                ON order_items.menu_item_id = menu_items.id
            WHERE order_items.order_id = ?
            ORDER BY order_items.id
            """,
            (order_id,),
        ).fetchall()

        return items
    finally:
        connection.close()


def delete_order_items(order_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM order_items
            WHERE order_id = ?
            """,
            (order_id,),
        )

        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
