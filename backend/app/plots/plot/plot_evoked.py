import matplotlib.pyplot as plt
from mne import Evoked

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.grid_plot_helpers import draw_evoked_response
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


def prepare_evoked_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    evoked = executor.get_evoked(session)
    if evoked is None:
        return None

    evoked = prepare_channels(evoked, session.filter)
    return evoked


def plot_evoked(evoked: Evoked, session: PipelineSession):
    """Plot evoked time course; return finalized figure."""
    fig, ax = plt.subplots(1, 1)
    draw_evoked_response(ax, evoked, session.evoked)

    params = session.evoked
    x_lo = params.display_tmin if getattr(params, 'display_tmin', None) is not None else session.epochs.tmin
    x_hi = params.display_tmax if getattr(params, 'display_tmax', None) is not None else session.epochs.tmax
    ax.set_xlim(x_lo, x_hi)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("µV")
    nave = getattr(evoked, 'nave', None)
    if nave is not None:
        ax.text(1, 1, f"n={int(nave)}", transform=ax.transAxes, ha='right', va='bottom', fontsize=8, color='0.4')

    header = FigureHeader(
        plot_name="Evoked Plot",
        subject_line=format_subject_label(session.task, session.epochs.stimulus),
        caption_line=str(params)
    )

    return finalize_figure(fig, header)
