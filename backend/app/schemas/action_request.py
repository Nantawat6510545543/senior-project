from pydantic import BaseModel
from typing import Dict, Any
from .task import TaskRef


class ActionRequest(BaseModel):
    task: TaskRef
    group: str
    key: str
    params: Dict[str, Any]
