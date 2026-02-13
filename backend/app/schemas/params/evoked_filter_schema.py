import re

from pydantic import BaseModel, Field
from typing import Literal, Optional

from .epoch_filter_schema import EpochParams


class EvokedParams(EpochParams):
    spatial_colors: bool = Field(
        True, json_schema_extra={"ui": "checkbox", "group": "evoked"}
    )
    gfp: Optional[Literal[False, True, "only"]] = Field(
        False,
        json_schema_extra={
            "ui": "list",
            "group": "evoked",
            "options": [False, True, "only"],
        },
    )
    average_line: bool = Field(
        True, json_schema_extra={"ui": "checkbox", "group": "evoked"}
    )
    scale_mode: Optional[Literal["per-plot", "uniform-grid"]] = Field(
        "per-plot",
        json_schema_extra={
            "ui": "list",
            "group": "evoked",
            "options": ["per-plot", "uniform-grid"],
        },
    )


class EvokedTopoParams(EpochParams):
    times: str = Field(
        "auto", json_schema_extra={"ui": "text", "group": "topomap"}
    )

    @property
    def resolved_times(self):
        s = self.times.lower().strip()
        if s in {"auto", "peak"}:
            return s

        values = [
            float(x) for x in re.findall(r"[-+]?\d*\.?\d+", self.times)
        ]
        values = [t for t in values if self.tmin <= t <= self.tmax]
        return values or "auto"


class EvokedJointParams(EvokedParams, EvokedTopoParams):
    pass
