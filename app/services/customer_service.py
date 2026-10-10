from app.database import get_connection
from app.models.customer import Customer


def create_customer(name, phone, address):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (name, phone, address)
        VALUES (?, ?, ?)
        """,
        (name, phone, address)
    )

    customer_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return customer_id