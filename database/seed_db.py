import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "food_delivery.db"

connection = sqlite3.connect(database_path)
connection.execute("PRAGMA foreign_keys = ON")




print("Customer inserted successfully.")

connection.execute("""
    INSERT INTO menu_items (name, description, price, available)
    VALUES (?, ?, ?, ?)
""", ("Veg Burger", "Burger with vegetables and cheese", 120.00, True))

connection.execute("""
    INSERT INTO menu_items (name, description, price, available)
    VALUES (?, ?, ?, ?)
""", ("Margherita Pizza", "Pizza with tomato and mozzarella", 250.00, True))

connection.execute("""
    INSERT INTO menu_items (name, description, price, available)
    VALUES (?, ?, ?, ?)
""", ("French Fries", "Crispy salted potato fries", 100.00, True))
connection.commit()
connection.close()