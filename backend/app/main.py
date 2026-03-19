import time
import logging

# MUST be first — before any plot modules import pyplot
from app.core import matplotlib_config

from dotenv import load_dotenv
load_dotenv() # Load .env before program runs

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    plot, participants, params_schema, progress_ws, show_data
)

from app.core.config import DATA_ROOT, FRONTEND_URL, BACKEND_URL
from app.core.participants_loader import ParticipantManager

app = FastAPI()

origins = [
    FRONTEND_URL,  # Frontend URL
    BACKEND_URL,  # Backend URL
]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def measure_request_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)

    duration = time.perf_counter() - start
    logger.info(
        "%s %s took %.3fs",
        request.method,
        request.url.path,
        duration,
    )

    return response

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def startup():
    app.state.participant_manager = ParticipantManager(data_dir=DATA_ROOT)

# Register the API routers
app.include_router(plot.router)
app.include_router(show_data.router)
app.include_router(params_schema.router)
app.include_router(participants.router)
app.include_router(progress_ws.router)

# To run use -> "uvicorn app.main:app --reload" OR "fastapi dev"
@app.get("/")
def root():
    return {"message": "Welcome to the ML API"}
