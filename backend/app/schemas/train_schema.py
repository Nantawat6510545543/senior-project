from pydantic import BaseModel, field_validator
# from typing import Optional

class TrainRequest(BaseModel):
    model_name: str
    dataset_name: str
    epochs: int
    kfolds: int

    @field_validator("model_name", "dataset_name")
    @classmethod
    def non_empty_string(cls, v, field):
        if not v.strip():
            raise ValueError(f"{field} must not be empty.")
        return v

    @field_validator("epochs")
    @classmethod
    def positive_epochs(cls, v):
        if v <= 0:
            raise ValueError("Epochs must be greater than 0.")
        return v

    @field_validator("kfolds")
    @classmethod
    def minimum_kfolds(cls, v):
        if v <= 1:
            raise ValueError("K-folds must be greater than 1.")
        return v


class TrainResponse(BaseModel):
    message: str