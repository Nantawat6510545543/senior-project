import io
import matplotlib.pyplot as plt

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.config import DATA_ROOT
from app.pipeline.task_resolver import EEGTaskResolver
from app.core.session_store import get_session
from app.plots.plot_epochs import plot_epochs, prepare_epochs_plot_data
from app.plots.plot_evoked import plot_evoked, prepare_evoked_plot_data
from app.plots.plot_evoked_grid import plot_evoked_grid, prepare_evoked_grid_data
from app.plots.plot_evoked_joint import plot_evoked_joint, prepare_evoked_joint_plot_data
from app.plots.plot_evoked_per_condition import plot_evoked_per_condition, prepare_evoked_per_condition_plot_data
from app.plots.plot_evoked_topo import plot_evoked_topo, prepare_evoked_topo_plot_data
from app.plots.plot_frequency import plot_frequency, prepare_frequency_plot_data
from app.plots.plot_psd_grid import plot_psd_grid, prepare_psd_grid_data
from app.plots.plot_sensors import build_raw_from_sst, plot_sensors
from app.plots.plot_snr import plot_snr, prepare_snr_plot_data
from app.plots.plot_snr_grid import plot_snr_grid, prepare_snr_grid_data
from app.plots.plot_time_domain import plot_time_domain, prepare_time_domain_plot_data
from app.schemas.ui.view_schema import ViewName


router = APIRouter(prefix="/plot")

@router.get("/{sid}")
def plot(sid: str, view: ViewName = Query(...)):

    session = get_session(sid)
    if not session:
        raise HTTPException(404, "Session not found")

    resolver = EEGTaskResolver(DATA_ROOT)
    task_executor = resolver.resolve_task(session.task)

    fig = None
    if view == "sensor_layout":
        raw = build_raw_from_sst(task_executor, session)
        fig = plot_sensors(raw)

    elif view == "time_domain":
        channels_prepared_raw = prepare_time_domain_plot_data(task_executor, session)
        fig = plot_time_domain(channels_prepared_raw, session)

    elif view == "frequency_domain":
        psd = prepare_frequency_plot_data(task_executor, session)
        fig = plot_frequency(psd, session)

    elif view == "epoch":
        epochs = prepare_epochs_plot_data(task_executor, session)
        fig = plot_epochs(epochs, session)

    elif view == "evoked":
        evoked = prepare_evoked_plot_data(task_executor, session)
        fig = plot_evoked(evoked, session)

    elif view == "evoked_topo":
        evoked = prepare_evoked_topo_plot_data(task_executor, session)
        fig = plot_evoked_topo(evoked, session)

    elif view == "evoked_joint":
        evoked_joint = prepare_evoked_joint_plot_data(task_executor, session)
        fig = plot_evoked_joint(evoked_joint, session)

    elif view == "evoked_per_condition":
        prepared_data_list = prepare_evoked_per_condition_plot_data(task_executor, session)
        fig = plot_evoked_per_condition(prepared_data_list, session)

    elif view == "snr_spectrum":
        psds, freqs, snrs = prepare_snr_plot_data(task_executor, session)
        fig = plot_snr(psds, freqs, snrs, session)

    elif view == "psd_grid":
        epochs, available_labels, psd_cache = prepare_psd_grid_data(task_executor, session)
        fig = plot_psd_grid(epochs, available_labels, psd_cache, session)

    elif view == "snr_grid":
        epochs, available_labels, snr_cache = prepare_snr_grid_data(task_executor, session)
        fig = plot_snr_grid(epochs, available_labels, snr_cache, session)

    elif view == "evoked_grid":
        epochs, available_labels, evoked_cache = prepare_evoked_grid_data(task_executor, session)
        fig = plot_evoked_grid(epochs, available_labels, evoked_cache, session)


    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    plt.clf() # reduce memory creep
    plt.close("all")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
