from typing import Optional
from pydantic import BaseModel, Field

class TaskRequest(BaseModel):
    task: str
    subject: Optional[str] = None
    run: Optional[int] = None


class SingleSubjectTask(BaseModel):
    task: str
    subject: str
    run: Optional[str] = None


class CohortTask(BaseModel):
    task: str

    subject_limit: Optional[int] = None
    per_subject: bool = False

    sex: list[str] = Field(default_factory=lambda: ["M", "F"])

    age_min: Optional[float] = None
    age_max: Optional[float] = None

    ehq_total_min: Optional[float] = None
    ehq_total_max: Optional[float] = None

    p_factor_min: Optional[float] = None
    p_factor_max: Optional[float] = None