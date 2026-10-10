import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "food_delivery.db"

connection = sqlite3.connect(database_path)

cursor = connection.execute("""
    select * from menu_items""")

menu_items = cursor.fetchall()
print("Menu Items:")
for item in menu_items:
    print(item)


connection.close()