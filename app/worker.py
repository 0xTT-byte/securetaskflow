from celery import Celery
import os, time 

app = Celery(
        "tasks", 
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
        )

@app.task
def process_task(task_id: str, payload: dict):
    time.sleep(1)   # simulate work 
    return {"task_id": task_id, "result": "done"}

