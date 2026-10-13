
import os
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = (
    Path(__file__).parent.parent.parent
    / "database"
    / "food_delivery.db"
)


def get_connection():
    database_path = Path(
        os.environ.get(
            "FOOD_DELIVERY_DATABASE",
            DEFAULT_DATABASE_PATH,
        )
    )

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
