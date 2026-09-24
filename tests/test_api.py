from fastapi.testclient import TestClient

from src.app import main
from src.app.departments import Department

client = TestClient(main.app)


def test_route(monkeypatch) -> None:
    monkeypatch.setattr(main, "route_message_agent", lambda email, message: Department.IT)

    response = client.post(
        "/api/v1/route-message",
        json={"email": "jan.kowalski@firma.pl", "message": "VPN rozłącza mnie"},
    )

    assert response.status_code == 200
    assert response.json() == {"department": "IT"}


def test_bad_request() -> None:
    response = client.post(
        "/api/v1/route-message",
        json={"email": "not-an-email", "message": "Hi"},
    )

    assert response.status_code == 422


def test_model_error(monkeypatch) -> None:
    def fail(email, message):
        raise main.ModelRuntimeError("model unavailable")

    monkeypatch.setattr(main, "route_message_agent", fail)

    response = client.post(
        "/api/v1/route-message",
        json={"email": "jan.kowalski@firma.pl", "message": "VPN rozłącza mnie"},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Message classification service is unavailable"}
