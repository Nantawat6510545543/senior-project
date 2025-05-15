from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.schemas.predict_schema import PredictResponse

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="File must be uploaded.")
        
        if not model_name.strip():
            raise HTTPException(status_code=422, detail="model_name must not be empty.")

        return {
            "message": f"Prediction for '{file.filename}' using model '{model_name}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
