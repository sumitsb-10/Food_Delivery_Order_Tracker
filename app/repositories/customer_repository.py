from app.repositories.database import connection_scope, transaction


def create_customer(name, phone, address):
    with transaction() as connection:
        cursor = connection.execute(
            """INSERT INTO customers (name, phone, address)
               VALUES (?, ?, ?)""",
            (name, phone, address),
        )
        return cursor.lastrowid


def get_customer(customer_id):
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, phone, address, created_at
               FROM customers WHERE id = ?""",
            (customer_id,),
        ).fetchone()


def get_all_customers():
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, phone, address, created_at
               FROM customers ORDER BY id"""
        ).fetchall()
def update_customer(customer_id, name, phone, address):
    with transaction() as connection:
        cursor = connection.execute(
            """UPDATE customers SET name = ?, phone = ?, address = ?
               WHERE id = ?""",
            (name, phone, address, customer_id),
        )
        return cursor.rowcount


def delete_customer(customer_id):
    with transaction() as connection:
        cursor = connection.execute(
            "DELETE FROM customers WHERE id = ?", (customer_id,)
        )
        return cursor.rowcount

def search_customers(search_term):
    with connection_scope() as connection:
        return connection.execute(
            """SELECT id, name, phone, address, created_at
               FROM customers WHERE LOWER(name) LIKE LOWER(?) ORDER BY id""",
            (f"%{search_term}%",),
        ).fetchall()
