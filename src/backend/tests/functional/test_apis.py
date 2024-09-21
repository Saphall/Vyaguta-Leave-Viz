from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"success": "Vyaguta Leave Info"}
