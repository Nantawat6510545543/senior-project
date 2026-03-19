"""Cohort-level executor aggregating multiple task executors."""

import logging
import pandas as pd
import time

from mne import concatenate_raws, concatenate_epochs, grand_average
from tqdm.auto import tqdm

from app.core.progress_logger import ProgressEmitter
from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession


class EEGCohortExecutor:
    """Aggregate operations (filter, epochs, evoked) across a set of task models."""
    def __init__(
            self,
            task_executor_list: list[EEGTaskExecutor],
            subject_length: int,
            ws_progress: ProgressEmitter | None
        ):
        """Initialize cohort with filter DTO, task models and subject count."""
        self.task_executor_list = task_executor_list
        self.subject_length = subject_length
        self.ws_progress = ws_progress
        self.filtered_raw = None
        self.epochs = None
        self.labels = None
        self.evoked = None
        self._electrodes = None
        self._metadata = None
        self._channels = None
        self._events_concat = None
        self._log = logging.getLogger(__name__)

    @property
    def events(self):
        """Concatenate per-task events into a single DataFrame (computed lazily)."""
        if self._events_concat is None:
            t0 = time.perf_counter()
            events_list = []
            for tm in tqdm(self.task_executor_list, total=len(self.task_executor_list), desc="Collect events", leave=False):
                ev = tm.events
                if ev is not None:
                    events_list.append(ev)
            self._events_concat = pd.concat(events_list, ignore_index=True) if events_list else pd.DataFrame()
            self._log.info("Concatenated events from %d tasks in %.2fs", len(events_list), time.perf_counter() - t0)
        return self._events_concat

    @property
    def electrodes(self):
        """Return electrodes table from the first task (cached)."""
        if not self._electrodes and self.task_executor_list:
            self._electrodes = getattr(self.task_executor_list[0], "electrodes", None)
        return self._electrodes

    @property
    def metadata(self):
        """Return metadata JSON from the first task (cached)."""
        if not self._metadata and self.task_executor_list:
            self._metadata = getattr(self.task_executor_list[0], "metadata", None)
        return self._metadata

    @property
    def channels(self):
        """Return channels table from the first task (cached)."""
        if not self._channels and self.task_executor_list:
            self._channels = self.task_executor_list[0].channels
        return self._channels

    def get_filtered_raw(self, session: PipelineSession):
        """Filter and concatenate Raw objects across all tasks (with cache)."""
        if self.filtered_raw is not None:
            return self.filtered_raw

        filtered_list = []
        t0 = time.perf_counter()

        progress_bar = tqdm(
            self.task_executor_list,
            desc="Filtering raws",
            total=len(self.task_executor_list),
            leave=False
        )

        for i, task_executor in enumerate(progress_bar):
            raw = task_executor.get_filtered_raw(session)
            if raw is not None:
                filtered_list.append(raw)

            # ---- WS PROGRESS ----
            if self.ws_progress:
                meter = tqdm.format_meter(
                    n=i + 1,
                    total=len(self.task_executor_list),
                    elapsed=progress_bar.format_dict.get("elapsed", 0),
                    rate=progress_bar.format_dict.get("rate", None),
                    unit="task"
                )

                self.ws_progress.sync_log(
                    f"[Filter] {i+1}/{len(self.task_executor_list)} | {meter}",
                    progress=(i + 1) / len(self.task_executor_list)
                )

        t_loop = time.perf_counter() - t0
        if not filtered_list:
            self._log.info("No raws produced (loop took %.2fs)", t_loop)
            return None

        self._log.info("Concatenating %d raws (filter loop %.2fs)", len(filtered_list), t_loop)
        t_cat0 = time.perf_counter()
        self.filtered_raw = concatenate_raws(filtered_list)
        t_cat = time.perf_counter() - t_cat0
        self._log.info("Concatenated raws in %.2fs", t_cat)
        try:
            for r in filtered_list:
                if hasattr(r, 'close') and r is not self.filtered_raw:
                    try:
                        r.close()
                    except Exception:
                        pass
        finally:
            filtered_list.clear()
        return self.filtered_raw

    def get_epochs(self, session: PipelineSession):
        """Build and concatenate Epochs across tasks; return (epochs, labels)."""
        if self.epochs is not None:
            return self.epochs, self.labels

        epochs_list = []
        labels_union = set()

        t0 = time.perf_counter()

        progress_bar = tqdm(
            self.task_executor_list,
            desc="Building epochs",
            total=len(self.task_executor_list),
            leave=False
        )

        for i, task_executor in enumerate(progress_bar):
            epochs, labels = task_executor.get_epochs(session)
            if epochs is None:
                continue
            epochs_list.append(epochs)
            if isinstance(labels, str) and labels == "unavailable":
                return None
            if labels is not None:
                labels_union.update(labels)

            # ---- WS PROGRESS ----
            if self.ws_progress:
                meter = tqdm.format_meter(
                    n=i + 1,
                    total=len(self.task_executor_list),
                    elapsed=progress_bar.format_dict.get("elapsed", 0),
                    rate=progress_bar.format_dict.get("rate", None),
                    unit="task"
                )

                self.ws_progress.sync_log(
                    f"[Epochs] {i+1}/{len(self.task_executor_list)} | {meter}",
                    progress=(i + 1) / len(self.task_executor_list)
                )

        t_loop = time.perf_counter() - t0

        if not epochs_list:
            self._log.info("No epochs produced (loop took %.2fs)", t_loop)
            return None

        self._log.info("Concatenating %d epochs (build loop %.2fs)", len(epochs_list), t_loop)
        t_cat0 = time.perf_counter()
        self.epochs = concatenate_epochs(epochs_list)
        t_cat = time.perf_counter() - t_cat0
        self._log.info("Concatenated epochs in %.2fs", t_cat)
        epochs_list.clear()
        self.labels = sorted(labels_union)
        return self.epochs, self.labels

    def get_evoked(self, session: PipelineSession):
        """Compute per-subject averages then grand-average across subjects."""
        if self.evoked is not None:
            return self.evoked

        # 1) Get evoked for each task_executor
        evokeds_by_subject: dict[str, list] = {}
        t0 = time.perf_counter()

        progress_bar = tqdm(
            self.task_executor_list,
            desc="Computing evoked",
            total=len(self.task_executor_list),
            leave=False
        )

        for i, task_executor in enumerate(progress_bar):
            evk = task_executor.get_evoked(session)
            if evk is None:
                continue
            subj = task_executor.task.subject
            if subj is None:
                continue
            evokeds_by_subject.setdefault(subj, []).append(evk)

            if self.ws_progress:
                self.ws_progress.sync_log(
                    f"[Evoked] Collect {i+1}/{len(self.task_executor_list)}",

            progress=(i + 1) / len(self.task_executor_list) * 0.6
        )

        t_evoked_loop = time.perf_counter() - t0

        if not evokeds_by_subject:
            self._log.info("No evoked responses computed (loop took %.2fs)", t_evoked_loop)
            return None

        # 2) For same subject: average runs first (nave-weighted)
        per_subject_evoked = []
        t_sub0 = time.perf_counter()

        subjects = list(evokeds_by_subject.items())

        for i, (subj, evk_list) in enumerate(subjects):
            if not evk_list:
                continue
            if len(evk_list) == 1:
                per_subject_evoked.append(evk_list[0])
            else:
                per_subject_evoked.append(grand_average(evk_list))

            if self.ws_progress:
                self.ws_progress.sync_log(
                    f"[Evoked] Subject avg {i+1}/{len(subjects)}",
                    progress=0.6 + (i + 1) / len(subjects) * 0.3
                )

        t_sub = time.perf_counter() - t_sub0
        self._log.info("Per-subject averaging: %d subjects in %.2fs", len(evokeds_by_subject), t_sub)

        if not per_subject_evoked:
            return None

        # 3) Grand-average across subjects (nave-weighted)
        t_ga0 = time.perf_counter()
        if len(per_subject_evoked) == 1:
            self.evoked = per_subject_evoked[0]
        else:
            self.evoked = grand_average(per_subject_evoked)

        if self.ws_progress:
            self.ws_progress.sync_log(
                "[Evoked] Grand averaging...",
                progress=0.95
            )

        t_ga = time.perf_counter() - t_ga0
        self._log.info("Grand average across %d subjects in %.2fs (compute loop %.2fs)",
                       len(per_subject_evoked), t_ga, t_evoked_loop)

        return self.evoked
