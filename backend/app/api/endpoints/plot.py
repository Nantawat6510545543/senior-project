from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
import io

router = APIRouter()

# TODO fix with real example
def plot_time_domain(ax):
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title("Time Domain")

PLOT_HANDLERS = {
    "time_domain": plot_time_domain,
}

@router.get("/plot")
def plot(type: str = Query(...)):
    if type not in PLOT_HANDLERS:
        raise HTTPException(400, "Unknown plot type")

    fig, ax = plt.subplots()
    PLOT_HANDLERS[type](ax)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")