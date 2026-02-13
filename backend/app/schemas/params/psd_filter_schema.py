from typing import Optional
from pydantic import BaseModel, Field, model_validator
from .epoch_filter_schema import EpochParams

from .base_filter_schema import FilterParams


class PSDParams(FilterParams):
    fmin: Optional[float] = Field(
        4, json_schema_extra={"ui": "number", "group": "psd", "placeholder": "4.0"}
    )
    fmax: Optional[float] = Field(
        30, json_schema_extra={"ui": "number", "group": "psd", "placeholder": "30.0"}
    )
    average: bool = Field(
        True, json_schema_extra={"ui": "checkbox", "group": "psd"}
    )
    dB: bool = Field(
        True, json_schema_extra={"ui": "checkbox", "group": "psd"}
    )
    spatial_colors: bool = Field(
        True, json_schema_extra={"ui": "checkbox", "group": "psd"}
    )


class EpochPSDParams(EpochParams, PSDParams):
    pass
