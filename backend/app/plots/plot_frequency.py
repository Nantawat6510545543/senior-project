
# # def plot_frequency(self, task_dto: BaseTaskDTO, params: EpochPSDParamsDTO):
# #     """Plot average PSD with optional dB scaling; return finalized figure."""
# #     epochs, labels = self.get_epochs(task_dto, params)
# #     if epochs is None:
# #         return None
# #     epochs = prepare_channels(epochs, params)
# #     sfreq = epochs.info["sfreq"]
# #     nfft = int(max(8, sfreq * max(0.5, (params.tmax - params.tmin))))
# #     psd = epochs.compute_psd(
# #         method="welch",
# #         fmin=params.fmin,
# #         fmax=params.fmax,
# #         tmin=params.tmin,
# #         tmax=params.tmax,
# #         n_fft=nfft,
# #         window="hann",
# #         average='mean',
# #     )
# #     fig = psd.plot(average=params.average, spatial_colors=params.spatial_colors, dB=params.dB, show=False)
# #     return finalize_figure(fig, task_dto, caption_line=str(params), plot_name="Frequency Domain")

from app.core.config import DATA_ROOT
from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_resolver import EEGTaskResolver
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


def prepare_frequency_plot_data(session: PipelineSession):
    epochs_dto = session.epochs

    resolver = EEGTaskResolver(DATA_ROOT)
    executor = resolver.resolve_task(session.task)
    epochs, _ = executor.get_epochs(epochs_dto)

    if epochs is None:
        return None

    epochs = prepare_channels(epochs, epochs_dto)
    sfreq = epochs.info["sfreq"]
    nfft = int(max(8, sfreq * max(0.5, (epochs_dto.tmax - epochs_dto.tmin))))
    psd = epochs.compute_psd(
        method="welch",
        fmin=epochs_dto.fmin,
        fmax=epochs_dto.fmax,
        tmin=epochs_dto.tmin,
        tmax=epochs_dto.tmax,
        n_fft=nfft,
        window="hann",
        average='mean',
    )
    return psd

def plot_frequency(psd, session: PipelineSession):
    """Plot average PSD with optional dB scaling; return finalized figure."""
    epochs_dto = session.epochs

    fig = psd.plot(
        average=epochs_dto.average,
        spatial_colors=epochs_dto.spatial_colors,
        dB=epochs_dto.dB,
        show=False
    )
    
    header = FigureHeader(
        plot_name="Frequency Domain",
        subject_line=format_subject_label(session.task),
        caption_line=str(epochs_dto)
    )

    final_fig = finalize_figure(fig, header)
    return final_fig
