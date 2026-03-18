from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, Optional

from app.schemas.task_schema import SingleSubjectTask


@dataclass(slots=True)
class FigureHeader:
    plot_name: str
    subject_line: Optional[str] = None
    caption_line: Optional[str] = None


def format_subject_label(task: SingleSubjectTask, stimulus: str = None) -> str:
    """Human readable subject line for figure headers."""
    if stimulus:
        return f"{task} - {stimulus}"
    return str(task)

def format_caption_label(*models: Any, as_str: bool = True) -> Any:
    """
    Returns a combined dict of all active fields from one or more Pydantic models.
    Active fields = non-default and non-None.

    If as_str=True, returns a formatted string like "field1=val1, field2=val2".
    """
    combined = {}
    for model in models:
        if not isinstance(model, BaseModel):
            raise TypeError(f"Expected Pydantic BaseModel, got {type(model)}")
        data = model.model_dump(exclude_none=True)

        # Remove False values
        data = {k: v for k, v in data.items() if v is not False}
        combined.update(data)

    if as_str:
        # Convert dict to a single-line string
        return ", ".join(f"{k}={v}" for k, v in combined.items())

    return combined
