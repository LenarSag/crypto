from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from app.domain.ports.pw_hasher import PasswordHasher


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


@dataclass
class User:
    """User entity"""

    id: UUID
    username: str
    email: str
    hashed_password: str
    telegram_id: Optional[int]
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class UserUpdate:
    """Data class for user updates"""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    telegram_id: Optional[int] = None

    def to_update_dict(self, password_hasher: PasswordHasher) -> dict[str, Any]:
        """Convert to update dictionary"""

        update_dict = {}

        for class_field in fields(self):
            value = getattr(self, class_field.name)
            if value is not None:
                if class_field.name == 'password' and password_hasher:
                    update_dict['hashed_password'] = password_hasher.hash(value)
                else:
                    update_dict[class_field.name] = value

        return update_dict
