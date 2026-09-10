import sqlite3
from flask import current_app



def get_db_connection():
    connection = sqlite3.connect(
        current_app.config["DATABASE"]
    )
    connection.row_factory = sqlite3.Row
    return connection



def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
            )
    """)

    connection.commit()
    connection.close()
    