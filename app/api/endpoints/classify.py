from fastapi import APIRouter, UploadFile, File
from app.services import preprocessing
from app.models import predictor
from app.schemas.response import ClassifyResponse

router = APIRouter()

@router.post("/", response_model=ClassifyResponse)
async def classify_sample(file: UploadFile = File(...)):
    raw = await file.read()
    processed = preprocessing.run(raw)
    result = predictor.predict(processed)
    return ClassifyResponse(**result)
