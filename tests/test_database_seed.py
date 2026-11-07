import sqlite3
from pathlib import Path

from database.seed_db import seed_database


def test_seed_database_is_safe_to_run_repeatedly():
    schema = (
        Path(__file__).parent.parent / "database" / "schema.sql"
    ).read_text(encoding="utf-8")
    connection = sqlite3.connect(":memory:")
    connection.executescript(schema)

    seed_database(connection)
    connection.commit()
    seed_database(connection)
    connection.commit()

    assert connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 3
    assert connection.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0] == 5

    connection.close()
