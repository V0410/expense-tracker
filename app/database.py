import sqlite3
from flask import current_app, g



def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect(
        current_app.config["DATABASE"]
    )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db_connection(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()



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
    
