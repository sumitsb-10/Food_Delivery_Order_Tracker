
from app.repositories.database import connection_scope, transaction


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
        (order_id, menu_item_id, quantity, str(price)),
    )

    return cursor.lastrowid


def get_order_items(order_id):
    with connection_scope() as connection:
        return connection.execute(
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


def delete_order_items(order_id):
    with transaction() as connection:
        cursor = connection.execute(
            """
            DELETE FROM order_items
            WHERE order_id = ?
            """,
            (order_id,),
        )

        return cursor.rowcount
