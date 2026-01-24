from app.pipeline.eeg_pipeline import EEGPipeline
from app.rendering.render_time_plot import render_time_plot

def build_pipeline(raw, req: PlotRequest) -> EEGPipeline:
    p = EEGPipeline(raw)

    chs = parse_channels(req.channels)
    p.select_channels(chs)

    p.filter(req.l_freq, req.h_freq)
    p.notch(req.notch)
    p.resample(req.resample_fs)

    p.apply_cleaning(
        req.clean_flatline_sec,
        req.clean_hf_noise_sd_max,
    )

    p.apply_asr(req.asr_remove_only)

    if req.show_bad:
        bads = detect_bads(p.raw)
        p.mark_bads(bads)

    return p


def plot_time_service(req):
    raw = load_raw()
    # pipeline = build_pipeline(raw, req)
    image = render_time_plot(pipeline.raw)
    return {"image": image}
