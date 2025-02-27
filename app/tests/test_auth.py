from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_no_fields_user():
    response = client.post("/auth/register")
    assert response.status_code == 422

def test_create_empty_user():
    response = client.post(
        "/auth/register",
        json={"name": "", "password": ""}
    )
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
    assert response.json() == {"message": "User created"}

def test_user_login_no_password():
    response = client.post(
        "/auth/login",
        data={"username": "teste"}

    )
    assert response.status_code == 422

def test_user_uncreated_login():
    response = client.post(
        "/auth/login",
        data={"username": "usernotcreated", "password": "123"}

    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_user_login():
    response = client.post(
        "/auth/login",
        data={"username": "teste", "password": "123"}

    )
    assert response.status_code == 200