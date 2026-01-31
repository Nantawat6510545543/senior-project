from typing import Optional, Type

from .task_loader import EEGTaskLoader
from .task_processor import EEGTaskProcessor
from app.schemas.task_scehma import SingleSubjectTask
from app.core.cache_manager import LocalCache, PIPELINE_VERSION


class EEGTaskExecutor:
    """
    Lazy executor for a single subject/task.
    """

    def __init__(
        self,
        task: SingleSubjectTask,
        data_dir,
        *,
        cache: Optional[LocalCache] = None,
        loader_cls: Type[EEGTaskLoader] = EEGTaskLoader,
        processor_cls: Type[EEGTaskProcessor] = EEGTaskProcessor,
    ):
        self.task = task
        self._data_dir = data_dir

        self._raw = None
        self._events = None
        self._electrodes = None
        self._metadata = None
        self._channels = None

        self._loader_cls = loader_cls
        self._processor_cls = processor_cls

        self.loader = None
        self.processor = None
        self.cache = cache

    def _ensure(self):
        if self.loader is None:
            self.loader = self._loader_cls(self.task, self._data_dir)

        if self.cache is None:
            self.cache = LocalCache(pipeline_ver=PIPELINE_VERSION)

        if self.processor is None:
            self.processor = self._processor_cls(
                self.get_raw,
                self.get_event,
                self.task,
                self.cache,
            )

    def get_raw(self):
        self._ensure()
        if self._raw is None:
            self._raw = self.loader.load_raw()
        return self._raw

    def get_event(self):
        self._ensure()
        if self._events is None:
            self._events = self.loader.load_events()
        return self._events

    @property
    def electrodes(self):
        self._ensure()
        if self._electrodes is None:
            self._electrodes = self.loader.load_electrodes()
        return self._electrodes

    @property
    def metadata(self):
        self._ensure()
        if self._metadata is None:
            self._metadata = self.loader.load_metadata()
        return self._metadata

    @property
    def channels(self):
        self._ensure()
        if self._channels is None:
            self._channels = self.loader.load_channels()
        return self._channels

    def get_filtered_raw(self, filter_params):
        self._ensure()
        raw = self.processor.get_filtered(filter_params)
        self._raw = None
        return raw

    def get_epochs(self, epoch_params):
        self._ensure()
        return self.processor.get_epochs(epoch_params)

    def get_evoked(self, epoch_params):
        self._ensure()
        return self.processor.get_evoked(epoch_params)
