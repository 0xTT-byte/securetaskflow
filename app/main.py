from fastapi import FastAPI
from app.worker import process_task 
import uuid

app = FastAPI(title="SecureTaskFlow")

@app.post("/task")
def submit_task(payload: dict):
    task_id = str(uuid.uuid4())
    process_task.apply_async(args=[task_id, payload], task_id=task_id)
    return {"task_id": task_id, "status": "queued"}

@app.get("/task/{task_id}/status") 
def get_status(task_id: str):
    result = process_task.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return {"task_queued": 0}   # Placeholder for Prometheus later 
