from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.subscription import ComparisonOperator


class SubscriptionCreate(BaseModel):
    user_id: UUID
    coin_id: UUID
    threshold_value: Optional[int]
    comparison_operator: Optional[ComparisonOperator]


class SubscriptionUpdate(BaseModel):
    threshold_value: Optional[int]
    comparison_operator: Optional[ComparisonOperator]
    is_active: Optional[bool]


class SubscriptionResponse(SubscriptionCreate):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
