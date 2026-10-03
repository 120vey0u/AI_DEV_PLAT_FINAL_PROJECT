from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app
from app.database.session import get_db

app.dependency_overrides[get_db] = lambda: None
client = TestClient(app)


def test_analyze_endpoint_success():
    with patch("app.routers.sentiment.process_text") as mock_process:
        mock_process.return_value = {
            "id": 1, "text": "hello", "label": "positive", "score": 0.95
        }

        response = client.post("/api/v1/analyze", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json()["label"] == "positive"


def test_analyze_endpoint_rejects_invalid_input():
    response = client.post("/api/v1/analyze", json={"text": 12345})

    assert response.status_code == 422


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}