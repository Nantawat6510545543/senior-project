from pydantic import BaseModel

class CompareRequest(BaseModel):
    pass

class CompareResponse(BaseModel):
    message: str