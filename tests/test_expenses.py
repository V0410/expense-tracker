def test_get_expenses(client):
    response = client.get("/expenses")

    assert response.status_code == 200


def test_get_nonexistent_expenses(client):
    response = client.get("/expenses/99999")

    assert response.status_code == 404


def test_get_expenses_with_invalid_id(client):
    response = client.get("/expenses/abc")

    assert response.status_code == 404