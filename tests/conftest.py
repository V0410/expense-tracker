from app import create_app
import pytest
from app.database import init_db, get_db_connection

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test_expenses.db"

    app = create_app()

    app.config["TESTING"] = True
    app.config["DATABASE"] = str(db_path)

    with app.app_context():
        init_db()

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO expenses
            (name, amount, category, date)
            VALUES
            (?, ?, ?, ?)
        """, ("Test lunch",  250.0, "food", "2026-09-01"))

        connection.execute("""
            INSERT INTO expenses
            (name, amount, category, date)
            VALUES
            (?, ?, ?, ?)
        """, ("Test bus", 40.0, "transport", "2026-09-02"))

        connection.commit()
        connection.close()

    with app.test_client() as client:
        yield client