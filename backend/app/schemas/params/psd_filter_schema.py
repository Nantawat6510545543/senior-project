from typing import Optional
from pydantic import Field
from .base_filter_schema import FilterParams
from .epoch_filter_schema import EpochParams


class PSDParams(FilterParams):
    fmin: Optional[float] = Field(
        4.0, json_schema_extra={"ui": "number", "group": "psd"}
    )
    fmax: Optional[float] = Field(
        30.0, json_schema_extra={"ui": "number", "group": "psd"}
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

    @property
    def psd_freqs(self):
        return {
            "fmin": self.fmin if self.fmin is not None else self.l_freq,
            "fmax": self.fmax if self.fmax is not None else self.h_freq,
        }


class EpochPSDParams(EpochParams, PSDParams):
    pass
