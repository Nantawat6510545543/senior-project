from fastapi import APIRouter, HTTPException
from app.schemas.train_schema import TrainRequest, TrainResponse

router = APIRouter()

@router.post("/train", response_model=TrainResponse)
async def train(request: TrainRequest):
    try:
        model_name = request.model_name
        dataset_name = request.dataset_name
        epochs = request.epochs
        kfolds = request.kfolds

        return {
            "message": (
                f"Training started for model '{model_name}' with dataset '{dataset_name}', "
                f"for {epochs} epochs and {kfolds}-fold cross-validation."
            )
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")