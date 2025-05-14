from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.compare_schema import CompareRequest, CompareResponse

router = APIRouter()

@router.post("/compare", response_model=CompareResponse)
async def compare(
    request: CompareRequest,
    file1: UploadFile = File(...),  # First file
    file2: UploadFile = File(...),  # Second file
):
    try:
        # Ensure both files are uploaded
        if not file1 or not file2:
            raise HTTPException(status_code=400, detail="Both files must be uploaded.")
        
        return {
            "message": f"Comparsion for file '{file1.filename}' and '{file2.filename}'"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")