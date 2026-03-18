from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.params.psd_filter_schema import EpochPSDParams


class TrainingParams(BaseModel):
    epochs_psd: EpochPSDParams = Field(default_factory=EpochPSDParams)

    batch_size: int = Field(
        32,
        title="batch_size",
        json_schema_extra={
            "ui": "integer",
            "group": "training",
        },
    )

    epochs_n: int = Field(
        50,
        title="epochs_n",
        json_schema_extra={
            "ui": "integer",
            "group": "training",
        },
    )

    lr: float = Field(
        0.001,
        title="lr",
        json_schema_extra={
            "ui": "number",
            "group": "training",
        },
    )

    val_split: float = Field(
        0.2,
        title="val_split",
        json_schema_extra={
            "ui": "number",
            "group": "training",
        },
    )

    test_split: float = Field(
        0.2,
        title="test_split",
        json_schema_extra={
            "ui": "number",
            "group": "training",
        },
    )

    seed: int = Field(
        42,
        title="seed",
        json_schema_extra={
            "ui": "integer",
            "group": "training",
        },
    )

    patience: int = Field(
        0,
        title="patience",
        json_schema_extra={
            "ui": "integer",
            "group": "training",
        },
    )

    train: Literal["epoch", "evoked", "psd"] = Field(
        "epoch",
        title="train",
        json_schema_extra={
            "ui": "list",
            "group": "training",
            "options": ["epoch", "evoked", "psd"],
        },
    )

    target: Literal[
                "ccd_accuracy",
                "ccd_response_time",
                "stimulus",
                "ccd_accuracy + ccd_response_time"
            ] = Field(
        "ccd_accuracy",
        title="target",
        json_schema_extra={
            "ui": "list",
            "group": "training",
            "options": [
                "ccd_accuracy",
                "ccd_response_time",
                "stimulus",
                "ccd_accuracy + ccd_response_time"
            ],
        },
    )

    device: Literal["auto", "cpu", "cuda"] = Field(
        "auto",
        title="device",
        json_schema_extra={
            "ui": "list",
            "group": "training",
            "options": ["auto", "cpu", "cuda"],
        },
    )

    save_checkpoint: bool = Field(
        True,
        title="save_checkpoint",
        json_schema_extra={
            "ui": "checkbox",
            "group": "training",
        },
    )

    weight_classes: bool = Field(
        False,
        title="weight_classes",
        json_schema_extra={
            "ui": "checkbox",
            "group": "training",
        },
    )
