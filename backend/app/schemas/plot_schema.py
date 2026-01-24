from pydantic import BaseModel
from typing import Optional

class PlotRequest(BaseModel):
    l_freq: Optional[float] = None
    h_freq: Optional[float] = None
    notch: Optional[float] = None
    resample_fs: Optional[float] = None

    uv_min: Optional[float] = None
    uv_max: Optional[float] = None

    clean_flatline_sec: Optional[float] = None
    clean_hf_noise_sd_max: Optional[float] = None

    channels: str = "69-76,81-83,88,89"
    combine_channels: bool = False
    show_bad: bool = False
    asr_remove_only: bool = False
