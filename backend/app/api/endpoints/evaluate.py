from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.evaluate_schema import EvaluateRequest, EvaluateResponse

router = APIRouter()

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(file: UploadFile = File(...)):  # File is required
    try:
        if not file:
            raise HTTPException(status_code=400, detail="File must be uploaded.")
        
        return {
            "message": f"Evaluation for '{file.filename}' file"
        }
    except Exception as e:
        # General error handler for any unexpected issues
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")