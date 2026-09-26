from app import create_app
import pytest
from app.config import TestingConfig
from app.extensions import db
from app.models import Expense, User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test_expenses.db"

    app = create_app(TestingConfig, db_path)

    with app.app_context():

        db.create_all()

        test_user = User(
            user_name="testuser",
            password_hash="test-hash"
        )

        db.session.add(test_user)
        db.session.flush()
    
        expense = Expense(
            user_id=test_user.id,
            name="Test lunch",
            amount=250,
            category="food",
            date="2026-09-15"
        )

        db.session.add(expense)

        db.session.commit()

        app.config["TEST_USER_ID"] = test_user.id

        with app.test_client() as client:
            yield client

        db.session.remove()



@pytest.fixture
def auth_headers(client):
    with client.application.app_context():
        user_id = client.application.config["TEST_USER_ID"]
        access_token = create_access_token(identity=str(user_id))

    return {
        "Authorization": f"Bearer {access_token}"
    }
