from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession

def prepare_evoked_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    evoked_dto = session.evoked
    evoked = executor.get_evoked(evoked_dto)

    if evoked is None:
        return None

    evoked = prepare_channels(evoked, evoked_dto)
    return evoked


def plot_evoked(evoked, session: PipelineSession):
    """Plot evoked time course; return finalized figure."""
    evoked_dto = session.evoked
    fig = evoked.plot(gfp=evoked_dto.gfp, spatial_colors=evoked_dto.spatial_colors, show=False)

    header = FigureHeader(
        plot_name="Evoked Plot",
        subject_line=format_subject_label(session.task, session.epochs.stimulus),
        caption_line=str(evoked_dto)
    )

    return finalize_figure(fig, header)