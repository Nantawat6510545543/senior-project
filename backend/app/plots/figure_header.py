from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, Optional

from app.schemas.params.subject_filter_schema import RangeFilter
from app.schemas.session_schema import PipelineSession


@dataclass(slots=True)
class FigureHeader:
    plot_name: str
    subject_line: Optional[str] = None
    caption_line: Optional[str] = None


def format_subject_label(
    session: 'PipelineSession',
    stimulus: Optional[str] = None
) -> Optional[str]:
    """
    Build a human-readable label for figure headers using PipelineSession.

    - 'single' subject_type: uses str(session.task)
    - 'cohort' subject_type: dynamically includes all non-None fields from session.subject_filter
    - Stimulus is either passed or derived from session.epochs.stimulus
    - Returns None if session.task / subject_filter.task is missing
    """
    if session.subject_type == "single":
        if not session.task or not getattr(session.task, "task", None):
            return None
        task_str = str(session.task)

    elif session.subject_type == "cohort":
        sf = session.subject_filter
        if not sf or not sf.task:
            return None

        parts = [f"Task={sf.task}"]

        # Subject limit
        subject_limit = getattr(sf, "subject_limit", None)
        parts.append(f"(Total: {subject_limit if subject_limit is not None else 'All'} subjects)")

        # Iterate over all other fields
        for field_name, value in sf:
            if field_name in {"task", "subject_limit"}:
                continue

            # Handle RangeFilter fields
            if isinstance(value, RangeFilter):
                min_val = value.min
                max_val = value.max
                if min_val is None and max_val is None:
                    continue  # skip empty ranges
                parts.append(f"{field_name}={min_val if min_val is not None else ''}-{max_val if max_val is not None else ''}")

            # Skip None values (including normalized sex)
            elif value is not None:
                parts.append(f"{field_name}={value}")

        task_str = ", ".join(parts)

    else:
        return None

    # Add stimulus if available
    stimulus = stimulus or getattr(session.epochs, 'stimulus', None)
    if stimulus:
        return f"{task_str} - {stimulus}"

    return task_str


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
