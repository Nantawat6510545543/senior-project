import numpy as np
import pandas as pd

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.concurrency import run_in_threadpool

from app.core.progress_logger import ProgressEmitter
from app.core.session_store import get_session
from app.core.ws_manager import ws_manager

from app.pipeline.task_resolver import get_single_subject_executor, get_cohort_subject_executor
from app.plots.data import *
from app.schemas.ui.view_schema import ViewName


def build_table_data(view, task_executor, session):

    if view == "eeg_table":
        return prepare_eeg_table_data(task_executor, session)

    elif view == "epochs_table":
        return prepare_epochs_table_data(task_executor, session)

    elif view == "metadata":
        return prepare_metadata_data(task_executor, session)

    else:
        raise ValueError("Unsupported table view")


router = APIRouter(prefix="/data")


@router.get("/{sid}")
async def show_data(sid: str, request: Request, view: ViewName = Query(...)):

    session = get_session(sid)
    if not session:
        raise HTTPException(404, "Session not found")

    progress = ProgressEmitter(lambda msg: ws_manager.send(sid, msg))

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
            session
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