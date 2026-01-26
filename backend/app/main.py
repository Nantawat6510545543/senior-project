from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import train, predict, evaluate, compare, plot, participants

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

# Register the API routers
app.include_router(plot.router)
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(evaluate.router)
app.include_router(compare.router)

app.include_router(
    participants.router,
    prefix="/participants",
    tags=["participants"],
)

# To run use -> uvicorn app.main:app --reload
@app.get("/")
def root():
    return {"message": "Welcome to the ML API"}
