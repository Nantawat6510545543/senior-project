import matplotlib.pyplot as plt

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.grid_plot_helpers import draw_evoked_response
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
        fig, ax = plt.subplots(1, 1)

        draw_evoked_response(ax, prepared_evoked, conditioned_evoked_dto)
        
        if getattr(conditioned_evoked_dto, "display_tmin", None):
            x_lo = conditioned_evoked_dto.display_tmin
        else:
            x_lo = conditioned_evoked_dto.tmin

        if getattr(conditioned_evoked_dto, "display_tmax", None):    
            x_hi = conditioned_evoked_dto.display_tmax
        else:
            x_hi = conditioned_evoked_dto.tmax

        ax.set_xlim(x_lo, x_hi)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("µV")

        nave = getattr(prepared_evoked, "nave", None)
        if nave is not None:
            ax.text(
                1, 1, f"n={int(nave)}", transform=ax.transAxes, 
                ha="right", va="bottom", fontsize=8, color="0.4",
            )

        header = FigureHeader(
            plot_name="Evoked per Condition",
            subject_line=format_subject_label(session.task, conditioned_evoked_dto.stimulus),
            caption_line=str(conditioned_evoked_dto),
        )

        figs.append(finalize_figure(fig, header))

    return merge_figures_vertical(figs)
