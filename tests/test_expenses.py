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
    