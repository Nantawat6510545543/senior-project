from mne.io import Raw

from app.core.config import DATA_ROOT
from app.schemas.task_schema import SingleSubjectTask
from app.schemas.params import base_filter_schema
from app.pipeline.task_resolver import EEGTaskResolver

# TODO add input from UI
# Example call
# sst = SingleSubjectTask(
#     task="DespicableMe",
#     subject="sub-NDARAC904DMU",
# )

# Prepare data for plotting
def plot_sensors(sst: SingleSubjectTask, params: base_filter_schema):
    """Plot sensor montage with channel names; return Matplotlib figure list."""
    ee = EEGTaskResolver(DATA_ROOT)
    task_executor = ee.resolve_task(sst)
    raw = task_executor.get_raw()
    raw.pick(params.channels_list) # Pick only channel-specific data
    return plt_sensors(raw)

# Actual plotter
def plt_sensors(raw: Raw):
    """Plot sensor montage with channel names; return Matplotlib figure list."""
    fig = raw.plot_sensors(show_names=True)
    return fig