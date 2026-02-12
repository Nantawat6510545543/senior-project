from pydantic import BaseModel, Field
from typing import Literal, Optional


class TableParams(BaseModel):
    rows: int = Field(
        10, json_schema_extra={"ui": "integer", "group": "tables"}
    )

    table_type: Optional[Literal["events", "channels", "electrodes"]] = Field(
        "events",
        json_schema_extra={
            "ui": "list",
            "group": "tables",
            "options": ["events", "channels", "electrodes"],
        },
    )
