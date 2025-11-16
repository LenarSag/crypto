from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class ComparisonOperator(Enum):
    GREATER_THAN = '>'
    LESS_THAN = '<'


@dataclass
class Subscription:
    id: UUID
    user_id: UUID
    coin_id: UUID
    threshold_value: Optional[float] = None
    comparison_operator: Optional[ComparisonOperator] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class SubscriptionUpdate:
    """Data class for subscription update."""

    threshold_value: Optional[float] = None
    comparison_operator: Optional[ComparisonOperator] = None
    is_active: Optional[bool] = None

    def to_update_dict(self):
        """Convert to update dictionary."""

        update_dict = {}

        for class_field in fields(self):
            value = getattr(self, class_field.name)
            if value is not None:
                update_dict[class_field.name] = value

        return update_dict
