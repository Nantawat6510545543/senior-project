import matplotlib.pyplot as plt
from mne import Evoked

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.grid_plot_helpers import draw_evoked_response
from app.plots.figure_header import FigureHeader, format_caption_label, format_subject_label
from app.plots.plot_finalizer import finalize_figure
from app.plots.plot_merger import merge_figures_vertical
from app.schemas.session_schema import PipelineSession


def prepare_evoked_per_condition_plot_data(
    executor: EEGTaskExecutor,
    session: PipelineSession
) -> list[tuple[Evoked, str]] | None:
    epochs, _ = executor.get_epochs(session)
    if epochs is None:
        return None

    prepared = []

    for condition in epochs.event_id.keys():
        epochs_params = session.epochs.model_copy(update={"stimulus": [condition]})
        session_updated = session.model_copy(update={"epochs": epochs_params})

        evoked = executor.get_evoked(session_updated)
        if evoked is None:
            continue

        prepared_evoked = prepare_channels(evoked, session.filter)
        prepared.append((prepared_evoked, condition))

    return prepared


def plot_evoked_per_condition(
        prepared_data: list[tuple[Evoked, str]],
        session: PipelineSession
    ):
    if not prepared_data:
        return None

    figs = []

    for prepared_evoked, condition in prepared_data:
        fig, ax = plt.subplots()

        draw_evoked_response(ax, prepared_evoked, session.evoked)

        params = session.evoked
        if getattr(params, 'display_tmin', None) is not None:
            x_lo = params.display_tmin
        else:
            x_lo = session.epochs.tmin

        if getattr(params, 'display_tmax', None) is not None:
            x_hi = params.display_tmax
        else:
            x_hi = session.epochs.tmax

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
            subject_line=format_subject_label(session, condition),
            caption_line=format_caption_label(session.filter, session.epochs, session.evoked),
        )

        figs.append(finalize_figure(fig, header))

    return merge_figures_vertical(figs)
