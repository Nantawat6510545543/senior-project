from app.core.config import DATA_ROOT
from app.pipeline.channels_helper import prepare_channels
from app.pipeline.task_resolver import EEGTaskResolver
from app.plots.plot_finalizer import FigureHeader, finalize_figure, format_subject_label
from app.schemas.params.evoked_filter_schema import EvokedJointParams
from app.schemas.session_schema import PipelineSession


# def plot_evoked_per_condition(self, task_dto: BaseTaskDTO, params: EvokedParamsDTO):
#     """Return list of evoked figures, one per available condition/label."""
#     import copy as _copy

#     epochs, labels = self.get_epochs(task_dto, params)
#     if epochs is None:
#         return None
#     fig_list = []
#     for condition in epochs.event_id:
#         copy_params = _copy.deepcopy(params)
#         copy_params.stimulus = condition
#         evk = self.get_evoked(task_dto, copy_params)
#         if evk is None:
#             continue
#         evk = prepare_channels(evk, copy_params)
#         fig = evk.plot(gfp=copy_params.gfp, spatial_colors=copy_params.spatial_colors, show=False)
#         fig = finalize_figure(
#             fig,
#             task_dto,
#             condition,
#             caption_line=str(copy_params),
#             plot_name="Evoked per Condition",
#         )
#         fig_list.append(fig)
#     return fig_list
