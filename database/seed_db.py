
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "food_delivery.db"

connection = sqlite3.connect(database_path)
connection.execute("PRAGMA foreign_keys = ON")

try:
    # Insert sample customers
    connection.executemany("""
        INSERT INTO customers (name, phone, address)
        VALUES (?, ?, ?)
    """, [
        ("Rahul Sharma", "9876543210", "Bengaluru"),
        ("Priya Nair", "9876543211", "Koramangala, Bengaluru"),
        ("Amit Kumar", "9876543212", "Whitefield, Bengaluru"),
    ])

    # Insert sample menu items
    connection.executemany("""
        INSERT INTO menu_items (name, description, price, available)
        VALUES (?, ?, ?, ?)
    """, [
        ("Veg Burger", "Burger with vegetables and cheese", 120.00, True),
        ("Margherita Pizza", "Pizza with tomato and mozzarella", 250.00, True),
        ("French Fries", "Crispy salted potato fries", 100.00, True),
        ("Chicken Burger", "Grilled chicken burger", 180.00, True),
        ("Chocolate Brownie", "Chocolate brownie dessert", 90.00, False),
    ])

    connection.commit()
    print("Sample data inserted successfully.")

except sqlite3.Error:
    connection.rollback()
    raise

finally:
    connection.close()
