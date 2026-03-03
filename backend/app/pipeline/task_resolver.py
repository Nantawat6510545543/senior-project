"""Subject-level access layer resolving single tasks or building cohorts."""
from typing import Union

import logging
import time

from app.schemas.task_schema import SingleSubjectTask, CohortTask
from app.pipeline.task_executor import EEGTaskExecutor
from app.pipeline.cohort_executor import EEGCohortExecutor
from app.core.participants_loader import ParticipantManager

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
    # TODO deprecate
    def resolve_task(self, task: Union[SingleSubjectTask, CohortTask]):

        if isinstance(task, SingleSubjectTask):
            return self._resolve_single(task)

        if isinstance(task, CohortTask):
            return self._resolve_cohort(task)

        raise TypeError(f"Unsupported task type: {type(task)}")

    def _resolve_single(self, task: SingleSubjectTask) -> EEGTaskExecutor:
        subject_dir = self._participants.subject_data_dir(task.subject)

        return EEGTaskExecutor(task=task, data_dir=subject_dir)

    def _resolve_cohort(self, cohort_task: CohortTask) -> EEGCohortExecutor:
        subjects = self._participants.filter_subjects_by_dto(cohort_task)

        task = cohort_task.task
        models = []
        for subj in subjects:
            subj_tasks = self._participants.list_tasks(subj)
            runs = [r for (t, r) in subj_tasks if t == task] or [None]
            subj_dir = self._participants.subject_data_dir(subj)
            for run in runs:
                dto = SingleSubjectTask(subject=subj, task=task, run=run)
                models.append(EEGTaskExecutor(dto, subj_dir))
        
        cohort = EEGCohortExecutor(cohort_task, models, len(subjects))

        return cohort
