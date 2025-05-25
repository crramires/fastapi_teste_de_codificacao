from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_client():
    response = client.get("/clients")
    assert response.status_code == 200

    assert response.json() == [
        {
            "cpf": "02912787017",
            "email": "crramiress@gmail.com",
            "id": 1,
            "name": "Charles Ramires",
        }
    ]


def test_create_client():
    new_client = {
        "name": "Maria Ramires",
        "email": "cr@gmail.com",
        "cpf": "123456789",
    }
    response = client.post("/clients", json=new_client)
    assert response.status_code == 201
