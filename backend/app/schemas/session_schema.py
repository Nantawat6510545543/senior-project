from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.task_schema import SingleSubjectTask, CohortTask
from .params.base_filter_schema import FilterParams
from .params.epoch_filter_schema import EpochParams
from .params.evoked_filter_schema import EvokedParams, EvokedTopoParams
from .params.psd_filter_schema import PSDParams
from .params.table_filter_schema import TableParams
from .params.subject_filter_schema import SubjectFilterParams
from .params.time_domain_filter_schema import TimeDomainParams


class PipelineSession(BaseModel):
    task: SingleSubjectTask | CohortTask = None
    subject_type: Literal["single", "cohort"] = "single"
    subject_filter: SubjectFilterParams = Field(default_factory=SubjectFilterParams)

    filter: FilterParams = Field(default_factory=FilterParams)
    epochs: EpochParams = Field(default_factory=EpochParams)
    time: TimeDomainParams = Field(default_factory=TimeDomainParams)
    psd: PSDParams = Field(default_factory=PSDParams)
    evoked: EvokedParams = Field(default_factory=EvokedParams)
    topomap: EvokedTopoParams = Field(default_factory=EvokedTopoParams)
    table: TableParams = Field(default_factory=TableParams)
