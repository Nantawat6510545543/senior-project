"""Responsible only for building ML datasets from epochs."""
from typing import Any, Callable, Dict, Optional, Tuple, List
import numpy as np

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.cohort_executor import EEGCohortExecutor
from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession


def dataset_from_events(executor: EEGTaskExecutor, session: PipelineSession):
    """Build dataset using event labels."""
    params = session.epochs
    epochs, labels = executor.get_epochs(params)
    if epochs is None:
        return None, None, {"reason": "epochs_unavailable"}
    epochs.load_data()
    epochs = prepare_channels(epochs, params)
    X = epochs.get_data()
    if labels is None:
        inv_map = {v: k for k, v in (epochs.event_id or {}).items()}
        y = np.array([inv_map.get(code, "?") for code in epochs.events[:, 2]], dtype=object)
    else:
        y = np.array(labels)
    meta = {
        "sfreq": float(epochs.info.get("sfreq", 0.0)),
        "ch_names": list(epochs.ch_names),
        "event_id": dict(epochs.event_id or {}),
        "shape": tuple(X.shape),
    }
    return X.astype(np.float32), y, meta


def dataset_from_participants(
        executor: EEGTaskExecutor, 
        session: PipelineSession, 
        cols: List[str], 
        get_subjects_metadata: Callable
    ):
    """Build dataset using participants metadata columns (cohort preferred).

    For regression targets, continuous numeric columns are returned as a
    float32 matrix (n_samples, n_outputs). For classification-like usage,
    values are combined into pipe-delimited strings. Currently we treat
    participants targets always as regression when columns are numeric.
    """
    def _to_float(v):
        try:
            if v is None:
                return np.nan
            if isinstance(v, str):
                s = v.strip().replace(',', '')
                if s == '' or s.lower() in {"nan", "none", "na", "null"}:
                    return np.nan
                return float(s)
            return float(v)
        except Exception:
            return np.nan

    params = session.epochs

    if isinstance(executor, EEGCohortExecutor):
        task_models = executor.task_model_list
        if not task_models:
            return None, None, {"reason": "no_task_models"}
        X_parts: List[np.ndarray] = []
        y_parts: List[Any] = []
        subj_ids: List[str] = []
        for tm in task_models:
            epochs, _labels = tm.get_epochs(params)
            if epochs is None:
                continue
            epochs.load_data()
            epochs = prepare_channels(epochs, params)
            subj = getattr(tm.task_dto, "subject", None)
            if subj is None:
                continue
            X_parts.append(epochs.get_data())
            values = []
            if get_subjects_metadata is not None:
                try:
                    df = get_subjects_metadata([subj], cols)
                    if not df.empty:
                        values = [df.iloc[0].get(c) for c in cols]
                except Exception:  # pragma: no cover
                    values = []
            # Convert to floats when possible (NaN if not convertible)
            n_ep = len(epochs)
            if values:
                vec = [_to_float(v) for v in values]
                # Numeric regression mode if at least one finite value exists
                if np.any(np.isfinite(vec)):
                    for _ in range(n_ep):
                        y_parts.append(vec)
                else:
                    # Fall back to classification-like label
                    if len(values) == 1:
                        val = values[0]
                    else:
                        val = "|".join(str(v) for v in values)
                    y_parts.extend([val] * n_ep)
            else:
                y_parts.extend([None] * n_ep)
            subj_ids.extend([str(subj)] * n_ep)
        if not X_parts:
            return None, None, {"reason": "empty_cohort_epochs"}
        X = np.concatenate(X_parts, axis=0)
        # If first element is list -> regression multi-output
        if y_parts and isinstance(y_parts[0], list):
            y = np.array(y_parts, dtype=np.float32)
            # Drop rows with NaNs in any target
            mask = np.isfinite(y).all(axis=1)
            dropped = int((~mask).sum())
            if dropped > 0:
                X = X[mask]
                y = y[mask]
        else:
            y = np.array(y_parts, dtype=object)
        ref_epochs = None
        for tm in task_models:
            e, _ = tm.get_epochs(params)
            if e is not None:
                ref_epochs = e
                ref_epochs = prepare_channels(ref_epochs, params)
                break
        sfreq = float(ref_epochs.info.get("sfreq", 0.0)) if ref_epochs is not None else 0.0
        ch_names = list(ref_epochs.ch_names) if ref_epochs is not None else []
        meta = {"sfreq": sfreq, "ch_names": ch_names, "event_id": {}, "shape": tuple(X.shape), "target_cols": cols, "subject_ids": subj_ids}
        return X.astype(np.float32), y, meta

    # Single-subject fallback
    epochs, _labels = executor.get_epochs(params)
    if epochs is None:
        return None, None, {"reason": "epochs_unavailable"}
    epochs.load_data()
    epochs = prepare_channels(epochs, params)
    X = epochs.get_data()
    subj = session.task.subject
    values = []
    if subj and get_subjects_metadata is not None:
        try:
            df = get_subjects_metadata([subj], cols)
            if not df.empty:
                values = [df.iloc[0].get(c) for c in cols]
        except Exception:  # pragma: no cover
            values = []
    if values:
        vec = np.array([_to_float(v) for v in values], dtype=np.float32)
        if np.any(np.isfinite(vec)):
            y = np.repeat(vec.reshape(1, -1), repeats=len(X), axis=0).astype(np.float32)
            # If vector contains NaN only, mark unavailable
            if not np.isfinite(vec).all():
                # Drop all rows that are NaN (which is all)
                return None, None, {"reason": "nan_targets_single_subject", "target_cols": cols}
        else:
            # fall back to classification-like
            if len(values) == 1:
                val = values[0]
            else:
                val = "|".join(str(v) for v in values)
            y = np.array([val] * len(X), dtype=object)
    else:
        y = np.array([None] * len(X), dtype=object)
    meta = {
        "sfreq": float(epochs.info.get("sfreq", 0.0)),
        "ch_names": list(epochs.ch_names),
        "event_id": dict(epochs.event_id or {}),
        "shape": tuple(X.shape),
        "warning": "constant_label_single_subject_meta_target",
        "target_cols": cols,
        "subject_ids": [str(subj)] * len(X),
    }
    return X.astype(np.float32), y, meta

def build_epoch_dataset(
        executor: EEGTaskExecutor,
        session: PipelineSession,
        get_subjects_metadata: Callable
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Dict[str, Any]]:
    """Return (X, y, meta) using selected target option (event or participants)."""
    params = session.training
    sel = getattr(params, "target", ["stimulus"])
    if isinstance(sel, list) and sel:
        sel = sel[0] or "stimulus"
    sel_norm = sel.strip().lower() if isinstance(sel, str) else "stimulus"
    # sel_norm = session.training.target

    if sel_norm == "stimulus":
        return dataset_from_events(executor, session)
    if sel_norm == "ccd_accuracy":
        return dataset_from_participants(
            executor, session, ["ccd_accuracy"], get_subjects_metadata
        )
    if sel_norm == "ccd_response_time":
        return dataset_from_participants(
            executor, session, ["ccd_response_time"], get_subjects_metadata
        )
    if sel_norm.replace(" ", "") in {"ccd_accuracy+ccd_response_time", "ccd_accuracy+ccd_responsetime"}:
        return dataset_from_participants(
            executor, session, ["ccd_accuracy", "ccd_response_time"], get_subjects_metadata
        )
    # Fallback
    return dataset_from_events(executor, session)