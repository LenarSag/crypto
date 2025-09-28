from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID


class ComparisonOperator(Enum):
    GREATER_THAN = '>'
    LESS_THAN = '<'


@dataclass
class Subscription:
    id: int
    user_id: UUID
    coin_id: UUID
    threshold_value: float
    comparison_operator: ComparisonOperator
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
