from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_send_data_empty():
    response = client.post("/data")
    assert response.status_code == 422

def test_send_data_invalid_timestamp():
    response = client.post(
        "/data",
        json={
            "server_ulid": "01JN48HKVJTPJ1NW58MTNAA2JG",
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

def test_send_data_only_temperature():
    response = client.post(
        "/data",
        json={
            "server_ulid": "01JN48HKVJTPJ1NW58MTNAA2JG",
            "timestamp": "2025-02-27T17:53:38.083Z",
            "temperature": 25.5
        }
    )
    assert response.status_code == 200

def test_send_data_only_humidty():
    response = client.post(
        "/data",
        json={
            "server_ulid": "01JN48HKVJTPJ1NW58MTNAA2JG",
            "timestamp": "2025-02-27T17:53:38.083Z",
            "humidity": 60.2
        }
    )
    assert response.status_code == 200

def test_send_data_only_voltage():
    response = client.post(
        "/data",
        json={
            "server_ulid": "01JN48HKVJTPJ1NW58MTNAA2JG",
            "timestamp": "2025-02-27T17:53:38.083Z",
            "voltage": 220.0
        }
    )
    assert response.status_code == 200

def test_send_data_only_current():
    response = client.post(
        "/data",
        json={
            "server_ulid": "01JN48HKVJTPJ1NW58MTNAA2JG",
            "timestamp": "2025-02-27T17:53:38.083Z",
            "current": 1.5
        }
    )
    assert response.status_code == 200
