from pydantic import BaseModel

class EpochParams(BaseModel):
    tmin: float
    tmax: float
    event_id: dict