import matplotlib.pyplot as plt
from mne import Evoked

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.grid_plot_helpers import draw_evoked_response
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.plots.plot_merger import merge_figures_vertical
from app.schemas.params.evoked_filter_schema import EvokedParams
from app.schemas.session_schema import PipelineSession

# TODO fix
def prepare_evoked_per_condition_plot_data(
    executor: EEGTaskExecutor,
    session: PipelineSession
) -> list[tuple[Evoked, EvokedParams]]:
    epochs, _ = executor.get_epochs(session)
    if epochs is None:
        return None

    prepared = []

    for condition in epochs.event_id:
        evoked_params = session.evoked.model_copy(update={"stimulus": condition})

        evoked = executor.get_evoked(session, evoked_params)
        if evoked is None:
            continue

        prepared_evoked = prepare_channels(evoked, session.filter)
        prepared.append((prepared_evoked, evoked_params))

    return prepared


def plot_evoked_per_condition(
        prepared_data: list[tuple[Evoked, EvokedParams]],
        session: PipelineSession
    ):
    if not prepared_data:
        return None

    figs = []

    for prepared_evoked, evoked_params in prepared_data:
        fig, ax = plt.subplots()

        draw_evoked_response(ax, prepared_evoked, evoked_params)

        x_lo = evoked_params.display_tmin or evoked_params.tmin
        x_hi = evoked_params.display_tmax or evoked_params.tmax

        ax.set_xlim(x_lo, x_hi)
        ax.set(xlabel="Time [s]", ylabel="µV")

        if prepared_evoked.nave:
            ax.text(
                1, 1, f"n={int(prepared_evoked.nave)}",
                transform=ax.transAxes,
                ha="right",
                va="bottom",
                fontsize=8,
                color="0.4",
            )

        header = FigureHeader(
            plot_name="Evoked per Condition",
            subject_line=format_subject_label(session.task, session.epochs.stimulus),
            caption_line=str(evoked_params),
        )

        figs.append(finalize_figure(fig, header))

    return merge_figures_vertical(figs)
