import io
import matplotlib.pyplot as plt

from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse

from app.core.config import DATA_ROOT
from app.core.session_store import get_session
from app.core.progress_logger import ProgressEmitter
from app.core.ws_manager import ws_manager
from app.pipeline.task_resolver import EEGTaskResolver

from app.plots.plot_epochs import plot_epochs, prepare_epochs_plot_data
from app.plots.plot_evoked import plot_evoked, prepare_evoked_plot_data
from app.plots.plot_evoked_grid import plot_evoked_grid, prepare_evoked_grid_data
from app.plots.plot_evoked_joint import plot_evoked_joint, prepare_evoked_joint_plot_data
from app.plots.plot_evoked_per_condition import (
    plot_evoked_per_condition,
    prepare_evoked_per_condition_plot_data,
)
from app.plots.plot_evoked_topo import plot_evoked_topo, prepare_evoked_topo_plot_data
from app.plots.plot_frequency import plot_frequency, prepare_frequency_plot_data
from app.plots.plot_psd_grid import plot_psd_grid, prepare_psd_grid_data
from app.plots.plot_sensors import build_raw_from_sst, plot_sensors
from app.plots.plot_snr import plot_snr, prepare_snr_plot_data
from app.plots.plot_snr_grid import plot_snr_grid, prepare_snr_grid_data
from app.plots.plot_time_domain import plot_time_domain, prepare_time_domain_plot_data
from app.schemas.ui.view_schema import ViewName


def build_plot_figure(view, task_executor, session):
    if view == "sensor_layout":
        raw = build_raw_from_sst(task_executor, session)
        return plot_sensors(raw)

    elif view == "time_domain":
        data = prepare_time_domain_plot_data(task_executor, session)
        return plot_time_domain(data, session)

    elif view == "frequency_domain":
        psd = prepare_frequency_plot_data(task_executor, session)
        return plot_frequency(psd, session)

    elif view == "epoch":
        epochs = prepare_epochs_plot_data(task_executor, session)
        return plot_epochs(epochs, session)

    elif view == "evoked":
        evoked = prepare_evoked_plot_data(task_executor, session)
        return plot_evoked(evoked, session)

    elif view == "evoked_topo":
        evoked = prepare_evoked_topo_plot_data(task_executor, session)
        return plot_evoked_topo(evoked, session)

    elif view == "evoked_joint":
        evoked_joint = prepare_evoked_joint_plot_data(task_executor, session)
        return plot_evoked_joint(evoked_joint, session)

    elif view == "evoked_per_condition":
        data_list = prepare_evoked_per_condition_plot_data(task_executor, session)
        return plot_evoked_per_condition(data_list, session)

    elif view == "snr_spectrum":
        psds, freqs, snrs = prepare_snr_plot_data(task_executor, session)
        return plot_snr(psds, freqs, snrs, session)

    elif view == "psd_grid":
        epochs, labels, cache = prepare_psd_grid_data(task_executor, session)
        return plot_psd_grid(epochs, labels, cache, session)

    elif view == "snr_grid":
        epochs, labels, cache = prepare_snr_grid_data(task_executor, session)
        return plot_snr_grid(epochs, labels, cache, session)

    elif view == "evoked_grid":
        epochs, labels, cache = prepare_evoked_grid_data(task_executor, session)
        return plot_evoked_grid(epochs, labels, cache, session)

    else:
        raise ValueError("Unsupported view")


router = APIRouter(prefix="/plot")

@router.get("/{sid}")
async def plot(sid: str, view: ViewName = Query(...)):

    session = get_session(sid)
    if not session:
        raise HTTPException(404, "Session not found")

    progress = ProgressEmitter(
        lambda msg: ws_manager.send(sid, msg)
    )

    await progress.log("Session loaded")

    try:
        await progress.log("Resolving EEG task")

        resolver = EEGTaskResolver(DATA_ROOT)
        task_executor = resolver.resolve_task(session.task)

        await progress.log(f"Building plot figure for: {view}")

        # All heavy work runs here in one thread
        fig = await run_in_threadpool(
            build_plot_figure,
            view,
            task_executor,
            session
        )

        await progress.log("Encoding PNG")

        buf = io.BytesIO()

        await run_in_threadpool(
            fig.savefig,
            buf,
            format="png",
            bbox_inches="tight"
        )

        plt.close(fig)
        buf.seek(0)

        await progress.log("Plot complete")

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        await progress.log(str(e), level="error")
        raise  # For dev debugging
