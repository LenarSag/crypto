from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass(frozen=True)
class Price:
    id: UUID
    coin_id: UUID
    price: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
