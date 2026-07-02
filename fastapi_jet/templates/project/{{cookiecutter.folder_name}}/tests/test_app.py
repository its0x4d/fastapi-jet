from fastapi.testclient import TestClient

from base.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_core_app_route() -> None:
    response = client.get("/core/")
    assert response.status_code == 200
    assert "message" in response.json()
