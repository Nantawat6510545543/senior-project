from typing import Optional
from pydantic import Field
from .base_filter_schema import FilterParams


class EpochParams(FilterParams):
    tmin: float = Field(
        -2.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epoch"}
    )
    tmax: float = Field(
        0.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "epoch"}
    )
    stimulus: list[Optional[str]] = Field(
        "None", json_schema_extra={"ui": "list", "group": "epoch", "options": ["None"]}
    )

    @property
    def epochs_key(self) -> dict[str, float]:
        return {**self.cleaning_key, "tmin": self.tmin, "tmax": self.tmax}

    @property
    def evoked_key(self) -> dict[str, object]:
        return {**self.epochs_key, "stimulus": self.stimulus}
