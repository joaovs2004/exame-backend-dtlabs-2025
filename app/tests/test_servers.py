from fastapi.testclient import TestClient

from ..main import app
from app.tests.test_setup import data_for_test

client = TestClient(app)

def test_create_server_unauthorized(data_for_test):
    response = client.post("/servers", json={"name": "Dolly #1"})
    assert response.status_code == 401

def test_create_empty_server(data_for_test):
    response = client.post("/servers", headers={"Authorization": f"Bearer {data_for_test.acess_token}"})
    assert response.status_code == 422

def test_create_server(data_for_test):
    response = client.post("/servers", json={"name": "Dolly #1"}, headers={"Authorization": f"Bearer {data_for_test.acess_token}"})
    assert response.status_code == 200