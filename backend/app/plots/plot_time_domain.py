from app.pipeline.channels_helper import prepare_channels
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.plots.plot_sensors import build_raw_from_sst


def prepare_time_domain_plot_data(session):
    raw = build_raw_from_sst(session)
    time_dto = session.time
    channels_prepared_raw = prepare_channels(raw, time_dto)
    return channels_prepared_raw

def plot_time_domain(channels_prepared_raw, session):
    time_domain_dto = session.time

    old_fig = channels_prepared_raw.plot(
        duration=time_domain_dto.duration,
        start=time_domain_dto.start,
        n_channels=time_domain_dto.n_channels,
        scalings='auto',
        show=False,
    )

    header = FigureHeader(
        plot_name="Time Domain",
        subject_line=format_subject_label(session.task),
        caption_line=str(time_domain_dto)
    )

    fig = finalize_figure(old_fig, header)
    return fig