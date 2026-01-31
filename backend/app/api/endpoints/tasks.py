from fastapi import APIRouter, Request
from schema.action import ActionRequest
from schema.adapters import to_pipeline_task_dto

router = APIRouter()


@router.get("/modes")
def modes(request: Request):
    return request.app.state.eeg.modes()


@router.get("/specs")
def specs(request: Request):
    return request.app.state.eeg.specs()


@router.post("/prepare")
def prepare(req: ActionRequest, request: Request):
    eeg = request.app.state.eeg
    task = to_pipeline_task_dto(req.task)
    return eeg.prepare(task, req.group, req.params)


@router.post("/execute")
def execute(req: ActionRequest, request: Request):
    eeg = request.app.state.eeg
    task = to_pipeline_task_dto(req.task)
    return eeg.execute(task, req.group, req.key, req.params)