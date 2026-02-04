import re
from typing import Optional
from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    l_freq: float = Field(
        4.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter"}
    )
    h_freq: float = Field(
        30.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter"}
    )
    notch: Optional[float] = Field(
        60.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter"}
    )
    resample_fs: float = Field(
        100.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter"}
    )

    channels: str = Field(
        "69-76,81-83,88,89",
        json_schema_extra={"ui": "text", "group": "channels"},
    )
    combine_channels: bool = Field(
        False, json_schema_extra={"ui": "checkbox", "group": "channels"}
    )

    uv_min: Optional[float] = Field(
        -100.0, title="µV Min", json_schema_extra={"ui": "number", "group": "cleaning"}
    )
    uv_max: Optional[float] = Field(
        100.0, title="µV Max", json_schema_extra={"ui": "number", "group": "cleaning"}
    )

    clean_flatline_sec: Optional[float] = Field(
        5.0, json_schema_extra={"ui": "number", "unit": "sec", "group": "cleaning"}
    )
    clean_hf_noise_sd_max: Optional[float] = Field(
        4.0, json_schema_extra={"ui": "number", "group": "cleaning"}
    )
    clean_corr_min: Optional[float] = Field(
        0.8, json_schema_extra={"ui": "number", "group": "cleaning"}
    )
    clean_asr_max_std: Optional[float] = Field(
        20.0, json_schema_extra={"ui": "number", "group": "cleaning"}
    )

    clean_power_min_sd: Optional[float] = Field(
        -100.0, json_schema_extra={"ui": "number", "group": "cleaning"}
    )
    clean_power_max_sd: Optional[float] = Field(
        7.0, json_schema_extra={"ui": "number", "group": "cleaning"}
    )
    clean_max_outbound_pct: Optional[float] = Field(
        25.0, json_schema_extra={"ui": "number", "unit": "%", "group": "cleaning"}
    )
    clean_window_sec: Optional[float] = Field(
        0.5, json_schema_extra={"ui": "number", "unit": "sec", "group": "cleaning"}
    )

    asr_remove_only: bool = Field(
        False, json_schema_extra={"ui": "checkbox", "group": "cleaning"}
    )

    # combine_channels: bool = False
    # show_bad: bool = False

    class Config:
        extra = "forbid"

    @property
    def filter_key(self) -> dict[str, float | None]:
        return {
            "l_freq": self.l_freq,
            "h_freq": self.h_freq,
            "notch": self.notch,
            "resample_fs": self.resample_fs,
        }

    @property
    def cleaning_key(self) -> dict[str, float | bool]:
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

        if self.clean_asr_remove_only:
            key["clean_asr_remove_only"] = True

        return key

    @property
    def channels_list(self) -> list[str]:
        if not self.channels.strip():
            return [f"E{i}" for i in range(1, 129)]

        out, seen = [], set()
        for token in re.split(r"[,\s]+", self.channels):
            if "-" in token:
                a, b = token.split("-", 1)
                for i in range(min(int(a), int(b)), max(int(a), int(b)) + 1):
                    name = f"E{i}"
                    if name not in seen:
                        seen.add(name)
                        out.append(name)
            else:
                name = f"E{int(token)}"
                if name not in seen:
                    seen.add(name)
                    out.append(name)

        return out
