from fastapi import APIRouter, HTTPException
from app.schemas.train_schema import TrainRequest, TrainResponse

router = APIRouter()

@router.post("/train", response_model=TrainResponse)
async def train(request: TrainRequest):
    try:
        return {
            "message": (
                f"Training started for model '{request.model_name}' with dataset '{request.dataset_name}', "
                f"for {request.epochs} epochs and {request.kfolds}-fold cross-validation."
            )
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")