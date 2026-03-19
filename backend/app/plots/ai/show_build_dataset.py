"""Build a simple dataset summary for training inputs."""
import numpy as np

from typing import Callable

from app.pipeline.task_executor import EEGTaskExecutor
from app.pipeline.trainer_data_builder import build_epoch_dataset
from app.schemas.session_schema import PipelineSession

def prepare_build_dataset_data(
        executor: EEGTaskExecutor,
        session: PipelineSession,
        get_subjects_metadata: Callable
    ):
    """Return a one-row DataFrame summarizing dataset size and class balance."""
    X, y, meta = build_epoch_dataset(executor, session, get_subjects_metadata)
    if X is None:
        return [{"status": [meta.get("reason", "unavailable")]}]
    n_e, n_c, n_t = X.shape
    uniq, counts = np.unique(y, return_counts=True)
    # TODO FIX LABEL WRONG VALUE
    dist = {f"label::{str(k)}": int(v) for k, v in zip(uniq, counts)}
    row = {
        "n_epochs": int(n_e),
        "n_channels": int(n_c),
        "n_times": int(n_t),
        "sfreq": meta.get("sfreq", 0.0),
        **dist,
    }
    return [row]
