"""Subject-level access layer resolving single tasks or building cohorts."""
from app.core.participants_loader import ParticipantManager
from app.schemas.task_schema import SingleSubjectTask, CohortTask
from app.pipeline.task_executor import EEGTaskExecutor
from app.pipeline.cohort_executor import EEGCohortExecutor


def get_single_subject_executor(
        pm: ParticipantManager, task: SingleSubjectTask) -> EEGTaskExecutor:

    subject_dir = pm.subject_data_dir(task.subject)
    return EEGTaskExecutor(task, subject_dir)


def get_cohort_subject_executor(
        pm: ParticipantManager, cohort_task: CohortTask) -> EEGCohortExecutor:

    subjects = pm.filter_subjects_by_dto(cohort_task)

    task = cohort_task.task
    models = []
    for subj in subjects:
        subj_tasks = pm.list_tasks(subj)
        runs = [r for (t, r) in subj_tasks if t == task] or [None]
        for run in runs:
            single_subject = SingleSubjectTask(subject=subj, task=task, run=run)
            models.append(get_single_subject_executor(pm, single_subject))
    cohort = EEGCohortExecutor(cohort_task, models, len(subjects))

    return cohort
