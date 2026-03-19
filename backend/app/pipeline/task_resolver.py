"""Subject-level access layer resolving single tasks or building cohorts."""
from app.core.participants_loader import ParticipantManager
from app.core.progress_logger import ProgressEmitter
from app.schemas.params.subject_filter_schema import SubjectFilterParams
from app.schemas.task_schema import SingleSubjectTask
from app.pipeline.cohort_executor import EEGCohortExecutor
from app.pipeline.task_executor import EEGTaskExecutor


def get_single_subject_executor(
        pm: ParticipantManager,
        task: SingleSubjectTask,
        progress_emitter: ProgressEmitter | None = None
    ) -> EEGTaskExecutor:

    subject_dir = pm.subject_data_dir(task.subject)
    return EEGTaskExecutor(task, subject_dir, progress_emitter)


def get_cohort_subject_executor(
        pm: ParticipantManager,
        subject_filter_params: SubjectFilterParams,
        progress_emitter: ProgressEmitter | None = None
    ) -> EEGCohortExecutor:

    subjects = pm.filter_subjects_by_dto(subject_filter_params)

    task = subject_filter_params.task
    task_executor_list = []
    for subj in subjects:
        subj_tasks = pm.list_tasks(subj)
        runs = [r for (t, r) in subj_tasks if t == task] or [None]
        for run in runs:
            single_subject = SingleSubjectTask(subject=subj, task=task, run=run)
            task_executor_list.append(get_single_subject_executor(pm, single_subject))
    cohort = EEGCohortExecutor(task_executor_list, len(subjects), progress_emitter)

    return cohort
