from app.core.config import DATA_ROOT
from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_resolver import EEGTaskResolver
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.params.evoked_filter_schema import EvokedJointParams
from app.schemas.session_schema import PipelineSession


# TODO fix inheritance hell
def get_evoked_joint_params(session: PipelineSession):
    evoked_dict = session.evoked.model_dump()

    topo_dict = session.topomap.model_copy(
        update={"combine_channels": False}
    ).model_dump()

    # remove overlapping keys from topo
    for k in evoked_dict.keys():
        topo_dict.pop(k, None)

    evoked_joint_dto = EvokedJointParams(**evoked_dict, **topo_dict)
    return evoked_joint_dto


def prepare_evoked_joint_plot_data(session: PipelineSession):
    evoked_joint_dto = get_evoked_joint_params(session)

    resolver = EEGTaskResolver(DATA_ROOT)
    executor = resolver.resolve_task(session.task)
    evoked = executor.get_evoked(evoked_joint_dto)

    if evoked is None:
        return None

    evoked_joint = prepare_channels(evoked, evoked_joint_dto)
    return evoked_joint


def plot_evoked_joint(evoked_joint, session: PipelineSession):
    """Plot joint time course + topomap panels; return finalized figure."""
    evoked_joint_dto = get_evoked_joint_params(session)

    fig = evoked_joint.plot_joint(
        times=evoked_joint_dto.resolved_times,
        topomap_args={},
        ts_args={"gfp": evoked_joint_dto.gfp, "spatial_colors": evoked_joint_dto.spatial_colors},
        show=False,
    )

    header = FigureHeader(
        plot_name="Evoked Joint",
        subject_line=format_subject_label(session.task, evoked_joint_dto.stimulus),
        caption_line=str(evoked_joint_dto)
    )

    return finalize_figure(fig, header)
