from app.repositories.database import get_connection

def create_menu_item(name, description, price, available):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO menu_items (name, description, price, available)
        VALUES (?, ?, ?, ?)
    """, (name, description, price, available))

    connection.commit()

    menu_item_id = cursor.lastrowid
    connection.close()

    return menu_item_id


def get_menu_item(menu_item_id):
    connection = get_connection()

    menu_item = connection.execute("""
        SELECT id, name, description, price, available, created_at
        FROM menu_items
        WHERE id = ?
    """, (menu_item_id,)).fetchone()

    connection.close()

    return menu_item


def get_all_menu_items():
    connection = get_connection()

    menu_items = connection.execute("""
        SELECT id, name, description, price, available, created_at
        FROM menu_items
        ORDER BY id
    """).fetchall()

    connection.close()

    return menu_items

def search_menu_items(search_term):
    connection = get_connection()

    menu_items = connection.execute("""
        SELECT
            id,
            name,
            description,
            price,
            available,
            created_at
        FROM menu_items
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY id
    """, (f"%{search_term}%",)).fetchall()

    connection.close()

    return menu_items


def update_menu_item(menu_item_id, name, description, price, available):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE menu_items
        SET name = ?, description = ?, price = ?, available = ?
        WHERE id = ?
    """, (name, description, price, available, menu_item_id))

    connection.commit()

    rows_updated = cursor.rowcount
    connection.close()

    return rows_updated


def delete_menu_item(menu_item_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM menu_items
        WHERE id = ?
    """, (menu_item_id,))

    connection.commit()

    rows_deleted = cursor.rowcount
    connection.close()

    return rows_deleted

def get_available_menu_items():
    connection = get_connection()

    menu_items = connection.execute("""
        SELECT
            id,
            name,
            description,
            price,
            available,
            created_at
        FROM menu_items
        WHERE available = 1
        ORDER BY id
    """).fetchall()

    connection.close()

    return menu_items