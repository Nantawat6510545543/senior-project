from mne.io import Raw
from matplotlib.figure import Figure

from app.core.config import DATA_ROOT
from app.schemas.session_schema import PipelineSession
from app.pipeline.task_resolver import EEGTaskResolver


# TODO this doesn't belong here, MOVE!
def build_raw_from_sst(session: PipelineSession) -> Raw:
    "Build raw data from SingleSubjectTask Schemas"
    resolver = EEGTaskResolver(DATA_ROOT)
    executor = resolver.resolve_task(session.task)

    raw = executor.get_raw()

    if session.filter:
        
        raw.pick(session.filter.channels_list)

    return raw

# Actual plotter
def plot_sensors(raw: Raw) -> Figure:
    """Plot sensor montage with channel names; return Matplotlib figure list."""
    fig = raw.plot_sensors(show_names=True)
    return fig