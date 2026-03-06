from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


def prepare_epochs_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_dto = session.epochs
    epochs, _ = executor.get_epochs(epochs_dto)

    if epochs is None:
        return None

    if epochs_dto.stimulus and epochs_dto.stimulus in epochs.event_id:
        epochs = epochs[epochs_dto.stimulus]

    epochs = prepare_channels(epochs, epochs_dto)
    return epochs


def plot_epochs(epochs, session: PipelineSession):
    """Plot epochs with channel selection; return finalized Matplotlib figure."""
    fig = epochs.plot(events=False, show=False)

    header = FigureHeader(
        plot_name="Epoch Plot",
        subject_line=format_subject_label(session.task, session.epochs.stimulus),
        caption_line=str(session.epochs)
    )

    final_fig = finalize_figure(fig, header)
    return final_fig
