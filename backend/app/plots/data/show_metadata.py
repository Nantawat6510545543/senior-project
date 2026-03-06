from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession

def prepare_metadata_data(executor: EEGTaskExecutor, session: PipelineSession):
    """Return task metadata as a dictionary-like mapping."""
    meta = executor.metadata

    rows = []
    for key, value in meta.items():
        rows.append({
            "field": key,
            "value": value
        })

    return rows
