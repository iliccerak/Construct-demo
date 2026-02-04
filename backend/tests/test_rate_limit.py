import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from main import create_app


def test_rate_limit_blocks_after_threshold(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")
    monkeypatch.setenv("RATE_LIMIT_MAX_REQUESTS", "2")
    monkeypatch.setenv("AUTH_RATE_LIMIT_MAX_REQUESTS", "1")

    app = create_app()
    client = TestClient(app)

    response1 = client.get("/api/v1/users/me")
    assert response1.status_code in {401, 403}

    response2 = client.get("/api/v1/users/me")
    assert response2.status_code in {401, 403, 429}

    response3 = client.get("/api/v1/users/me")
    assert response3.status_code == 429
