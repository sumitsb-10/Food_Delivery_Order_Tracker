from app.repositories.database import connection_scope, transaction

def create_menu_item(name, description, price, available):
    with transaction() as connection:
        cursor = connection.execute(
            """INSERT INTO menu_items (name, description, price, available)
               VALUES (?, ?, ?, ?)""",
            (name, description, price, available),
        )
        return cursor.lastrowid


def get_menu_item(menu_item_id):
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, description, price, available, created_at
               FROM menu_items WHERE id = ?""",
            (menu_item_id,),
        ).fetchone()


def get_all_menu_items():
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, description, price, available, created_at
               FROM menu_items ORDER BY id"""
        ).fetchall()

def search_menu_items(search_term):
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, description, price, available, created_at
               FROM menu_items WHERE LOWER(name) LIKE LOWER(?) ORDER BY id""",
            (f"%{search_term}%",),
        ).fetchall()


def update_menu_item(menu_item_id, name, description, price, available):
    with transaction() as connection:
        cursor = connection.execute(
            """UPDATE menu_items SET name = ?, description = ?, price = ?, available = ?
               WHERE id = ?""",
            (name, description, price, available, menu_item_id),
        )
        return cursor.rowcount


def delete_menu_item(menu_item_id):
    with transaction() as connection:
        cursor = connection.execute(
            "DELETE FROM menu_items WHERE id = ?", (menu_item_id,)
        )
        return cursor.rowcount

def get_available_menu_items():
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, description, price, available, created_at
               FROM menu_items WHERE available = 1 ORDER BY id"""
        ).fetchall()
