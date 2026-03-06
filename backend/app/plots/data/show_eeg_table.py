from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession

def prepare_eeg_table_data(executor: EEGTaskExecutor, session: PipelineSession):
    """Return a small preview table for the requested component type."""
    table_info = session.table
    df_map = {
        'events': executor.get_event(),
        'channels': executor.channels,
        'electrodes': executor.electrodes
    }
    df = df_map.get(table_info.table_type)

    if df is None:
        return []

    return df.head(table_info.rows)
