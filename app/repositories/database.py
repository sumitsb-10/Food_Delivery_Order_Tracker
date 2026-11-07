
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path


DEFAULT_DATABASE_PATH = (
    Path(__file__).parent.parent.parent
    / "database"
    / "food_delivery.db"
)


def get_connection():
    configured_path = os.environ.get("FOOD_DELIVERY_DATABASE")
    database_path = (
        Path(configured_path).expanduser()
        if configured_path
        else DEFAULT_DATABASE_PATH
    )
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


@contextmanager
def connection_scope():
    """Close a connection reliably and roll back if an operation fails."""
    connection = get_connection()
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


@contextmanager
def transaction():
    """Commit on success, roll back on failure, and always close the connection."""
    with connection_scope() as connection:
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
