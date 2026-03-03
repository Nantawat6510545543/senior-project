from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/participants", tags=["participants"])

@router.get("/")
def get_participants(request: Request):
    participant_manager = request.app.state.participant_manager
    return participant_manager.list_subjects()


@router.get("/{subject_id}/tasks/")
def get_subject_tasks(subject_id: str, request: Request):
    participant_manager = request.app.state.participant_manager
    tasks = participant_manager.list_tasks(subject_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="Subject not found")

    return { "subject": subject_id, "tasks": tasks }
