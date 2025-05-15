from fastapi import FastAPI
from app.api.endpoints import train, predict, evaluate, compare

app = FastAPI()

# To run use -> uvicorn app.main:app --reload

# Register the API routers
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(evaluate.router)
app.include_router(compare.router)

@app.get("/")
def root():
    return {"message": "Welcome to the ML API"}
