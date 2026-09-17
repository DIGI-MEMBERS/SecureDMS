import sqlite3
from pathlib import Path


# Path to the SQLite database
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "securedms.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    # Allows rows to be accessed like dictionaries
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """
    Create all database tables using schema.sql.
    """
    schema_path = BASE_DIR / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    connection = get_connection()

    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("SecureDMS database initialized successfully.")