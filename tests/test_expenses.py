def test_get_expenses(client):
    response = client.get("/expenses")

    assert response.status_code == 200


def test_get_nonexistent_expenses(client):
    response = client.get("/expenses/99999")

    assert response.status_code == 404


def test_get_expenses_with_invalid_id(client):
    response = client.get("/expenses/abc")

    assert response.status_code == 404


def test_create_expense(client):
    response = client.post(
        "/expenses",
        json = {
            "name": "Coffee",
            "amount": 120.50,
            "category": "food"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Expense Created"
    assert data["expense"]["name"] == "Coffee"
    assert data["expense"]["amount"] == 120.50
    assert data["expense"]["category"] == "food"



def test_create_expense_persists(client):
    response = client.post(
        "/expenses",
        json = {
            "name": "Coffee",
            "amount": 120.50,
            "category": "food"
        }
    )

    assert response.status_code == 201

    created = response.get_json()["expense"]

    expense_id = created["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200

    expense = response.get_json()

    assert expense["name"] == "Coffee"
    assert expense["amount"] == 120.50
    assert expense["category"] == "food"



def test_create_expense_invalid_amount(client):
    response = client.post(
        "/expenses",
        json = {
            "name": "Coffee",
            "amount": -50,
            "category": "food"
        }
    )

    assert response.status_code == 400



def test_create_expense_missing_name(client):
    response = client.post(
        "/expenses",
        json = {
            "amount": 100,
            "category": "food"
        }
    )

    assert response.status_code == 400



def test_update_expense(client):
    response = client.put(
        "/expenses/1",
        json = {
            "name": "Updated lunch",
            "amount": 300.50,
            "category": "food"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Expense updated successfully"
    assert data["expense"]["id"] == 1
    assert data["expense"]["name"] == "Updated lunch"
    assert data["expense"]["amount"] == 300.50
    assert data["expense"]["category"] == "food"



def test_update_expense_persists(client):
    response = client.put(
            "/expenses/1",
            json = {
                "name": "Updated lunch",
                "amount": 300.50,
                "category": "food"
            }
        )
    
    assert response.status_code == 200

    updated = response.get_json()["expense"]

    expense_id = updated["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200

    expense = response.get_json()

    assert expense["name"] == "Updated lunch"
    assert expense["amount"] == 300.50
    assert expense["category"] == "food"



def test_update_nonexistent_expense(client):
    response = client.put(
        "/expenses/999",
        json = {
            "name": "Updated lunch",
            "amount": 300.50,
            "category": "food"
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Expense not found"



def test_update_expense_invalid_amount(client):
    response = client.put(
        "/expenses/1",
        json = {
            "name": "Updated lunch",
            "amount": -50,
            "category": "food"
        }
    )

    assert response.status_code == 400



def test_update_expense_missing_name(client):
    response = client.put(
        "/expenses/1",
        json = {
            "amount": 100,
            "category": "food"
        }
    )

    assert response.status_code == 400



def test_delete_expense(client):
    response = client.delete("/expenses/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Expense deleted successfully"



def test_delete_expense_persists(client):
    response = client.delete("/expenses/1")

    assert response.status_code == 200

    response = client.get("expenses/1")

    assert response.status_code == 404



def test_delete_nonexistent_expense(client):
    response = client.delete("/expenses/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Expense not found"



def test_filter_by_category(client):
    response = client.get("/expenses?category=food")

    assert response.status_code == 200

    expenses = response.get_json()

    assert len(expenses) == 1
    assert expenses[0]["category"] == "food"



def test_filter_by_min_amount(client):
    response = client.get("/expenses?min_amount=100")

    assert response.status_code == 200

    expenses = response.get_json()

    assert len(expenses) == 1
    assert expenses[0]["amount"] >= 100



def test_filter_by_month(client):
    response = client.get("/expenses?month=2026-09")

    assert response.status_code == 200

    expenses = response.get_json()

    assert len(expenses) == 1



def test_filter_by_multiple_parameters(client):
    response = client.get("/expenses?category=food&min_amount=200&month=2026-09")

    assert response.status_code == 200

    expenses = response.get_json()

    assert len(expenses) == 1
    assert expenses[0]["name"] == "Test lunch"



def test_filter_invalid_category(client):
    response = client.get("/expenses?category=banana")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid Category"



def test_filter_invalid_min_amount(client):
    response = client.get("/expenses?min_amount=hello")

    assert response.status_code == 400



def test_filter_negative_min_amount(client):
    response = client.get("/expenses?min_amount=-100")

    assert response.status_code == 400



def test_filter_invalid_month(client):
    response = client.get("/expenses?month=2026-13")

    assert response.status_code == 400



def test_filter_invalid_month_format(client):
    response = client.get("/expenses?month=09")

    assert response.status_code == 400



def test_filter_with_no_matches(client):
    response = client.get("/expenses?category=shopping")

    assert response.status_code == 200
    assert response.get_json() == []


from app.extensions import db
from app.models import Expense


def test_sqlalchemy_can_read_expenses(client):
    with client.application.app_context():

        statement = db.select(Expense)

        result = db.session.execute(statement)

        expenses = result.scalars().all()

    assert len(expenses) >= 1
    assert expenses[0].name
    assert isinstance(expenses[0], Expense)



def test_sqlalchemy_can_create_expense(client):
    with client.application.app_context():

        expense = Expense(
            name="test lunch",
            amount=250,
            category="food",
            date="2026-09-15"
        )

        db.session.add(expense)

        db.session.commit()

        statement = db.select(Expense).where(
            Expense.name=="test lunch"
        )

        result = db.session.execute(statement)

        expense = result.scalar_one()

        assert expense.name == "test lunch"
        assert expense.amount == 250



def test_sqlalchemy_rollback(client):
    with client.application.app_context():
        expense = Expense(
            name="test dinner",
            amount=230,
            category="food",
            date="2026-09-16"
        )

        db.session.add(expense)

        db.session.flush()

        statement = db.select(Expense).where(
                    Expense.name =="test dinner"
                )
        
        result = db.session.execute(statement)

        expense = result.scalar_one_or_none()

        assert expense is not None
        assert expense.name == "test dinner"

        db.session.rollback()

        statement = db.select(Expense).where(
            Expense.name =="test dinner"
        )

        result = db.session.execute(statement)

        expense = result.scalar_one_or_none()

        assert expense is None



def test_sqlalchemy_can_update_expense(client):
    with client.application.app_context():

        expense = Expense(
            name="test breakfast",
            amount=300,
            category="food",
            date="2026-09-12"
        )

        db.session.add(expense)

        db.session.commit()

        statement = db.select(Expense).where(
            Expense.name=="test breakfast"
        )

        expense = db.session.execute(statement).scalar_one()

        expense.amount = 500

        db.session.commit()

        statement = db.select(Expense).where(
                    Expense.name=="test breakfast"
                )
        
        expense = db.session.execute(statement).scalar_one()

        assert expense.name == "test breakfast"
        assert expense.amount == 500

        

def test_sqlalchemy_can_delete_expense(client):
    with client.application.app_context():
        expense = Expense(
            name="test beer",
            amount=150,
            category="drink",
            date="2026-09-05"
        )

        db.session.add(expense)
        db.session.commit()

        statement = db.select(Expense).where(
            Expense.name=="test beer"
        )

        expense = db.session.execute(statement).scalar_one()

        assert expense is not None

        db.session.delete(expense)

        db.session.commit()

        statement = db.select(Expense).where(
            Expense.name=="test beer"
                )
        
        expense = db.session.execute(statement).scalar_one_or_none()

        assert expense is None