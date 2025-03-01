from fastapi.testclient import TestClient
import pytest

from ..main import app
from app.tests.test_setup import data_for_test
from datetime import datetime

client = TestClient(app)

def test_health(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": datetime.now().isoformat(),
            "temperature": 20.0
        }
    )
    response = client.get(f"/health/{data_for_test.server_ulid}", headers={"Authorization": f"Bearer {data_for_test.acess_token}"})
    assert response.status_code == 200

def test_health_all(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": datetime.now().isoformat(),
            "temperature": 24.0
        }
    )
    response = client.get("/health/all", headers={"Authorization": f"Bearer {data_for_test.acess_token}"})
    assert response.status_code == 200