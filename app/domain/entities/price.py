from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass()
class Price:
    id: UUID
    coin_id: UUID
    price: float
    timestamp: Optional[datetime]
