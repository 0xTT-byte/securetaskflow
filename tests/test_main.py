from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
client = TestClient(app)

@patch("app.main.process_task")     # swap the real Celery task for mock, only inside app.main
def test_submit_task_returns_task_id(mock_process):
    response = client.post("/task", json={"foo": "bar"})

    assert response.status_code == 200
    body = response.json()
    assert "task_id" in body        # endpoint must hand back an id 
    assert body["status"] == "queued"
    mock_process.apply_async.assert_called_once()       # prove it tried to equeue, without real Redis

@patch("app.main.process_task")
def test_get_status_returns_valid_status(mock_process):
    # force the chained call process_task.AsyncResult(id).status to return a known Celery state
    mock_process.AsyncResult.return_value.status = "PENDING"

    response = client.get("/task/some-fake-id/status")

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == "some-fake-id"
    assert body["status"] in {"PENDING", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

