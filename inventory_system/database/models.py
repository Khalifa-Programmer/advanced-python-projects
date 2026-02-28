import sqlite3
import os

DB_PATH = os.path.join("data", "inventory.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS products ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name TEXT NOT NULL,"
        "quantity INTEGER,"
        "price REAL)"
    )
    conn.commit()
    conn.close()
