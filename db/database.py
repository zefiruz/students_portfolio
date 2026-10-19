import sqlite3

DB_PATH = "data/portfolio.sqlite"


def get_connection():
    """Создать и настроить соединение с базой данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
