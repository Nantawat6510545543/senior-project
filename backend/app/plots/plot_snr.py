"""Signal-to-noise ratio spectrum plot of epochs."""
import numpy as np
import matplotlib.pyplot as plt

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.signal_spatial import compute_snr_spectrum
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.session_schema import PipelineSession


def prepare_snr_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_dto = session.epochs
    psd_dto = session.psd

    epochs, _ = executor.get_epochs(epochs_dto)

    if epochs is None:
        return None

    epochs = prepare_channels(epochs, epochs_dto)
    sfreq = epochs.info["sfreq"]

    spectrum = epochs.compute_psd(
        method="welch",
        n_fft=int(max(8, sfreq * (epochs_dto.tmax - epochs_dto.tmin))),  # minimal n_fft safeguard
        n_overlap=0,
        n_per_seg=None,
        tmin=epochs_dto.tmin,
        tmax=epochs_dto.tmax,
        fmin=psd_dto.fmin,
        fmax=psd_dto.fmax,
        window="hann",
        average='mean',
        verbose=False,
    )
    psds, freqs = spectrum.get_data(return_freqs=True)
    snrs = compute_snr_spectrum(psds)

    return psds, freqs, snrs


def plot_snr(psds, freqs, snrs, session: PipelineSession):
    """Plot mean SNR spectrum with shaded variability; return finalized figure."""
    fig, axes = plt.subplots(2, 1, sharex="all", figsize=(8, 5))
    try:
        start_idx = int(np.where(np.floor(freqs) == 1.0)[0][0])
    except IndexError:
        start_idx = 0
    try:
        end_idx = int(np.where(np.ceil(freqs) == session.psd.fmax - 1)[0][0])
    except IndexError:
        end_idx = len(freqs) - 1
    if end_idx <= start_idx:
        start_idx, end_idx = 0, len(freqs) - 1
    freq_idx = range(start_idx, end_idx)
    psds_db = 10 * np.log10(psds, where=psds > 0, out=np.full_like(psds, np.nan))
    psds_mean = np.nanmean(psds_db[..., freq_idx], axis=(0, 1))
    psds_std = np.nanstd(psds_db[..., freq_idx], axis=(0, 1))
    axes[0].plot(freqs[freq_idx], psds_mean, color="b")
    axes[0].fill_between(
        freqs[freq_idx], psds_mean - psds_std, psds_mean + psds_std, color="b", alpha=0.2
    )
    axes[0].set(title="PSD spectrum", ylabel="Power Spectral Density [dB]")
    snr_mean = np.nanmean(snrs[..., freq_idx], axis=(0, 1))
    snr_std = np.nanstd(snrs[..., freq_idx], axis=(0, 1))
    axes[1].plot(freqs[freq_idx], snr_mean, color="r")
    axes[1].fill_between(
        freqs[freq_idx], snr_mean - snr_std, snr_mean + snr_std, color="r", alpha=0.2
    )
    axes[1].set(
        title="SNR spectrum",
        xlabel="Frequency [Hz]",
        ylabel="SNR",
        xlim=[session.psd.fmin, session.psd.fmax],
    )

    header = FigureHeader(
        plot_name="SNR Spectrum",
        subject_line=format_subject_label(session.task, session.epochs.stimulus),
        caption_line=str(session.epochs)
    )

    final_fig = finalize_figure(fig, header)
    return final_fig
