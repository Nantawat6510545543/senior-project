from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_executor import EEGTaskExecutor
from app.plots.figure_header import FigureHeader, format_caption_label, format_subject_label
from app.plots.plot_finalizer import finalize_figure
from app.schemas.session_schema import PipelineSession


def prepare_evoked_joint_plot_data(executor: EEGTaskExecutor, session: PipelineSession):
    session_updated = session.model_copy(
        update={
            "filter": session.filter.model_copy(update={"combine_channels": False})
        }
    )

    evoked = executor.get_evoked(session_updated)

    if evoked is None:
        return None

    evoked_joint = prepare_channels(evoked, session_updated.filter)
    return evoked_joint


def plot_evoked_joint(evoked_joint, session: PipelineSession):
    """Plot joint time course + topomap panels; return finalized figure."""
    evoked_joint_dto = session.evoked_joint

    fig = evoked_joint.plot_joint(
        times=evoked_joint_dto.resolved_times,
        topomap_args={},
        ts_args={"gfp": evoked_joint_dto.gfp, "spatial_colors": evoked_joint_dto.spatial_colors},
        show=False
    )

    header = FigureHeader(
        plot_name="Evoked Joint",
        subject_line=format_subject_label(session),
        caption_line=format_caption_label(session.filter, session.epochs, evoked_joint_dto)
    )

    return finalize_figure(fig, header)
