from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


Grade = Annotated[int, Field(ge=1, le=5)]
TextSize = Literal["compact", "comfortable", "large"]
DeviceType = Literal["phone", "tablet", "desktop"]


class ReadingPreferences(BaseModel):
    text_size: TextSize = "comfortable"
    text_size_by_device: dict[DeviceType, TextSize] = Field(default_factory=dict)


class PreviewInput(StrictModel):
    summary: str = Field(default="", max_length=350)
    goals: list[Annotated[str, Field(max_length=120)]] = Field(default_factory=list, max_length=5)


class CatalogAccess(BaseModel):
    minimum_plan_code: Literal["free", "vip"] | None = None
    learning_level: Literal["basic", "reinforcement", "advanced"] = "basic"
    locked: bool = False
    lock_reason: str | None = None
