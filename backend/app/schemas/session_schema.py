from pydantic import BaseModel
from typing import Any, Optional

from .params.base_filter_schema import FilterParams
from .params.epoch_filter_schema import EpochParams
from .params.evoked_filter_schema import EvokedParams, EvokedTopoParams
from .params.psd_filter_schema import PSDParams
from .params.table_filter_schema import TableParams
from .params.time_domain_filter_schema import TimeDomainParams


class PipelineSession(BaseModel):
    # dataset selection TODO change to task
    input: dict[str, Any]

    filter: Optional[FilterParams] = None
    epochs: Optional[EpochParams] = None
    time: Optional[TimeDomainParams] = None
    psd: Optional[PSDParams] = None
    evoked: Optional[EvokedParams] = None
    topomap: Optional[EvokedTopoParams] = None
    table: Optional[TableParams] = None