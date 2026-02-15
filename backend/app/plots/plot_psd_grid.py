"""Grid of PSD curves per condition/label."""
import numpy as np

from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.schemas.session_schema import PipelineSession
from .grid_plot_helpers import render_label_grid
from .plot_merger import merge_figures_vertical
from .plot_snr_grid import get_epoch_psd_params


def prepare_psd_grid_data(executor: EEGTaskExecutor, session: PipelineSession):
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
    psd_cache = {}

    for label in available_labels:
        try:
            ce = prepare_channels(epochs[label], epochs_psd_dto)
            if len(ce) == 0:
                continue

            spectrum = ce.compute_psd(
                method="welch",
                n_fft=nfft,
                n_overlap=0,
                n_per_seg=None,
                tmin=epochs_psd_dto.tmin,
                tmax=epochs_psd_dto.tmax,
                fmin=epochs_psd_dto.fmin,
                fmax=epochs_psd_dto.fmax,
                window="hann",
                average="mean",
                verbose=False,
            )

            psd, freqs = spectrum.get_data(return_freqs=True)

            psd_db = 10 * np.log10(psd, where=psd > 0, out=np.full_like(psd, np.nan))
            mean = np.nanmean(psd_db, axis=(0, 1))
            std = np.nanstd(psd_db, axis=(0, 1))

            psd_cache[label] = (freqs, mean, std, len(ce))

        except Exception:
            continue

    return epochs, available_labels, psd_cache


def plot_psd_grid(epochs, available_labels, psd_cache, session: PipelineSession):
    """Render PSD spectrum per label in a grid; return figure or None."""
    epochs_psd_dto = get_epoch_psd_params(session)

    def _draw(ax, label):
        item = psd_cache.get(label)
        if item is None:
            return None

        freqs, mean, std, n = item

        ax.plot(freqs, mean, color="b")
        ax.fill_between(freqs, mean - std, mean + std, color="b", alpha=0.2)

        ax.text(
            1, 1, f"n={n}",
            transform=ax.transAxes,
            ha="right", va="bottom",
            fontsize=8, color="0.4"
        )

        return float(np.nanmin(mean)), float(np.nanmax(mean))

    rendered_fig = render_label_grid(
        task_dto=session.task,
        epochs=epochs,
        available_labels=available_labels,
        params=epochs_psd_dto,
        plot_name="PSD Grid",
        xlim=(epochs_psd_dto.fmin, epochs_psd_dto.fmax),
        xlabel="Frequency [Hz]",
        unit_tag="dB",
        per_cell_draw=_draw,
    )

    return merge_figures_vertical(rendered_fig)
