from pydantic import BaseModel
from typing import Optional


class SingleSubjectTask(BaseModel):
    task: Optional[str] = None
    subject: Optional[str] = None
    run: Optional[str] = None
