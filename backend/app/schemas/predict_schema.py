from pydantic import BaseModel, field_validator

class PredictRequest(BaseModel):
    model_name: str

    @field_validator("model_name")
    @classmethod
    def non_empty_string(cls, v, field):
        if not v.strip():
            raise ValueError(f"{field} must not be empty.")
        return v
    
class PredictResponse(BaseModel):
    message: str