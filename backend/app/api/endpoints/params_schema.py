from fastapi import APIRouter

from app.schemas.params.base_filter_schema import FilterParams
from app.schemas.params.epoch_filter_schema import EpochParams
from app.schemas.params.psd_filter_schema import PSDParams
from app.schemas.params.evoked_filter_schema import EvokedJointParams, EvokedParams, EvokedTopoParams
from app.schemas.params.table_filter_schema import TableParams
from app.schemas.params.time_domain_filter_schema import TimeDomainParams


router = APIRouter(prefix="/schemas", tags=["schemas"])

@router.get("/filter")
def filter_schema():
    return FilterParams.model_json_schema()

@router.get("/epochs")
def epochs_schema():
    return EpochParams.model_json_schema()

@router.get("/psd")
def psd_schema():
    return PSDParams.model_json_schema()

@router.get("/evoked")
def evoked_schema():
    return EvokedParams.model_json_schema()

@router.get("/topomap")
def topomap_schema():
    return EvokedTopoParams.model_json_schema()

@router.get("/time")
def time_domain_schema():
    return TimeDomainParams.model_json_schema()

@router.get("/tables")
def tables_schema():
    return TableParams.model_json_schema()
