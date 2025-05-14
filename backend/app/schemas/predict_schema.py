from pydantic import BaseModel

class PredictRequest(BaseModel):
    pass

class PredictResponse(BaseModel):
    message: str