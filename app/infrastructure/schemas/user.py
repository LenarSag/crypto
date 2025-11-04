import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.domain.entities.user import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    telegram_id: int

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        password_regex = re.compile(
            r'^'
            r'(?=.*[a-z])'
            r'(?=.*[A-Z])'
            r'(?=.*\d)'
            r'(?=.*[@$!%*?&])'
            r'[A-Za-z\d@$!%*?&]'
            r'{8,}$'
        )
        if not password_regex.match(value):
            raise ValueError(
                'The length at least 8 symbols, including '
                'lower-case, upper-case, nums, '
                'and special symbols.'
            )
        return value


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    telegram_id: Optional[int] = None
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
