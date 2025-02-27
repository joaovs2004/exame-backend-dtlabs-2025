from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_empty_user():
    response = client.post("/auth/register")
    assert response.status_code == 422

def test_create_user_no_password():
    response = client.post(
        "/auth/register",
        json={"name": "teste"}
    )
    assert response.status_code == 422

def test_create_user_no_name():
    response = client.post(
        "/auth/register",
        json={"password": "123"}
    )
    assert response.status_code == 422

def test_create_user():
    response = client.post(
        "/auth/register",
        json={"name": "teste", "password": "123"}
    )
    assert response.status_code == 200