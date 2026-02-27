import time
import logging

# MUST be first — before any plot modules import pyplot
from app.core import matplotlib_config

from dotenv import load_dotenv
load_dotenv() # Load .env before program runs

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    train, predict, evaluate, compare, plot, participants, params_schema, progress_ws, session
)
from app.pipeline.task_resolver import EEGTaskResolver
from app.core.config import DATA_ROOT

app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend URL
    "http://localhost:8000",  # Backend URL
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
    app.state.resolver = EEGTaskResolver(data_dir=DATA_ROOT)

# Register the API routers
app.include_router(plot.router)
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(evaluate.router)
app.include_router(compare.router)
app.include_router(params_schema.router)
app.include_router(participants.router)
app.include_router(progress_ws.router)
app.include_router(session.router)


# To run use -> "uvicorn app.main:app --reload" OR "fastapi dev app/main.py"
@app.get("/")
def root():
    return {"message": "Welcome to the ML API"}
