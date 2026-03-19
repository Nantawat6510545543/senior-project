from mne import Epochs, Evoked
from mne.io import Raw
from typing import Optional, Type

from app.core.cache_manager import LocalCache, PIPELINE_VERSION
from app.core.progress_logger import ProgressEmitter
from app.pipeline.task_loader import EEGTaskLoader
from app.pipeline.task_processor import EEGTaskProcessor
from app.schemas.task_schema import SingleSubjectTask
from app.schemas.session_schema import PipelineSession


class EEGTaskExecutor:
    """
    Lazy executor for a single subject/task.
    """

    def __init__(
        self,
        task: SingleSubjectTask,
        data_dir,
        progress_emitter: ProgressEmitter | None = None,
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
        self.progress_emitter = progress_emitter

    def _ensure(self):
        """Ensure loader, cache and processor are initialized."""
        if self.loader is None:
            self.loader = self._loader_cls(self.task, self._data_dir)

        if self.cache is None:
            self.cache = LocalCache(pipeline_ver=PIPELINE_VERSION)

        if self.processor is None:
            self.processor = self._processor_cls(
                self.get_raw,
                self.loader.load_events,
                self.task,
                self.cache,
            )

    def get_raw(self) -> Raw:
        """Return (and cache) raw MNE object for this task."""
        self._ensure()
        if self._raw is None:
            self._raw = self.loader.load_raw()
        return self._raw

    @property
    def events(self):
        """Return (and cache) events DataFrame for this task."""
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

    def get_filtered_raw(self, session: PipelineSession):
        """Return filtered Raw from processor and clear base raw cache."""
        self._ensure()
        raw = self.processor.get_filtered(session)
        self._raw = None
        return raw

    def get_epochs(self, session: PipelineSession) -> Epochs:
        """Return (epochs, labels) from processor for given params."""
        self._ensure()
        return self.processor.get_epochs(session)

    def get_evoked(self, session: PipelineSession) -> Evoked:
        """Return evoked response from processor for given params."""
        self._ensure()
        return self.processor.get_evoked(session)
