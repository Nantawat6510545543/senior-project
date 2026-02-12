import re
from typing import Optional
from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    l_freq: float = Field(
        4.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter", "placeholder": "4.0"}
    )
    h_freq: float = Field(
        30.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter", "placeholder": "30.0"}
    )
    notch: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter", "placeholder": "60.0"}
    )
    resample_fs: float = Field(
        100.0, json_schema_extra={"ui": "number", "unit": "Hz", "group": "filter", "placeholder": "100.0"}
    )

    channels: str = Field(
        "69-76,81-83,88,89", 
        json_schema_extra={"ui": "text", "group": "channels", "placeholder": "69-76,81-83,88,89"},
    )
    combine_channels: Optional[bool] = Field(
        False, json_schema_extra={"ui": "checkbox", "group": "channels"}
    )

    uv_min: Optional[float] = Field(
        None, title="µV Min", json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "-100.0"}
    )
    uv_max: Optional[float] = Field(
        None, title="µV Max", json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "100.0"}
    )

    clean_flatline_sec: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "unit": "sec", "group": "cleaning", "placeholder": "5.0"}
    )
    clean_hf_noise_sd_max: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "4.0"}
    )
    clean_corr_min: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "0.8"}
    )
    clean_asr_max_std: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "20.0"}
    )

    clean_power_min_sd: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "-100.0"}
    )
    clean_power_max_sd: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "group": "cleaning", "placeholder": "7.0"}
    )
    clean_max_outbound_pct: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "unit": "%", "group": "cleaning", "placeholder": "25.0"}
    )
    clean_window_sec: Optional[float] = Field(
        None, json_schema_extra={"ui": "number", "unit": "sec", "group": "cleaning", "placeholder": "0.5"}
    )

    clean_asr_remove_only: Optional[bool] = Field(
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
