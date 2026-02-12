from typing import Literal, Optional
from pydantic import Field, field_validator
from .base_filter_schema import FilterParams

Stimulus = Optional[Literal["open", "close"]]

class EpochParams(FilterParams):
    tmin: float = Field(
        -2.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epochs"}
    )
    tmax: float = Field(
        0.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epochs"}
    )
    stimulus: Stimulus = Field(
        default=None,
        json_schema_extra={
            "ui": "list",
            "group": "epochs",
            "options": ["None", "open", "close"],
        },
    )

    # Convert "none" to None
    @field_validator("stimulus", mode="before")
    @classmethod
    def normalize_none(cls, v):
        return None if v == "None" else v

    @property
    def epochs_key(self) -> dict[str, float]:
        return {**self.cleaning_key, "tmin": self.tmin, "tmax": self.tmax}

    @property
    def evoked_key(self) -> dict[str, object]:
        return {**self.epochs_key, "stimulus": self.stimulus}
