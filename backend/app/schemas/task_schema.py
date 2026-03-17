from pydantic import BaseModel, model_validator
from typing import Optional


class SingleSubjectTask(BaseModel):
    task: Optional[str] = None
    subject: Optional[str] = None
    run: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def parse_task_value(cls, data):
        """Parse a UI-encoded task string (e.g., 'task|run=2') into (task, run)."""
        task_value = data.get("task")

        # Only handle encoded strings like "task|run=2"
        if not isinstance(task_value, str):
            return data

        if "|" not in task_value:
            return data

        # Split into parts
        parts = task_value.split("|")

        # First part is always the task name
        data["task"] = parts[0]

        # Parse optional parameters
        for part in parts[1:]:
            if part.startswith("run="):
                run_str = part.split("=")[1]
                data["run"] = int(run_str)

        return data
