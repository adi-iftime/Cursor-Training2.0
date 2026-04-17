from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_get_users_status_and_shape():
    response = client.get("/users")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2
    for row in body:
        assert set(row.keys()) >= {"id", "name", "email"}
