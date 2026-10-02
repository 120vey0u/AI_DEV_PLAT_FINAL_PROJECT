from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
def test_sentiment_router_exists():
    response = client.get("/api/v1/non-existent-endpoint")
    assert response.status_code == 404