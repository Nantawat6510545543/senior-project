from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class EpochParams(BaseModel):
    tmin: float = Field(
        -2.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epochs"}
    )
    tmax: float = Field(
        0.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epochs"}
    )

    stimulus: Optional[Literal["None", "open", "close"]] = Field(
        "None", 
        validate_default=True,
        json_schema_extra={
            "ui": "list",
            "group": "epochs",
            "options": ["None", "open", "close"]
        },
    )

    # Convert "none" to None
    @field_validator("stimulus", mode="before")
    @classmethod
    def normalize_none(cls, v):
        return None if v == "None" else v
