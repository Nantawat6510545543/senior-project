from mne.io import Raw
from matplotlib.figure import Figure

from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession


def prepare_plot_sensors_data(executor, session: PipelineSession) -> Raw:
    raw = executor.get_filtered_raw(session.filter)

    if session.filter:
        raw.pick(session.filter.channels_list)

    return raw


def plot_sensors(raw: Raw) -> Figure:
    """Plot sensor montage with channel names; return Matplotlib figure list."""
    fig = raw.plot_sensors(show_names=True)
    return fig
