from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PreviewInput, StrictModel


class MembershipGrantInput(StrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    duration_days: Literal[30, 90, 365]
    reason: str = Field(min_length=5, max_length=500)


class MembershipRevokeInput(StrictModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    reason: str = Field(min_length=5, max_length=500)


class MembershipResponse(BaseModel):
    student_id: UUID
    plan_code: Literal["free", "vip"]
    status: Literal["free", "active", "expired", "revoked"]
    subscription_plan_code: str | None
    starts_at: datetime | None
    ends_at: datetime | None
    features: list[str]


class MembershipPlanResponse(BaseModel):
    code: str
    name: str
    features: list[str]


class ContentPolicyInput(StrictModel):
    minimum_plan_code: Literal["free", "vip"]
    learning_level: Literal["basic", "reinforcement", "advanced"]
    preview: PreviewInput
    reason: str = Field(min_length=5, max_length=500)
