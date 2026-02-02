from pydantic import Field
from .base_filter_schema import FilterParams


class TableParams(FilterParams):
    table_type: list[str] = Field(
        "electrodes",
        json_schema_extra={
            "ui": "list",
            "group": "tables",
            "options": ["events", "channels", "electrodes"],
        },
    )
    rows: int = Field(
        10, json_schema_extra={"ui": "number", "group": "tables"}
    )