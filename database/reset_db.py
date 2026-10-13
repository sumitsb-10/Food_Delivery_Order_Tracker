
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "food_delivery.db"
schema_path = Path(__file__).parent / "schema.sql"

if database_path.exists():
    database_path.unlink()

connection = sqlite3.connect(database_path)
connection.execute("PRAGMA foreign_keys = ON")

with open(schema_path, "r", encoding="utf-8") as file:
    schema = file.read()

connection.executescript(schema)
connection.close()

print("Database reset successfully.")
