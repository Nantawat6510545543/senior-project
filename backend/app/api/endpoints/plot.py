import io
import matplotlib.pyplot as plt

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.session_store import get_session
from app.plots.plot_epochs import plot_epochs, prepare_epochs_plot_data
from app.plots.plot_evoked import plot_evoked, prepare_evoked_plot_data
from app.plots.plot_frequency import plot_frequency, prepare_frequency_plot_data
from app.plots.plot_sensors import build_raw_from_sst, plot_sensors
from app.plots.plot_time_domain import plot_time_domain, prepare_time_domain_plot_data
from app.schemas.ui.view_schema import ViewName

router = APIRouter(prefix="/plot")

# def plot_time_domain(ax):
#     ax.plot([1, 2, 3], [1, 4, 2])
#     ax.set_title("Time Domain")

# PLOT_HANDLERS = {
#     "time_domain": plot_time_domain,
#     "sensor_layout": plot_sensors,
# }

@router.get("/{sid}")
def plot(sid: str, view: ViewName = Query(...)):

    session = get_session(sid)
    if not session:
        raise HTTPException(404, "Session not found")

    fig = None
    if view == "sensor_layout":
        raw = build_raw_from_sst(session)
        fig = plot_sensors(raw)

    elif view == "time_domain":
        channels_prepared_raw = prepare_time_domain_plot_data(session)
        fig = plot_time_domain(channels_prepared_raw, session)
        # fig, ax = plt.subplots()
        # PLOT_HANDLERS[view](ax)

    elif view == "frequency_domain":
        psd = prepare_frequency_plot_data(session)
        fig = plot_frequency(psd, session)

    elif view == "epoch":
        epochs = prepare_epochs_plot_data(session)
        fig = plot_epochs(epochs, session)

    elif view == "evoked":
        evoked = prepare_evoked_plot_data(session)
        fig = plot_evoked(evoked, session)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
