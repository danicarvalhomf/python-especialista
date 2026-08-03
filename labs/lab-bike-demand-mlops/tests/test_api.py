from fastapi.testclient import TestClient

from src.api.main import app


VALID_PAYLOAD = {
    "year": 2012,
    "month": 8,
    "day": 7,
    "hour": 8,
    "weekday": 2,
    "season": 3,
    "holiday": 0,
    "working_day": 1,
    "weather_situation": 1,
    "temperature": 0.7,
    "apparent_temperature": 0.65,
    "humidity": 0.55,
    "wind_speed": 0.2,
}


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_prediction_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json=VALID_PAYLOAD,
        )

    assert response.status_code == 200

    response_data = response.json()

    assert "predicted_total_rentals" in response_data
    assert response_data["predicted_total_rentals"] >= 0


def test_prediction_rejects_invalid_hour():
    invalid_payload = {
        **VALID_PAYLOAD,
        "hour": 25,
    }

    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json=invalid_payload,
        )

    assert response.status_code == 422


def test_prediction_rejects_missing_field():
    invalid_payload = VALID_PAYLOAD.copy()
    invalid_payload.pop("temperature")

    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json=invalid_payload,
        )

    assert response.status_code == 422