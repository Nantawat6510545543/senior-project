from mne.io import Raw
from matplotlib.figure import Figure

from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession


# TODO this doesn't belong here, MOVE!
def build_raw_from_sst(executor: EEGTaskExecutor, session: PipelineSession) -> Raw:
    "Build raw data from SingleSubjectTask Schemas"
    raw = executor.get_raw()

    if session.filter:
        raw.pick(session.filter.channels_list)

    return raw

# Actual plotter
def plot_sensors(raw: Raw) -> Figure:
    """Plot sensor montage with channel names; return Matplotlib figure list."""
    fig = raw.plot_sensors(show_names=True)
    return fig
