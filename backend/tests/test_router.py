from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app
from app.database.session import get_db

app.dependency_overrides[get_db] = lambda: None
client = TestClient(app)


def test_analyze_endpoint_success():
    with patch("app.routers.sentiment.process_text") as mock_process:
        mock_process.return_value = {
            "id": 1,
            "input_text": "hello",
            "created_at": "2026-10-06T00:00:00Z",
            "analysis_data": {
                "overall": "Tích cực",
                "overall_comment": "Tốt",
                "highlightedText": [],
                "aspects": [],
            },
        }

        response = client.post("/api/v1/analyze", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json()["analysis_data"]["overall"] == "Tích cực"


def test_analyze_endpoint_rejects_invalid_input():
    response = client.post("/api/v1/analyze", json={"text": 12345})

    assert response.status_code == 422


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_history_list():
    with patch("app.routers.sentiment.crud.list_analyses") as mock_list:
        mock_list.return_value = []
        response = client.get("/api/v1/history")

    assert response.status_code == 200
    assert response.json() == []


def test_get_history_item_not_found():
    with patch("app.routers.sentiment.crud.get_analysis") as mock_get:
        mock_get.return_value = None
        response = client.get("/api/v1/history/999")

    assert response.status_code == 404


def test_delete_history_item_success():
    with patch("app.routers.sentiment.crud.delete_analysis") as mock_delete:
        mock_delete.return_value = True
        response = client.delete("/api/v1/history/1")

    assert response.status_code == 200
    assert "Đã xoá" in response.json()["message"]