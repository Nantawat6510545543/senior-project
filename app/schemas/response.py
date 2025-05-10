from pydantic import BaseModel

class TrainResponse(BaseModel):
    status: str
    accuracy: float

class ClassifyResponse(BaseModel):
    label: str
    confidence: float
