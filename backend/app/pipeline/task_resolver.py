from typing import Union

import logging
import time

from app.schemas.task_scehma import SingleSubjectTask, CohortTask
from app.pipeline.task_executor import EEGTaskExecutor
from app.pipeline.cohort_executor import EEGCohortExecutor
from app.core.participants_loader import 

class EEGTaskResolver:
    """
    Resolve a task DTO into a concrete execution object.
    """

    def __init__(self, data_dir: str):
        self._log = logging.getLogger(__name__)
        self._participants = ParticipantManager(data_dir)

        t0 = time.perf_counter()
        self._log.info(
            "EEGTaskResolver initialized in %.2fs",
            time.perf_counter() - t0,
        )

    # ---------- dataset introspection ----------

    def list_subjects(self):
        return self._participants.list_subjects()

    def list_all_tasks(self):
        return self._participants.list_all_tasks()

    def list_tasks(self, subject):
        return self._participants.list_tasks(subject)

    # ---------- resolution ----------
    def resolve(self, task: Union[SingleSubjectTask, CohortTask]):
        if isinstance(task, SingleSubjectTask):
            return self._resolve_single(task)

        if isinstance(task, CohortTask):
            return self._resolve_cohort(task)

        raise TypeError(f"Unsupported task type: {type(task)}")

    def _resolve_single(self, task: SingleSubjectTask) -> EEGTaskExecutor:
        subject_dir = self._participants.subject_data_dir(task.subject)

        return EEGTaskExecutor(
            task=task.task,
            subject=task.subject,
            run=task.run,
            data_dir=subject_dir,
        )

    def _resolve_cohort(self, task: CohortTask) -> EEGCohortExecutor:
        subjects = self._participants.filter_subjects(
            sex=task.sex,
            age_min=task.age_min,
            age_max=task.age_max,
            ehq_total_min=task.ehq_total_min,
            ehq_total_max=task.ehq_total_max,
            p_factor_min=task.p_factor_min,
            p_factor_max=task.p_factor_max,
            limit=task.subject_limit,
        )

        return EEGCohortExecutor(
            task=task.task,
            subjects=subjects,
            per_subject=task.per_subject,
            participant_manager=self._participants,
        )