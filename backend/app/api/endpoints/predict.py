from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.predict_schema import PredictRequest, PredictResponse

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest, file: UploadFile = File(...)):  # File is required
    try:
        if not file:
            raise HTTPException(status_code=400, detail="File must be uploaded.")
        
        return {
            "message": f"Prediction for '{file.filename}' file"
        }
    except Exception as e:
        # General error handler for any unexpected issues
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")