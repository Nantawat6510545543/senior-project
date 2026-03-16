from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession

def prepare_epochs_table_data(executor: EEGTaskExecutor, session: PipelineSession):
    """Return a per-condition summary DataFrame for the selected epochs.

    Columns include label, number of epochs/channels, sampling rate and durations.
    """
    epochs_dto = session.epochs
    epochs, labels = executor.get_epochs(session)

    if epochs is None:
        return None

    rows = []
    for label, _code in epochs.event_id.items():
        try:
            cond_epochs = epochs[label]
        except Exception:
            continue
        if len(cond_epochs) == 0:
            continue
        n_times = len(cond_epochs.times)
        sfreq = float(cond_epochs.info.get('sfreq', 0.0))
        row = {
            'label': label,
            'n_epochs': len(cond_epochs),
            'n_channels': len(cond_epochs.ch_names),
            'timespan_sec': float(cond_epochs.times[-1] - cond_epochs.times[0]) if n_times > 1 else 0.0,
            'sampling_rate': sfreq,
            'duration_per_epoch_sec': float(n_times / sfreq) if sfreq > 0 and n_times > 0 else 0.0,
        }
        rows.append(row)

    return rows

