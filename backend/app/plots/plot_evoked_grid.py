"""Grid of evoked responses, one cell per condition/label."""
import numpy as np

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession
from .grid_plot_helpers import draw_evoked_response, render_label_grid
from .plot_merger import merge_figures_vertical


def prepare_evoked_grid_data(executor: EEGTaskExecutor, session: PipelineSession):
    evoked_dto = session.evoked
    epochs, available_labels = executor.get_epochs(evoked_dto)
    if epochs is None:
        return None

    evoked_cache = {}

    for label in available_labels:
        try:
            p = evoked_dto.model_copy(update={"stimulus": label})

            evoked = executor.get_evoked(p)
            if evoked is None:
                continue

            evoked = prepare_channels(evoked, p)

            data_uv = evoked.data * 1e6
            dmin = float(np.nanmin(data_uv)) if data_uv.size else None
            dmax = float(np.nanmax(data_uv)) if data_uv.size else None

            nave = getattr(evoked, "nave", None)

            evoked_cache[label] = (evoked, dmin, dmax, nave)

        except Exception:
            continue

    return epochs, available_labels, evoked_cache


def plot_evoked_grid(epochs, available_labels, evoked_cache, session: PipelineSession):
    """Render evoked response per label in a grid; return figure or None."""
    evoked_dto = session.evoked

    def _draw(ax, label):
        item = evoked_cache.get(label)
        if item is None:
            return None

        evoked, dmin, dmax, nave = item

        draw_evoked_response(ax, evoked, evoked_dto)

        if nave is not None:
            ax.text(
                1, 1, f"n={int(nave)}",
                transform=ax.transAxes,
                ha="right", va="bottom",
                fontsize=8, color="0.4"
            )

        if dmin is not None and dmax is not None:
            return dmin, dmax

        return None

    rendered_fig = render_label_grid(
        task_dto=session.task,
        epochs=epochs,
        available_labels=available_labels,
        params=evoked_dto,
        plot_name="Evoked Grid",
        xlim=(evoked_dto.tmin, evoked_dto.tmax),
        xlabel="Time [s]",
        unit_tag="µV",
        per_cell_draw=_draw,
    )

    return merge_figures_vertical(rendered_fig)
