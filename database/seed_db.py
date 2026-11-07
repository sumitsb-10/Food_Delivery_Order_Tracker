import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "food_delivery.db"

SAMPLE_CUSTOMERS = (
    ("Rahul Sharma", "9876543210", "Bengaluru"),
    ("Priya Nair", "9876543211", "Koramangala, Bengaluru"),
    ("Amit Kumar", "9876543212", "Whitefield, Bengaluru"),
)

SAMPLE_MENU_ITEMS = (
    ("Veg Burger", "Burger with vegetables and cheese", 120.00, True),
    ("Margherita Pizza", "Pizza with tomato and mozzarella", 250.00, True),
    ("French Fries", "Crispy salted potato fries", 100.00, True),
    ("Chicken Burger", "Grilled chicken burger", 180.00, True),
    ("Chocolate Brownie", "Chocolate brownie dessert", 90.00, False),
)


def seed_database(connection):
    connection.executemany(
        """
        INSERT OR IGNORE INTO customers (name, phone, address)
        VALUES (?, ?, ?)
        """,
        SAMPLE_CUSTOMERS,
    )

    for menu_item in SAMPLE_MENU_ITEMS:
        name, description, price, available = menu_item
        exists = connection.execute(
            "SELECT 1 FROM menu_items WHERE name = ? LIMIT 1",
            (name,),
        ).fetchone()

        if exists is None:
            connection.execute(
                """
                INSERT INTO menu_items (name, description, price, available)
                VALUES (?, ?, ?, ?)
                """,
                menu_item,
            )


def main():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        seed_database(connection)
        connection.commit()
        print("Sample data is ready.")
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
