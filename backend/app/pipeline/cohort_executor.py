import logging
import pandas as pd

from mne import concatenate_raws, concatenate_epochs, grand_average
from tqdm.auto import tqdm

from app.pipeline.task_executor import EEGTaskExecutor


class EEGCohortExecutor:
    """
    Cohort-level executor aggregating multiple task executors.
    """

    def __init__(self, task, executors: list[EEGTaskExecutor]):
        self.task = task
        self.executors = executors

        self.filtered_raw = None
        self.epochs = None
        self.labels = None
        self.evoked = None

        self._events = None
        self._log = logging.getLogger(__name__)

    @property
    def events(self):
        if self._events is None:
            events = [e.get_event() for e in self.executors if e.get_event() is not None]
            self._events = pd.concat(events, ignore_index=True) if events else pd.DataFrame()
        return self._events

    @property
    def electrodes(self):
        return self.executors[0].electrodes if self.executors else None

    @property
    def metadata(self):
        return self.executors[0].metadata if self.executors else None

    @property
    def channels(self):
        return self.executors[0].channels if self.executors else None

    def get_filtered_raw(self, filter_params):
        if self.filtered_raw is not None:
            return self.filtered_raw

        raws = [
            e.get_filtered_raw(filter_params)
            for e in tqdm(self.executors, desc="Filtering raws", leave=False)
            if e.get_filtered_raw(filter_params) is not None
        ]

        if not raws:
            return None

        self.filtered_raw = concatenate_raws(raws)
        return self.filtered_raw

    def get_epochs(self, epoch_params):
        if self.epochs is not None:
            return self.epochs, self.labels

        epochs_list = []
        labels = set()

        for e in self.executors:
            epochs, lbls = e.get_epochs(epoch_params)
            if epochs is not None:
                epochs_list.append(epochs)
                if lbls:
                    labels.update(lbls)

        if not epochs_list:
            return None

        self.epochs = concatenate_epochs(epochs_list)
        self.labels = sorted(labels)
        return self.epochs, self.labels

    def get_evoked(self, epoch_params):
        if self.evoked is not None:
            return self.evoked

        per_subject = {}
        for e in self.executors:
            evk = e.get_evoked(epoch_params)
            if evk is None:
                continue
            per_subject.setdefault(e.task.subject, []).append(evk)

        evokeds = [
            grand_average(v) if len(v) > 1 else v[0]
            for v in per_subject.values()
        ]

        if not evokeds:
            return None

        self.evoked = grand_average(evokeds) if len(evokeds) > 1 else evokeds[0]
        return self.evoked
