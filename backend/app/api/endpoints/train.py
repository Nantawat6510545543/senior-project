from fastapi import APIRouter, UploadFile, File
from app.services import preprocessing
from app.models import trainer
from app.schemas.response import TrainResponse

router = APIRouter()

@router.post("/", response_model=TrainResponse)
async def train_model(file: UploadFile = File(...)):
    raw = await file.read()
    processed = preprocessing.run(raw)
    accuracy = trainer.train(processed)
    return TrainResponse(status="success", accuracy=accuracy)
