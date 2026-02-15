from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.plots.plot_merger import merge_figures_vertical
from app.schemas.session_schema import PipelineSession


def prepare_evoked_per_condition_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_dto = session.epochs
    evoked_dto = session.evoked

    epochs, _ = executor.get_epochs(epochs_dto)
    if epochs is None:
        return None

    prepared = []

    for condition in epochs.event_id:
        conditioned_evoked_dto = evoked_dto.model_copy(update={"stimulus": condition})
        evoked = executor.get_evoked(conditioned_evoked_dto)
        if evoked is None:
            continue

        prepared_evoked = prepare_channels(evoked, conditioned_evoked_dto)
        prepared.append((prepared_evoked, conditioned_evoked_dto))

    return prepared


def plot_evoked_per_condition(prepared_data, session: PipelineSession):
    if not prepared_data:
        return None

    figs = []

    for prepared_evoked, conditioned_evoked_dto in prepared_data:
        fig = prepared_evoked.plot(
            gfp=conditioned_evoked_dto.gfp,
            spatial_colors=conditioned_evoked_dto.spatial_colors,
            show=False
        )

        header = FigureHeader(
            plot_name="Evoked per Condition",
            subject_line=format_subject_label(session.task, conditioned_evoked_dto.stimulus),
            caption_line=str(conditioned_evoked_dto)
        )

        figs.append(finalize_figure(fig, header))

    return merge_figures_vertical(figs)
