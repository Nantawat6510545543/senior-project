from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


# TODO fix bug with second dataset "resting state" task
def prepare_frequency_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_dto = session.epochs
    psd_dto = session.psd

    epochs, _ = executor.get_epochs(epochs_dto)

    if epochs is None:
        return None

    epochs = prepare_channels(epochs, epochs_dto)

    sfreq = epochs.info["sfreq"]
    nfft = int(max(8, sfreq * max(0.5, (epochs_dto.tmax - epochs_dto.tmin))))
    psd = epochs.compute_psd(
        method="welch",
        fmin=psd_dto.fmin,
        fmax=psd_dto.fmax,
        tmin=epochs_dto.tmin,
        tmax=epochs_dto.tmax,
        n_fft=nfft,
        window="hann",
        average='mean',
    )
    return psd

# TODO fix to proper dto
def plot_frequency(fq_psd, session: PipelineSession):
    """Plot average PSD with optional dB scaling; return finalized figure."""
    psd_dto = session.psd

    fig = fq_psd.plot(
        average=psd_dto.average,
        spatial_colors=psd_dto.spatial_colors,
        dB=psd_dto.dB,
        show=False
    )
    
    header = FigureHeader(
        plot_name="Frequency Domain",
        subject_line=format_subject_label(session.task),
        caption_line=str(psd_dto)
    )

    final_fig = finalize_figure(fig, header)
    return final_fig
