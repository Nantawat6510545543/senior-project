"""
Signal processing pipeline: filtering, epoching and evoked computation with caching.
"""

import logging
import numpy as np
from mne import Epochs, set_log_level, events_from_annotations
from mne.io import read_raw_fif

from .constants import EVENT_ID, RESTING_STATE_EVENT_ID, CCD_EVENT_ID

from app.core.cache_manager import CacheKey
from app.pipeline.signal_cleaner import EEGCleaner
from app.schemas.task_schema import SingleSubjectTask
from app.schemas.params.base_filter_schema import FilterParams
from app.schemas.params.epoch_filter_schema import EpochParams
from app.schemas.params.evoked_filter_schema import EvokedParams


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
    """Apply preprocessing recipe per task and manage cached intermediate artifacts."""
    def __init__(self, get_raw_fn, get_events_fn, task_dto: SingleSubjectTask, cache):
        self.get_raw = get_raw_fn
        self.get_events = get_events_fn
        self.task_dto = task_dto
        self.cache = cache

        self._log = logging.getLogger(__name__)

    def _canonical_task(self, task_name: str) -> str:
        # BIDS: task_run-1, task_acq-xyz_run-2, etc
        return task_name.split("_")[0]

    def _apply_stimulus_filter(self, epochs: Epochs, params: EpochParams):
        stim = params.stimulus
        if isinstance(stim, (list, tuple)):
            stim = stim[0] if len(stim) > 0 else None
        if stim:
            if stim in epochs.event_id:
                return epochs[stim]
            self._log.warning("stim '%s' not in available event IDs %s", stim, list(epochs.event_id.keys()))
            return None
        return epochs.apply_baseline(baseline=(None, 0.0))

    def get_filtered(self, params: FilterParams):
        """Return cleaned Raw using cached prefilter/clean stages when available."""
        # 1) Find cleaned cache
        clean_ck = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="cleaned",
            params=params.cleaning_key,
            pipeline_ver=self.cache.pipeline_ver,
        )
        cleaned_cached = self.cache.load_raw_filtered(clean_ck)
        if cleaned_cached is not None:
            return cleaned_cached

        # 2) If cleaned cache not found, Build prefilter cache (Bandpass/resample/notch)
        pre_ck = CacheKey(
            subject=self.task_dto.subject,
            task=self.task_dto.task,
            run=self.task_dto.run,
            stage="prefilter",
            params=params.filter_key,
            pipeline_ver=self.cache.pipeline_ver,
        )
        cached = self.cache.load_raw_filtered(pre_ck)
        if cached is None:
            raw_pref = EEGCleaner.pre_filter(self.get_raw(), params)
            p = self.cache.save_raw_filtered(raw_pref, pre_ck)
            del raw_pref
            raw_pref = read_raw_fif(p.as_posix(), preload=False, verbose="ERROR")
        else:
            raw_pref = cached

        # 3) Mark bad channels/time windows and save cleaned cache
        raw_clean = EEGCleaner.clean_mark(raw_pref, params)
        self.cache.save_raw_filtered(raw_clean, clean_ck)
        return raw_clean

    def get_epochs(self, params: EpochParams) -> Epochs:
        """Return (epochs, labels) via registered task preprocessor with stimulus filter."""
        # preprocess_fn = self.preprocessors.get(self.task_dto.task)
        task_key = self._canonical_task(self.task_dto.task)
        fn = TASK_PREPROCESSORS.get(task_key)

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

        epochs, labels = self.cache.load_epochs(ck)
        if epochs is not None:
            epochs_sel = self._apply_stimulus_filter(epochs, params)
            if epochs_sel is None:
                return None, "unavailable"
            return epochs_sel, labels

        epochs, labels = fn(self, params)
        if epochs is None:
            return None, "unavailable"

        if epochs.info.get('bads'):
            epochs = epochs.interpolate_bads(reset_bads=True)

        if self.cache and ck:
            self.cache.save_epochs(epochs, ck, labels=labels)

        epochs_sel = self._apply_stimulus_filter(epochs, params)
        if epochs_sel is None:
            return None, "unavailable"

        return epochs_sel, labels

    def get_evoked(self, params: EvokedParams):
        """Return evoked average from epochs, caching on disk when possible."""
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
