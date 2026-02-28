from typing import Optional
from pydantic import BaseModel, Field


class RangeFilter(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None


class SingleSubjectTask(BaseModel):
    task: str
    subject: str
    run: Optional[str] = None


class CohortTask(BaseModel):
    task: str

    subject_limit: Optional[int] = None
    per_subject: bool = False

    sex: list[str] = Field(default_factory=lambda: ["None", "M", "F"])

    age: Optional[RangeFilter]
    ehq_total: Optional[RangeFilter]
    p_factor: Optional[RangeFilter]
    attention: Optional[RangeFilter]
    internalizing: Optional[RangeFilter]
    externalizing: Optional[RangeFilter]
    ccd_accuracy: Optional[RangeFilter]
    ccd_response_time: Optional[RangeFilter]


class SubjectFilterDTO(BaseModel):
    task: Optional[str]
    subject_limit: Optional[int]
    per_subject: Optional[bool]
    sex: Optional[str]

    age: Optional[RangeFilter]
    ehq_total: Optional[RangeFilter]
    p_factor: Optional[RangeFilter]
    attention: Optional[RangeFilter]
    internalizing: Optional[RangeFilter]
    externalizing: Optional[RangeFilter]
    ccd_accuracy: Optional[RangeFilter]
    ccd_response_time: Optional[RangeFilter]
