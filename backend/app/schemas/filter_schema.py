"""
Filtering, epoching, PSD, evoked, and table parameter schemas.
"""

from __future__ import annotations

import re
from typing import Optional, Union

from pydantic import BaseModel, computed_field


# -------------------------
# Filtering
# -------------------------

class FilterParams(BaseModel):
    l_freq: float = 4.0
    h_freq: float = 30.0
    notch: Optional[float] = 60.0
    resample_fs: float = 100.0

    channels: str = "69-76,81-83,88,89"

    uv_min: Optional[float] = -100.0
    uv_max: Optional[float] = 100.0

    clean_flatline_sec: Optional[float] = 5.0
    clean_hf_noise_sd_max: Optional[float] = 4.0
    clean_corr_min: Optional[float] = 0.8
    clean_asr_max_std: Optional[float] = 20.0
    clean_power_min_sd: Optional[float] = -100.0
    clean_power_max_sd: Optional[float] = 7.0
    clean_max_outbound_pct: Optional[float] = 25.0
    clean_window_sec: Optional[float] = 0.5

    # ---- cache helpers ----

    @computed_field
    def filter_key(self) -> dict[str, float]:
        return {
            "l_freq": self.l_freq,
            "h_freq": self.h_freq,
            "notch": self.notch,
            "resample_fs": self.resample_fs,
        }

    @computed_field
    def cleaning_key(self) -> dict[str, float]:
        key = dict(self.filter_key)
        for name in (
            "clean_flatline_sec",
            "clean_hf_noise_sd_max",
            "clean_corr_min",
            "clean_asr_max_std",
            "clean_power_min_sd",
            "clean_power_max_sd",
            "clean_max_outbound_pct",
            "clean_window_sec",
        ):
            val = getattr(self, name)
            if val is not None:
                key[name] = val
        return key

    # ---- channels ----

    @computed_field
    def channels_list(self) -> list[str]:
        if not self.channels:
            return [f"E{i}" for i in range(1, 129)]

        tokens = re.split(r"[,\s]+", self.channels)
        out: list[str] = []

        for t in tokens:
            if "-" in t:
                a, b = t.split("-")
                for i in range(int(a), int(b) + 1):
                    out.append(f"E{i}")
            else:
                out.append(f"E{int(t)}")

        return sorted(set(out))


# -------------------------
# Epoching
# -------------------------

class EpochParams(FilterParams):
    tmin: float = -2.0
    tmax: float = 0.0
    stimulus: Optional[str] = None

    @computed_field
    def epochs_key(self) -> Dict[str, Union[float, str]]:
        return {
            **self.cleaning_key,
            "tmin": self.tmin,
            "tmax": self.tmax,
        }


# -------------------------
# PSD
# -------------------------

class PSDParams(FilterParams):
    fmin: Optional[float] = None
    fmax: Optional[float] = None
    average: bool = True
    dB: bool = True

    def model_post_init(self, _):
        if self.fmin is None:
            self.fmin = self.l_freq
        if self.fmax is None:
            self.fmax = self.h_freq


# -------------------------
# Evoked
# -------------------------

class EvokedParams(EpochParams):
    spatial_colors: bool = True
    gfp: Union[bool, str] = False
    average_line: bool = True


class EvokedTopoParams(EpochParams):
    times: str = "auto"

    @computed_field
    def resolved_times(self):
        if self.times in ("auto", "peak"):
            return self.times

        nums = [
            float(x)
            for x in re.findall(r"[-+]?\d*\.?\d+", self.times)
        ]
        return [t for t in nums if self.tmin <= t <= self.tmax] or "auto"


# -------------------------
# Misc
# -------------------------

class TimeDomainParams(FilterParams):
    duration: float = 10.0
    start: float = 0.0
    n_channels: int = 10


class TableInfoParams(FilterParams):
    table_type: str = "events"
    rows: int = 10
