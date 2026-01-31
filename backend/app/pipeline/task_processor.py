"""
Signal processing pipeline: filtering, epoching and evoked computation with caching.
"""

import logging
import numpy as np
from mne import Epochs, set_log_level, events_from_annotations

from .constants import EVENT_ID, RESTING_STATE_EVENT_ID, CCD_EVENT_ID
from app.schemas.task_scehma import TaskRequest
from app.schemas.filter_schema import FilterParams, EpochParams, EvokedParams
from app.core.cache_manager import CacheKey
from app.pipeline.signal_cleaner import EEGCleaner

set_log_level("WARNING")
log = logging.getLogger(__name__)

def preprocess_surround_supp(processor, params: EpochParams):
    filtered = processor.get_filtered(params)
    events = processor.get_events()
    if events is None:
        return None, None

    stim = events[events["value"] == "stim_ON"].copy()
    if stim.empty:
        return None, None

    stim["label"] = stim.apply(
        lambda r: f"bg{int(r['background'])}_fg{r['foreground_contrast']}_stim{int(r['stimulus_cond'])}",
        axis=1,
    )
    stim["event_code"] = stim["label"].map(EVENT_ID)

    sfreq = float(filtered.info["sfreq"])
    stim = stim[stim["onset"].notna()].copy()
    stim["sample"] = np.round(stim["onset"] * sfreq).astype(int)

    tmin_samp = int(np.floor(params.tmin * sfreq))
    tmax_samp = int(np.ceil(params.tmax * sfreq))
    n_times = int(filtered.n_times)

    ok = (
        (stim["sample"] + tmin_samp >= 0)
        & (stim["sample"] + tmax_samp < n_times)
    )
    stim = stim.loc[ok]
    if stim.empty:
        return None, None

    events_arr = np.column_stack(
        [
            stim["sample"].values,
            np.zeros(len(stim), dtype=int),
            stim["event_code"].values,
        ]
    )

    event_id = {k: EVENT_ID[k] for k in stim["label"].unique()}
    epochs = Epochs(
        filtered,
        events_arr,
        event_id=event_id,
        tmin=params.tmin,
        tmax=params.tmax,
        proj=True,
        preload=False,
    )

    labels = stim["label"].values[epochs.selection]
    return epochs, labels


def preprocess_resting_state(processor, params: EpochParams):
    filtered = processor.get_filtered(params)
    df = processor.get_events()
    if df is None:
        return None, None

    if {"value", "onset"} <= set(df.columns):
        starts = df[df["value"] == "resting_start"]["onset"]
        ends = df[df["value"].isin(["resting_end", "break cnt"])]["onset"]
        if not starts.empty and not ends.empty:
            filtered.crop(float(starts.iloc[0]), float(ends.iloc[-1]))

    events, ann_id = events_from_annotations(filtered)
    new_events = []
    present = []

    for name, code in [
        ("open", "instructed_toOpenEyes"),
        ("close", "instructed_toCloseEyes"),
    ]:
        if code in ann_id:
            rows = events[events[:, 2] == ann_id[code]]
            for r in rows:
                new_events.append([r[0], 0, RESTING_STATE_EVENT_ID[name]])
            if len(rows):
                present.append(name)

    if not new_events:
        return None, None

    epochs = Epochs(
        filtered,
        np.array(sorted(new_events)),
        event_id={k: RESTING_STATE_EVENT_ID[k] for k in present},
        tmin=params.tmin,
        tmax=params.tmax,
        proj=True,
        preload=False,
    )
    return epochs, present


def preprocess_ccd(processor, params: EpochParams):
    filtered = processor.get_filtered(params)
    events, ann_id = events_from_annotations(processor.get_raw())

    if "contrastTrial_start" not in ann_id:
        return None, None

    rows = events[events[:, 2] == ann_id["contrastTrial_start"]]
    if not len(rows):
        return None, None

    new_events = np.column_stack(
        [
            rows[:, 0].astype(int),
            np.zeros(len(rows), dtype=int),
            np.full(len(rows), CCD_EVENT_ID["trial_start"], dtype=int),
        ]
    )

    epochs = Epochs(
        filtered,
        new_events,
        event_id=CCD_EVENT_ID,
        tmin=params.tmin,
        tmax=params.tmax,
        proj=True,
        preload=False,
    )
    return epochs, ["trial_start"]


TASK_PREPROCESSORS = {
    "surroundSupp": preprocess_surround_supp,
    "RestingState": preprocess_resting_state,
    "contrastChangeDetection": preprocess_ccd,
}


class EEGTaskProcessor:
    def __init__(self, get_raw_fn, get_events_fn, task_dto: TaskRequest, cache):
        self.get_raw = get_raw_fn
        self.get_events = get_events_fn
        self.task_dto = task_dto
        self.cache = cache

    def get_filtered(self, params: FilterParams):
        ck_clean = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="cleaned",
            params=params.cleaning_key,
            pipeline_ver=self.cache.pipeline_ver,
        )
        cached = self.cache.load_raw_filtered(ck_clean)
        if cached is not None:
            return cached

        ck_pre = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="prefilter",
            params=params.filter_key,
            pipeline_ver=self.cache.pipeline_ver,
        )
        raw = self.cache.load_raw_filtered(ck_pre)
        if raw is None:
            raw = EEGCleaner.pre_filter(self.get_raw(), params)
            path = self.cache.save_raw_filtered(raw, ck_pre)
            raw = mne.io.read_raw_fif(path, preload=False, verbose="ERROR")

        raw = EEGCleaner.clean_mark(raw, params)
        self.cache.save_raw_filtered(raw, ck_clean)
        return raw

    def get_epochs(self, params: EpochParams):
        fn = TASK_PREPROCESSORS.get(self.task_dto.task)
        if fn is None:
            log.warning("Unsupported task: %s", self.task_dto.task)
            return None, "unavailable"

        ck = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="epochs",
            params=params.epochs_key,
            pipeline_ver=self.cache.pipeline_ver,
        )

        cached = self.cache.load_epochs(ck)
        if cached:
            epochs, labels = cached
        else:
            epochs, labels = fn(self, params)
            if epochs is None:
                return None, "unavailable"
            if epochs.info["bads"]:
                epochs = epochs.interpolate_bads(reset_bads=True)
            self.cache.save_epochs(epochs, ck, labels)

        if params.stimulus:
            stim = params.stimulus[0] if isinstance(params.stimulus, list) else params.stimulus
            if stim not in epochs.event_id:
                return None, "unavailable"
            epochs = epochs[stim]
        else:
            epochs = epochs.apply_baseline((None, 0.0))

        return epochs, labels

    def get_evoked(self, params: EvokedParams):
        ck = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="evoked",
            params=params.evoked_key,
            pipeline_ver=self.cache.pipeline_ver,
        )

        evk = self.cache.load_evoked(ck)
        if evk is not None:
            return evk

        epochs, _ = self.get_epochs(params)
        if epochs is None:
            return None

        if epochs.info["bads"]:
            epochs = epochs.interpolate_bads(reset_bads=True)

        evk = epochs.average()
        self.cache.save_evoked(evk, ck)
        return evk
