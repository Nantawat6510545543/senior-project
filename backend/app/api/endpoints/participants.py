from fastapi import APIRouter, HTTPException
from app.core.participants_loader import list_subjects, list_tasks

router = APIRouter()

@router.get("/")
def get_participants():
    return { "subjects": list_subjects() }

@router.get("/{subject_id}/tasks")
def get_subject_tasks(subject_id: str):
    tasks = list_tasks(subject_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {
        "subject": subject_id,
        "tasks": tasks
    }
