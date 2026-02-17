# MUST be first — before any plot modules import pyplot
from app.core import matplotlib_config

from dotenv import load_dotenv
load_dotenv() # Load .env before program runs

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import train, predict, evaluate, compare, plot, participants, params_schema, session
from app.pipeline.task_resolver import EEGTaskResolver
from app.core.config import DATA_ROOT

# TODO disable matplotlib interactive plot pop-up (use plt.ioff())
app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend URL
    "http://localhost:8000",  # Backend URL
]

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
app.include_router(session.router)

# To run use -> uvicorn app.main:app --reload
@app.get("/")
def root():
    return {"message": "Welcome to the ML API"}
