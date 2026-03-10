import numpy as np
import pandas as pd

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool

from app.core.participants_loader import ParticipantManager
from app.core.progress_logger import ProgressEmitter
from app.core.ws_manager import ws_manager

from app.pipeline.task_resolver import get_single_subject_executor, get_cohort_subject_executor
from app.plots.data import *
from app.plots.ai import *
from app.schemas.session_schema import PipelineSession
from app.schemas.ui.view_schema import ViewName


def build_table_data(view, task_executor, session: PipelineSession, pm: ParticipantManager):

    if view == "eeg_table":
        return prepare_eeg_table_data(task_executor, session)

    elif view == "epochs_table":
        return prepare_epochs_table_data(task_executor, session)

    elif view == "metadata":
        return prepare_metadata_data(task_executor, session)
    
    elif view == "build_dataset":
        return prepare_build_dataset_data(task_executor, session, pm.get_subjects_metadata)

    elif view == "train_eeg":
        return prepare_train_eeg_data(task_executor, session, pm.get_subjects_metadata)
    
    elif view == "model_summary":
        return prepare_model_summary_data(task_executor, session, pm.get_subjects_metadata)

    else:
        raise ValueError("Unsupported table view")


router = APIRouter(prefix="/data")

@router.post("/")
async def show_data(
    request: Request,
    session: PipelineSession,
    view: ViewName = Query(...),
    runId: str = Query(...)
):
    progress = ProgressEmitter(lambda msg: ws_manager.send(runId, msg))

    await progress.log("Session loaded")

    try:
        await progress.log("Resolving EEG task")

        pm = request.app.state.participant_manager

        if session.subject_type == "single":
            task_executor = get_single_subject_executor(pm, session.task)
        else:
            task_executor = get_cohort_subject_executor(pm, session.subject_filter)

        await progress.log(f"Building table data for: {view}")

        result = await run_in_threadpool(
            build_table_data,
            view,
            task_executor,
            session,
            pm
        )

        await progress.log("Serializing table data")

        # Convert DataFrame → JSON-safe structure
        if isinstance(result, pd.DataFrame):
            result = (
                result
                .replace([np.inf, -np.inf], None)
                .fillna("")
                .to_dict(orient="records")
            )

        await progress.log("Table ready")

        return result

    except Exception as e:
        await progress.log(str(e), level="error")
        raise
