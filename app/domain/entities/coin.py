from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID


@dataclass
class Coin:
    """Coin entity"""

    id: UUID
    ticker: str
    name: str
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    price: Optional[float] = None


@dataclass
class CoinUpdate:
    """Data class for coin updates"""

    name: Optional[str] = None
    description: Optional[str] = None

    def to_update_dict(self) -> dict[str, Any]:
        """Convert to update dictionary"""

        update_dict = {}

        for class_field in fields(self):
            value = getattr(self, class_field.name)
            if value is not None:
                update_dict[class_field.name] = value

        return update_dict
