from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_empty_server():
    response = client.post("/servers")
    assert response.status_code == 422

def test_create_server():
    response = client.post("/servers", json={"name": "Dolly #1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Server created"}