"""Grid of SNR spectra per condition/label."""
import numpy as np

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.signal_spatial import compute_snr_spectrum
from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession
from app.schemas.params.psd_filter_schema import EpochPSDParams
from .grid_plot_helpers import render_label_grid
from .plot_merger import merge_figures_vertical


# TODO move asap
def get_epoch_psd_params(session: PipelineSession) -> EpochPSDParams:
    epoch_dict = session.epochs.model_dump()
    psd_dict = session.psd.model_dump()

    # remove overlapping keys from psd
    for k in epoch_dict.keys():
        psd_dict.pop(k, None)

    epochs_psd_dto = EpochPSDParams(**epoch_dict, **psd_dict)
    return epochs_psd_dto


def prepare_snr_grid_data(executor: EEGTaskExecutor, session: PipelineSession):
    epochs_psd_dto = get_epoch_psd_params(session)
    epochs, available_labels = executor.get_epochs(epochs_psd_dto)
    if epochs is None:
        return None

    sfreq = float(epochs.info.get("sfreq", 0.0))
    duration = (
        (epochs_psd_dto.tmax - epochs_psd_dto.tmin)
        if (epochs_psd_dto.tmax is not None and epochs_psd_dto.tmin is not None)
        else 1.0
    )
    nfft = int(max(8, sfreq * max(0.5, duration)))

    # ---- precompute once per label ----
    snr_cache = {}

    for label in available_labels:
        try:
            ce = prepare_channels(epochs[label], epochs_psd_dto)
            if len(ce) == 0:
                continue

            spectrum = ce.compute_psd(
                method="welch",
                n_fft=nfft,
                tmin=epochs_psd_dto.tmin,
                tmax=epochs_psd_dto.tmax,
                fmin=epochs_psd_dto.fmin,
                fmax=epochs_psd_dto.fmax,
                window="hann",
                average="mean",
                verbose=False,
            )

            psd, freqs = spectrum.get_data(return_freqs=True)
            snr = compute_snr_spectrum(psd)

            mean = np.nanmean(snr, axis=(0, 1))
            std = np.nanstd(snr, axis=(0, 1))

            snr_cache[label] = (freqs, mean, std, len(ce))

        except Exception:
            continue

    return epochs, available_labels, snr_cache


# TODO fix dto type (EpochPSD)
def plot_snr_grid(epochs, available_labels, snr_cache, session: PipelineSession):
    """Render SNR spectrum per label in a grid; return figure or None."""
    epochs_psd_dto = get_epoch_psd_params(session)

    def _draw(ax, label):
        item = snr_cache.get(label)
        if item is None:
            return None

        freqs, mean, std, n = item

        ax.plot(freqs, mean, color="r")
        ax.fill_between(freqs, mean - std, mean + std, color="r", alpha=0.2)

        ax.text(1, 1, f"n={n}",
                transform=ax.transAxes,
                ha="right", va="bottom",
                fontsize=8, color="0.4")

        return float(np.nanmin(mean)), float(np.nanmax(mean))

    rendered_fig = render_label_grid(
        task_dto=session.task,
        epochs=epochs,
        available_labels=available_labels,
        params=epochs_psd_dto,
        plot_name="SNR Grid",
        xlim=(epochs_psd_dto.fmin, epochs_psd_dto.fmax),
        xlabel="Frequency [Hz]",
        unit_tag="SNR",
        per_cell_draw=_draw,
    )

    return merge_figures_vertical(rendered_fig)
