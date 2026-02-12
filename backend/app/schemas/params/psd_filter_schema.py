from typing import Optional
from pydantic import BaseModel, Field, model_validator
from .epoch_filter_schema import EpochParams

from .base_filter_schema import FilterParams


class PSDParams(FilterParams):
    fmin: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "psd", "placeholder": "4.0"}
    )
    fmax: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "psd", "placeholder": "30.0"}
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

    # TODO

    # @model_validator(mode="after")
    # def apply_default_to_filter_value(self):
    #     if self.fmin is None:
    #         self.fmin = self.l_freq
    #     if self.fmax is None:
    #         self.fmax = self.h_freq
    #     return self


class EpochPSDParams(EpochParams, PSDParams):
    pass
