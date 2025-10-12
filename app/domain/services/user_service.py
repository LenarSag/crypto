from typing import Optional
from uuid import UUID, uuid4

from app.domain.const.constants import KEY_EXPIRATION_SECONDS
from app.domain.entities.user import User, UserRole, UserUpdate
from app.domain.exceptions.user import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from app.domain.ports.cache import ICache
from app.domain.ports.pw_hasher import PasswordHasher
from app.domain.ports.token_provider import TokenProvider
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.cache.cache_serializers import UserSerializer


class UserService:
    """Business use-cases for managing users."""

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
        cache: ICache,
    ):
        self._repo = user_repo
        self._hasher = password_hasher
        self._token_provider = token_provider
        self._cache = cache

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        telegram_id: Optional[int] = None,
    ) -> User:
        """Create a new user with a hashed password and default values."""

        existing = await self._repo.get_by_email(email)
        if existing:
            raise EmailAlreadyExistsError(email)

        hashed_pw = self._hasher.hash(password)

        user = User(
            id=uuid4(),
            username=username,
            email=email,
            hashed_password=hashed_pw,
            telegram_id=telegram_id,
            role=UserRole.USER,
            is_active=True,
        )
        await self._repo.add(user)
        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Retrieve a user by ID."""

        cache_key = f'user:{user_id}'
        cached = await self._cache.get(cache_key)
        if cached:
            return UserSerializer.deserialize(cached)

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        serialized_user = UserSerializer.serialize(user)
        await self._cache.set(
            cache_key, serialized_user, expire_seconds=KEY_EXPIRATION_SECONDS
        )

        return user

    async def list_users(self, offset: int, limit: int) -> list[User]:
        """List users with pagination."""

        return await self._repo.list_users(offset=offset, limit=limit)

    async def update_user(self, user_id: UUID, update_data: UserUpdate) -> User:
        """Update user fields. Only non-None parameters will be updated."""

        user_to_update = await self._repo.get_by_id(user_id)
        if not user_to_update:
            raise UserNotFoundError()

        if update_data.email and update_data.email != user_to_update.email:
            existing_user = await self._repo.get_by_email(update_data.email)
            if existing_user and existing_user.id != user_id:
                raise EmailAlreadyExistsError(update_data.email)

        values_to_update = update_data.to_update_dict(self._hasher)

        updated_user = await self._repo.update(user_id, values_to_update)
        await self._cache.delete(f'user:{user_id}')

        return updated_user

    async def deactivate_user(self, user_id: UUID) -> None:
        """Soft delete: mark user as inactive."""

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        await self._repo.soft_delete(user_id)
        await self._cache.delete(f'user:{user_id}')

    async def delete_user(self, user_id: UUID):
        """Permanent deletion: remove user from storage."""

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        await self._repo.delete_permanently(user_id)
        await self._cache.delete(f'user:{user_id}')
