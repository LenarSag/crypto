from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class Coin:
    id: UUID
    ticker: str
    name: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
