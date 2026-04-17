from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from task_tracker.main import app


@pytest.fixture
def api_client(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Isolate SQLite to a temp file so tests never touch task_tracker/tasks.db."""
    db_file = tmp_path / "test_tasks.db"
    monkeypatch.setattr("task_tracker.db.DB_PATH", db_file)

    with TestClient(app) as client:
        yield client


def test_post_tasks_creates_task_201(api_client: TestClient):
    response = api_client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["done"] is False
    assert "id" in data
    assert "created_at" in data


def test_get_tasks_returns_list(api_client: TestClient):
    api_client.post("/tasks", json={"title": "A"})
    api_client.post("/tasks", json={"title": "B"})

    response = api_client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 2
    assert {t["title"] for t in tasks} == {"A", "B"}


def test_get_task_by_id_404_for_bad_id(api_client: TestClient):
    response = api_client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_patch_task_updates_done(api_client: TestClient):
    create = api_client.post("/tasks", json={"title": "Finish patch"})
    assert create.status_code == 201
    task_id = create.json()["id"]

    patch = api_client.patch(f"/tasks/{task_id}", json={"done": True})
    assert patch.status_code == 200
    body = patch.json()
    assert body["done"] is True
    assert body["title"] == "Finish patch"

    fetched = api_client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["done"] is True
