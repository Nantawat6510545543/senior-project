from typing import Optional
from pydantic import BaseModel, Field
from .epoch_filter_schema import EpochParams


class PSDParams(BaseModel):
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

    @property
    def psd_freqs(self):
        return {
            "fmin": self.fmin if self.fmin is not None else self.l_freq,
            "fmax": self.fmax if self.fmax is not None else self.h_freq,
        }


class EpochPSDParams(EpochParams, PSDParams):
    pass
