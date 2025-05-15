from pydantic import BaseModel

class EvaluateRequest(BaseModel):
    pass

class EvaluateResponse(BaseModel):
    message: str