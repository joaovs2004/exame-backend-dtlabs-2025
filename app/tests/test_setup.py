from fastapi.testclient import TestClient
import pytest

from ..main import app

client = TestClient(app)

class DataForTest():
    def __init__(self, acess_token, server_ulid):
        self.acess_token = acess_token
        self.server_ulid = server_ulid

@pytest.fixture(scope="module")
def data_for_test():
    response = client.post(
        "/auth/login",
        data={"username": "teste", "password": "123"}
    )
    assert response.status_code == 200
    acess_token = response.json()["access_token"]

    server_ulid = client.post("/servers", json={"name": "Test server"}, headers={"Authorization": f"Bearer {acess_token}"})
    assert server_ulid.status_code == 200
    server_ulid = server_ulid.json()["server_ulid"]

    return DataForTest(acess_token=acess_token, server_ulid=server_ulid)
