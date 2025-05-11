from fastapi import FastAPI
from app.api.endpoints import train, classify

app = FastAPI(title="EEG SSL FastAPI", version="0.1")

# Register routes
app.include_router(train.router, prefix="/train", tags=["Training"])
app.include_router(classify.router, prefix="/classify", tags=["Classification"])

@app.get("/")
def read_root():
    return {"message": "EEG SSL API is up and running!"}
