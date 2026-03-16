from app.schemas.session_schema import PipelineSession


def get_filter_key(session: PipelineSession) -> dict[str, float | None]:
    return {
        "l_freq": session.filter.l_freq,
        "h_freq": session.filter.h_freq,
        "notch": session.filter.notch,
        "resample_fs": session.filter.resample_fs,
    }


def get_cleaning_key(session: PipelineSession) -> dict[str, float | bool]:
    key = get_filter_key(session)
    for name in (
        "clean_flatline_sec",
        "clean_hf_noise_sd_max",
        "clean_corr_min",
        "clean_asr_max_std",
        "clean_power_min_sd",
        "clean_power_max_sd",
        "clean_max_outbound_pct",
        "clean_window_sec",
    ):
        val = getattr(session.filter, name)
        if val is not None:
            key[name] = val

    if session.filter.clean_asr_remove_only:
        key["clean_asr_remove_only"] = True

    return key

def get_epochs_key(session: PipelineSession):
    return {
        **get_cleaning_key(session),
        "tmin": session.epochs.tmin,
        "tmax": session.epochs.tmax,
    }

def get_evoked_key(session: PipelineSession):
    return {
        **get_epochs_key(session),
        "stimulus": session.epochs.stimulus,
    }
