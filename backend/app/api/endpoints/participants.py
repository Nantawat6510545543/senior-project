from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.get("/")
def get_participants(request: Request):
    resolver = request.app.state.resolver
    return resolver.list_subjects()


@router.get("/{subject_id}/tasks/")
def get_subject_tasks(subject_id: str, request: Request):
    resolver = request.app.state.resolver
    tasks = resolver.list_tasks(subject_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {
        "subject": subject_id,
        "tasks": tasks,
    }

