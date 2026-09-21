from app import create_app
import pytest
from app.config import TestingConfig
from app.extensions import db
from app.models import Expense

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test_expenses.db"

    app = create_app(TestingConfig, db_path)

    with app.app_context():

        db.create_all()

        expense = Expense(
            name="Test lunch",
            amount=250,
            category="food",
            date="2026-09-15"
        )

        db.session.add(expense)

        db.session.commit()

        with app.test_client() as client:
            yield client

        db.session.remove()
