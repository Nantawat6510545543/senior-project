from mne import Evoked

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


def prepare_evoked_topo_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    session_updated = session.model_copy(
        update={
            "filter": session.filter.model_copy(update={"combine_channels": False})
        }
    )

    evoked = executor.get_evoked(session_updated)

    if evoked is None:
        return None

    evoked_topo = prepare_channels(evoked, session.filter)
    return evoked_topo


def plot_evoked_topo(evoked_topo: Evoked, session: PipelineSession):
    """Plot evoked topomap at selected times; return finalized figure."""
    fig = evoked_topo.plot_topomap(times=session.topomap.resolved_times, show=False)

    header = FigureHeader(
        plot_name="Evoked Topo",
        subject_line=format_subject_label(session.task, session.epochs.stimulus),
        caption_line=str(session.topomap)
    )

    return finalize_figure(fig, header)
