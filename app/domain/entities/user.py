from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


@dataclass
class User:
    id: UUID
    username: str
    email: str
    hashed_password: str
    telegram_id: Optional[int]
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
