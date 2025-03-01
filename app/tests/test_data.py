from fastapi.testclient import TestClient
import pytest

from ..main import app
from app.tests.test_setup import data_for_test

client = TestClient(app)

def test_send_data_empty():
    response = client.post("/data")
    assert response.status_code == 422

def test_send_data_invalid_timestamp(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025/02/27",
            "temperature": 25.5
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "datetime_from_date_parsing",
                "loc": [
                    "body",
                    "timestamp"
                ],
                "msg": "Input should be a valid datetime or date, invalid date separator, expected `-`",
                "input": "2025/02/27",
                "ctx": {
                    "error": "invalid date separator, expected `-`"
                }
            }
        ]
    }

def test_send_data_only_temperature(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-02-27T17:53:38.083Z",
            "temperature": 25.5
        }
    )
    assert response.status_code == 200

def test_send_data_only_humidty(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-02-27T17:53:38.083Z",
            "humidity": 60.2
        }
    )
    assert response.status_code == 200

def test_send_data_only_voltage(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-02-27T17:53:38.083Z",
            "voltage": 220.0
        }
    )
    assert response.status_code == 200

def test_send_data_only_current(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-02-27T17:53:38.083Z",
            "current": 1.5
        }
    )
    assert response.status_code == 200

def test_send_data_all_fields(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-02-27T17:53:38.083Z",
            "temperature": 20.0,
            "humidity": 50.0,
            "voltage": 220.0,
            "current": 2.5
        }
    )
    assert response.status_code == 200

def test_send_data_all_fields_2(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-01-01T10:40:00.000Z",
            "temperature": 22.5,
            "humidity": 55.0,
            "voltage": 100.0,
            "current": 2.5
        }
    )
    assert response.status_code == 200

def test_send_data_all_fields_3(data_for_test):
    response = client.post(
        "/data",
        json={
            "server_ulid": data_for_test.server_ulid,
            "timestamp": "2025-01-15T10:40:00.000Z",
            "temperature": 12.0,
            "humidity": 65.0,
            "voltage": 110.0,
            "current": 3.0
        }
    )
    assert response.status_code == 200

def test_get_data_all(data_for_test):
    response = client.get("/data", headers={"Authorization": f"Bearer {data_for_test.acess_token}"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "temperature": 25.5
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "humidity": 60.2
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "voltage": 220.0
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "current": 1.5
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "temperature": 20.0
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "humidity": 50.0
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "voltage": 220.0
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "current": 2.5
        },
        {
            "timestamp": "2025-01-01T10:40:00",
            "temperature": 22.5,
        },
        {
            "timestamp": "2025-01-01T10:40:00",
            "humidity": 55.0,
        },
        {
            "timestamp": "2025-01-01T10:40:00",
            "voltage": 100.0,
        },
        {
            "timestamp": "2025-01-01T10:40:00",
            "current": 2.5
        },
        {
            "timestamp": "2025-01-15T10:40:00",
            "temperature": 12.0,
        },
        {
            "timestamp": "2025-01-15T10:40:00",
            "humidity": 65.0,
        },
        {
            "timestamp": "2025-01-15T10:40:00",
            "voltage": 110.0,
        },
        {
            "timestamp": "2025-01-15T10:40:00",
            "current": 3.0
        },
    ]

def test_get_temperature_data(data_for_test):
    response = client.get("/data", headers={"Authorization": f"Bearer {data_for_test.acess_token}"}, params={"sensor_type": "temperature"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "temperature": 25.5
        },
        {
            "timestamp": "2025-02-27T17:53:38.083000",
            "temperature": 20.0
        },
        {
            "timestamp": "2025-01-01T10:40:00",
            "temperature": 22.5,
        },
        {
            "timestamp": "2025-01-15T10:40:00",
            "temperature": 12.0,
        },
    ]

def test_get_data_unauthorized(data_for_test):
    response = client.get("/data")
    assert response.status_code == 401