from typing import Optional

from app.domain.const.constants import KEY_EXPIRATION_SECONDS
from app.domain.entities.token import Token
from app.domain.entities.user import User, UserLogin
from app.domain.exceptions.token import InvalidTokenError, TokenExpiredError
from app.domain.exceptions.user import (
    InactiveUserError,
    InvalidCredentialsError,
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
        password_hasher: PasswordHasher,
        cache: ICache,
    ):
        self._user_repo = user_repo
        self._token_provider = token_provider
        self._hasher = password_hasher
        self._cache = cache

    async def authenticate_user(self, user_data: UserLogin) -> Optional[Token]:
        """Authenticate a user and return an access token."""

        user = await self._user_repo.get_by_email(user_data.email)
        if not user or not self._hasher.verify(
            user_data.password, user.hashed_password
        ):
            raise InvalidCredentialsError()

        token = self._token_provider.create_access_token(user.id)
        return Token(access_token=token, token_type='Bearer')

    async def get_current_user(self, token: str) -> User:
        """Resolve user from token, with caching."""

        try:
            user_id = self._token_provider.verify_token(token)
        except InvalidTokenError:
            raise InvalidTokenError()
        except TokenExpiredError:
            raise TokenExpiredError()

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
