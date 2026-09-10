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