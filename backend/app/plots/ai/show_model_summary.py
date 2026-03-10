"""Model summary action (parameter counts and layer outputs)."""
from typing import Callable

from app.pipeline.task_executor import EEGTaskExecutor
from app.pipeline.trainer_data_builder import build_epoch_dataset
from app.schemas.session_schema import PipelineSession
from app.ai_models.EEGNetMultiReg import EEGNetMultiReg

def prepare_model_summary_data(
        executor: EEGTaskExecutor,
        session: PipelineSession,
        get_subjects_metadata: Callable    
    ):
    """Return a torchinfo-style textual summary for EEGNetMultiReg."""
    X, y_raw, meta = build_epoch_dataset(executor, session, get_subjects_metadata)

    if X is None:
        return [{"status": meta.get("reason", "unavailable")}]
    n_e, n_c, n_t = X.shape
    model = EEGNetMultiReg(n_outputs=1)
    input_size = (1, n_c, n_t)  # batch=1 for summary

    # torchinfo may not be installed; try import lazily here
    try:
        # TODO full implement
        from torchinfo import summary as torchinfo_summary  # type: ignore
        info = torchinfo_summary(
            model,
            input_size=input_size,
            col_names=("output_size", "num_params"),
            verbose=0
        )

        rows = []
        for layer in info.summary_list:
            rows.append({
                "Layer": layer.class_name,
                "Output Shape": list(layer.output_size),
                "Params": layer.num_params
            })

        # summary rows
        rows.append({
            "Layer": "",
            "Output Shape": "",
            "Params": ""
        })

        rows.append({
            "Layer": "TOTAL PARAMS",
            "Output Shape": "",
            "Params": info.total_params
        })

        rows.append({
            "Layer": "TRAINABLE PARAMS",
            "Output Shape": "",
            "Params": info.trainable_params
        })

        rows.append({
            "Layer": "NON-TRAINABLE PARAMS",
            "Output Shape": "",
            "Params": info.total_params - info.trainable_params
        })

        rows.append({
            "Layer": "TOTAL MULT-ADDS (M)",
            "Output Shape": "",
            "Params": round(info.total_mult_adds / 1e6, 2)
        })

        rows.append({
            "Layer": "INPUT SIZE (MB)",
            "Output Shape": "",
            "Params": round(info.total_input / 1e6, 2)
        })

        rows.append({
            "Layer": "FWD/BWD SIZE (MB)",
            "Output Shape": "",
            "Params": round(info.total_output_bytes / 1e6, 2)
        })

        rows.append({
            "Layer": "PARAM SIZE (MB)",
            "Output Shape": "",
            "Params": round(info.total_param_bytes / 1e6, 2)
        })

        return rows

    except ImportError:
        raise RuntimeError("torchinfo is not installed")
