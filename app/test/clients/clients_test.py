

def test_create_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "Charles Ramires",
            "email": "crramiress@gmail.com",
            "cpf": "02912787017",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charles Ramires"
    assert data["email"] == "crramiress@gmail.com"


def test_list_clients(client):
    response = client.get("/clients")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_client_by_id(client):
    create = client.post(
        "/clients",
        json={
            "name": "Charles Ramires",
            "email": "crramiress@gmail.com",
            "cpf": "02912787017",
        },
    )
    client_id = create.json()["id"]

    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == "Charles Ramires"


def test_update_client(client):
    create = client.post(
        "/clients",
        json={
            "name": "Charles Ramires",
            "email": "crramiress@gmail.com",
            "cpf": "02912787017",
        },
    )
    client_id = create.json()["id"]

    response = client.put(
        f"/clients/{client_id}",
        json={
            "name": "Charles Ramires Atualizado",
            "email": "crramiress@gmail.com",
            "cpf": "02912787017",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charles Ramires Atualizada"


def test_delete_client(client):
    create = client.post(
        "/clients",
        json={
            "name": "Charles Ramires",
            "email": "crramiress@gmail.com",
            "cpf": "02912787017",
        },
    )
    client_id = create.json()["id"]

    response = client.delete(f"/clients/{client_id}")
    assert response.status_code == 204

    get_response = client.get(f"/clients/{client_id}")
    assert get_response.status_code == 404
