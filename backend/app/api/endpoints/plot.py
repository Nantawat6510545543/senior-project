from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from app.core.session_store import get_session
from app.plots.plot_sensors import build_raw_from_sst, plot_sensors
from app.plots.plot_time_domain import plot_time_domain, prepare_time_domain_plot_data
from app.schemas.ui.view_schema import ViewName

router = APIRouter(prefix="/plot")

# # TODO fix with real example
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
        raw = build_raw_from_sst(session)
        channels_prepared_raw = prepare_time_domain_plot_data(session)
        fig = plot_time_domain(channels_prepared_raw, session)
        # fig, ax = plt.subplots()
        # PLOT_HANDLERS[view](ax)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")