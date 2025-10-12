from typing import Optional

from app.domain.const.constants import KEY_EXPIRATION_SECONDS
from app.domain.entities.token import Token
from app.domain.entities.user import User
from app.domain.exceptions.token import InvalidTokenError
from app.domain.exceptions.user import (
    InactiveUserError,
    IncorrectEmailOrPasswordError,
)
from app.domain.ports.cache import ICache
from app.domain.ports.pw_hasher import PasswordHasher
from app.domain.ports.token_provider import TokenProvider
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.cache.cache_serializers import UserSerializer


class AuthService:
    """Handles authentication business logic."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_provider: TokenProvider,
        hasher: PasswordHasher,
        cache: ICache,
    ):
        self._user_repo = user_repo
        self._token_provider = token_provider
        self._hasher = hasher
        self._cache = cache

    async def authenticate_user(self, email: str, raw_password: str) -> Optional[Token]:
        """Authenticate a user and return an access token."""

        user = await self._user_repo.get_by_email(email)
        if not user or not self._hasher.verify(raw_password, user.hashed_password):
            raise IncorrectEmailOrPasswordError()

        token = self._token_provider.create_access_token(user.id)
        return token

    async def get_current_user(self, token: str) -> User:
        """Resolve user from JWT token, with caching."""

        user_id = self._token_provider.verify_token(token)
        if user_id is None:
            raise InvalidTokenError()

        cache_key = f'user:{user_id}'
        cached = await self._cache.get(cache_key)
        if cached:
            user = UserSerializer.deserialize(cached)
            if not user.is_active:
                raise InactiveUserError()
            return user

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise InvalidTokenError()

        serialized_user = UserSerializer.serialize(user)
        await self._cache.set(
            cache_key, serialized_user, expire_seconds=KEY_EXPIRATION_SECONDS
        )

        if not user.is_active:
            raise InactiveUserError()

        return user
