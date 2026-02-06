from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse

import io
import matplotlib.pyplot as plt

from app.plots.plot_sensors import plot_sensors
from app.schemas.task_schema import SingleSubjectTask
from app.schemas.params.base_filter_schema import FilterParams

router = APIRouter()

# TODO fix with real example
def plot_time_domain(ax):
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title("Time Domain")

PLOT_HANDLERS = {
    "time_domain": plot_time_domain,
    "sensor_layout": plot_sensors,
}

@router.get("/plot")
def plot(
    type: str = Query(...),
    task: str = Query(None),
    subject: str = Query(None),
    run: str | None = Query(None),
):
    if type not in PLOT_HANDLERS:
        raise HTTPException(400, "Unknown plot type")

    fig = None

    sst = SingleSubjectTask(
        task=task,
        subject=subject,
        run=run
    )
    params = FilterParams()

    if type == "sensor_layout":
        fig = plot_sensors(sst, params)

    else:
        fig, ax = plt.subplots()
        PLOT_HANDLERS[type](ax)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")