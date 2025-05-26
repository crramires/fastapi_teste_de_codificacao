import pytest
from fastapi.testclient import TestClient

from app.models.product_model import Product


@pytest.fixture
def test_product(db_session):
    product = Product(
        name="Produto Teste",
        description="Descrição do produto teste",
        barcode="1234567890",
        category="Categoria Teste",
        section="Seção Teste",
        sale_value=100.0,
        initial_stock=20,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    yield product
    db_session.delete(product)
    db_session.commit()


def test_create_product(client: TestClient, token_auth_headers):
    response = client.post(
        "/products",
        json={
            "name": "Novo Produto",
            "description": "Descrição",
            "barcode": "9999999999",
            "category": "Categoria X",
            "section": "Seção Y",
            "sale_value": 60.0,
            "initial_stock": 100,
        },
        headers=token_auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Novo Produto"
    assert data["barcode"] == "9999999999"


def test_get_products(client: TestClient, test_product, token_auth_headers):
    response = client.get("/products", headers=token_auth_headers)
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)


def test_get_product_by_id(
    client: TestClient, test_product, token_auth_headers
):
    response = client.get(
        f"/products/{test_product.id}", headers=token_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product.id
    assert data["name"] == test_product.name


def test_get_product_by_id_not_found(client: TestClient, token_auth_headers):
    response = client.get("/products/9999", headers=token_auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_update_product(client: TestClient, test_product, token_auth_headers):
    response = client.put(
        f"/products/{test_product.id}",
        json={
            "name": "Produto Atualizado",
            "description": test_product.description,
            "barcode": test_product.barcode,
            "category": test_product.category,
            "section": test_product.section,
            "sale_value": test_product.sale_value,
            "initial_stock": test_product.initial_stock,
        },
        headers=token_auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Produto Atualizado"


def test_update_product_not_found(client: TestClient, token_auth_headers):
    response = client.put(
        "/products/9999",
        json={
            "name": "Produto Inexistente",
            "description": "Teste",
            "barcode": "0000000000",
            "category": "Cat",
            "section": "Sec",
            "sale_value": 20.0,
            "initial_stock": 10,
        },
        headers=token_auth_headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found."


def test_delete_product(client: TestClient, test_product, token_auth_headers):
    response = client.delete(
        f"/products/{test_product.id}", headers=token_auth_headers
    )
    assert response.status_code == 204

    get_response = client.get(
        f"/products/{test_product.id}", headers=token_auth_headers
    )
    assert get_response.status_code == 404


def test_delete_product_not_found(client: TestClient, token_auth_headers):
    response = client.delete("/products/9999", headers=token_auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found"
