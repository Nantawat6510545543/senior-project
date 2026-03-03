from pydantic import BaseModel
from typing import Optional

class RangeFilter(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None


# TODO change to subject: str | list[str]
class SingleSubjectTask(BaseModel):
    task: Optional[str] = None
    subject: Optional[str] = None
    run: Optional[str] = None

# TODO CohortTask -> SingleSubjectFilter -> list[SingleSubjectTask]
# TODO deprecate this
class CohortTask(BaseModel):
    task: Optional[str] = None

    subject_limit: Optional[int] = None
    per_subject: bool = False

    sex: Optional[str] = None

    age: Optional[RangeFilter] = None
    ehq_total: Optional[RangeFilter] = None
    p_factor: Optional[RangeFilter] = None
    attention: Optional[RangeFilter] = None
    internalizing: Optional[RangeFilter] = None
    externalizing: Optional[RangeFilter] = None
    ccd_accuracy: Optional[RangeFilter] = None
    ccd_response_time: Optional[RangeFilter] = None
