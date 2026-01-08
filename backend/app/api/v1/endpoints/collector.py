from fastapi import APIRouter, Depends, HTTPException
from app.worker import run_collector_task
from typing import Any

router = APIRouter()

@router.post("/run")
def run_collector() -> Any:
    """
    Trigger collector manually.
    """
    task = run_collector_task.delay()
    return {"message": "Collector started", "task_id": str(task.id)}
