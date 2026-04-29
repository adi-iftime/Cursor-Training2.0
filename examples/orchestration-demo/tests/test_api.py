"""Task T1: API smoke tests."""
from fastapi.testclient import TestClient


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_workouts_crud(client: TestClient):
    r = client.get("/workouts")
    assert r.status_code == 200
    assert r.json() == []
    r = client.post(
        "/workouts",
        json={"title": "Test run", "duration_min": 20, "calories": 150},
    )
    assert r.status_code == 201
    wid = r.json()["id"]
    r = client.get(f"/workouts/{wid}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test run"


def test_metrics_summary(client: TestClient):
    client.post("/workouts", json={"title": "x", "duration_min": 10, "calories": 100})
    r = client.get("/metrics/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["total_workouts"] >= 1
