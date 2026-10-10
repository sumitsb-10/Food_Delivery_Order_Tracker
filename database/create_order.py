import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "food_delivery.db"

connection = sqlite3.connect(database_path)
connection.execute("PRAGMA foreign_keys = ON")

# Create the order
cursor = connection.execute("""
    INSERT INTO orders (customer_id, status, total_amount)
    VALUES (?, ?, ?)
""", (1, "PENDING", 320.00))

order_id = cursor.lastrowid

# Add Veg Burger
connection.execute("""
    INSERT INTO order_items (order_id, menu_item_id, quantity, price)
    VALUES (?, ?, ?, ?)
""", (order_id, 1, 1, 120.00))

# Add French Fries
connection.execute("""
    INSERT INTO order_items (order_id, menu_item_id, quantity, price)
    VALUES (?, ?, ?, ?)
""", (order_id, 3, 2, 100.00))

connection.commit()
connection.close()

print(f"Order {order_id} created successfully.")