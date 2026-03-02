from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class RangeFilter(BaseModel):
    min: Optional[float] = Field(
        None,
        json_schema_extra={"ui": "number", "placeholder": "min"},
    )
    max: Optional[float] = Field(
        None,
        json_schema_extra={"ui": "number", "placeholder": "max"},
    )

class SubjectFilterParams(BaseModel):
    task: Optional[str] = Field(
        None,
        json_schema_extra={
            "ui": "select",
            "group": "subject_filter",
        },
    )

    subject_limit: Optional[int] = Field(
        None,
        json_schema_extra={
            "ui": "number",
            "group": "subject_filter",
            "placeholder": "e.g. 50",
        },
    )

    per_subject: bool = Field(
        False,
        json_schema_extra={
            "ui": "checkbox",
            "group": "subject_filter",
        },
    )

    sex: Optional[Literal["None", "M", "F"]] = Field(
        "None",
        validate_default=True,
        json_schema_extra={
            "ui": "list",
            "group": "subject_filter",
            "options": ["None", "M", "F"]
        },
    )

    # Convert "none" to None
    @field_validator("sex", mode="before")
    @classmethod
    def normalize_none(cls, v):
        return None if v == "None" else v

    # ---------- Range Filters ----------
    age: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "unit": "years",
            "group": "subject_filter",
        },
    )

    ehq_total: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "group": "subject_filter",
        },
    )

    p_factor: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "group": "subject_filter",
        },
    )

    attention: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "group": "subject_filter",
        },
    )

    internalizing: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "group": "subject_filter",
        },
    )

    externalizing: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "group": "subject_filter",
        },
    )

    ccd_accuracy: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "unit": "%",
            "group": "subject_filter",
        },
    )

    ccd_response_time: Optional[RangeFilter] = Field(
        None,
        json_schema_extra={
            "ui": "range",
            "unit": "ms",
            "group": "subject_filter",
        },
    )
