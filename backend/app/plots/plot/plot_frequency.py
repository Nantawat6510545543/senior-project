from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.figure_header import FigureHeader, format_caption_label, format_subject_label
from app.plots.plot_finalizer import finalize_figure
from app.schemas.session_schema import PipelineSession


def prepare_frequency_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_psd_dto = session.epochs_psd

    epochs, _ = executor.get_epochs(session)

    if epochs is None:
        return None

    epochs = prepare_channels(epochs, session.filter)

    sfreq = epochs.info["sfreq"]
    nfft = int(max(8, sfreq * max(0.5, (epochs_psd_dto.tmax - epochs_psd_dto.tmin))))
    psd = epochs.compute_psd(
        method="welch",
        fmin=epochs_psd_dto.fmin,
        fmax=epochs_psd_dto.fmax,
        tmin=epochs_psd_dto.tmin,
        tmax=epochs_psd_dto.tmax,
        n_fft=nfft,
        window="hann",
        average='mean',
    )
    return psd


def plot_frequency(fq_psd, session: PipelineSession):
    """Plot average PSD with optional dB scaling; return finalized figure."""
    fig = fq_psd.plot(
        average=session.epochs_psd.average,
        spatial_colors=session.epochs_psd.spatial_colors,
        dB=session.epochs_psd.dB,
        show=False
    )

    header = FigureHeader(
        plot_name="Frequency Domain",
        subject_line=format_subject_label(session.task),
        caption_line=format_caption_label(session.filter, session.epochs_psd)
    )

    final_fig = finalize_figure(fig, header)
    return final_fig
