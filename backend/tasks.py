from uuid import uuid4
from datetime import datetime
from typing import Dict, Optional

tasks: Dict[str, dict] = {}

def create_task(original_filename: str, brightness: float, contrast: float, saturation: float):
    task_id = str(uuid4())
    tasks[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "original_filename": original_filename,
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
        "result_bytes": None,
        "result_path": None,
        "created_at": datetime.utcnow(),
        "error": None
    }
    return task_id

def get_task(task_id: str):
    return tasks.get(task_id)

def update_task(task_id: str, **kwargs):
    if task_id in tasks:
        tasks[task_id].update(kwargs)

def delete_task(task_id: str):
    if task_id in tasks:
        del tasks[task_id]