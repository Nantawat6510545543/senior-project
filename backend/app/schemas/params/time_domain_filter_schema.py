from pydantic import BaseModel, Field


class TimeDomainParams(BaseModel):
    duration: float = Field(
        10.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "time"}
    )
    start: float = Field(
        0.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "time"}
    )
    n_channels: int = Field(
        10, json_schema_extra={"ui": "integer", "group": "time"}
    )
