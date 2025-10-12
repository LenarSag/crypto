# app/infrastructure/auth/dependencies.py
from fastapi_permissions import configure_permissions

from app.domain.entities.user import User


def get_user_permissions(user: User) -> list[str]:
    return user.permissions


def get_user_roles(user: User) -> list[str]:
    return [user.role.value]


Permission = configure_permissions(lambda: ..., get_user_permissions, get_user_roles)
