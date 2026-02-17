FILTER_SHARED_KEYS = [
    "l_freq","h_freq","notch","resample_fs","channels","combine_channels",
    "uv_min","uv_max","clean_flatline_sec","clean_hf_noise_sd_max",
    "clean_corr_min","clean_asr_max_std","clean_power_min_sd",
    "clean_power_max_sd","clean_max_outbound_pct","clean_window_sec",
    "clean_asr_remove_only",
]

CHILD_SCHEMAS = ["epochs","time","psd","evoked","topomap","table"]


def normalize_session(session):
    base = session.filter
    base_dict = base.model_dump()

    for name in CHILD_SCHEMAS:
        child = getattr(session, name, None)
        if child is None:
            continue

        child_dict = child.model_dump()

        for key in FILTER_SHARED_KEYS:
            child_dict[key] = base_dict[key]

        setattr(session, name, type(child)(**child_dict))

    return session
