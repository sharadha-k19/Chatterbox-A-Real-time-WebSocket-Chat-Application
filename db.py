import sqlite3

def get_db_connection():
    conn = sqlite3.connect(
        "chat.db",
        timeout=20,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn