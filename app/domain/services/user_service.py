from typing import Optional
from uuid import UUID, uuid4

from app.domain.entities.token import Token
from app.domain.entities.user import User, UserRole
from app.domain.exceptions.user import (
    EmailAlreadyExistsError,
    IncorrectEmailOrPasswordError,
    UserNotFoundError,
)
from app.domain.ports.pw_hasher import PasswordHasher
from app.domain.ports.token_provider import TokenProvider
from app.domain.repositories.user_repo import IUserRepository


class UserService:
    """Business use-cases for managing users."""

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
    ):
        """:param user_repo: abstraction for persistence (implements IUserRepository)
        :param password_hasher: callable or adapter with hash() / verify() methods
        """

        self._repo = user_repo
        self._hasher = password_hasher
        self._token_provider = token_provider

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

    async def login(self, email: str, password: str) -> Optional[Token]:
        """Authenticate a user and return both the user and an access token.
        Raises IncorrectEmailOrPasswordError if credentials are invalid.
        """

        user = await self._repo.get_by_email(email)
        if not user or not self._hasher.verify(password, user.hashed_password):
            raise IncorrectEmailOrPasswordError()

        token = self._token_provider.create_access_token(user.id)
        return token

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Retrieve a user by ID for API endpoints.
        Raises UserNotFoundError if not found.
        """

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def list_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        """List users with pagination."""

        return await self._repo.list_users(offset=offset, limit=limit)

    async def update_user(
        self,
        user_id: UUID,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        telegram_id: Optional[int] = None,
    ) -> None:
        """Update user fields. Only non-None parameters will be updated.
        Raises UserNotFoundError if the user does not exist.
        Raises EmailAlreadyExistsError if the new email is already taken.
        """

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        if email and email != user.email:
            existing = await self._repo.get_by_email(email)
            if existing:
                raise EmailAlreadyExistsError(email)
            user.email = email

        if username is not None:
            user.username = username
        if password is not None:
            user.hashed_password = self._hasher.hash(password)
        if telegram_id is not None:
            user.telegram_id = telegram_id

        await self._repo.update(user)

    async def deactivate_user(self, user_id: UUID):
        """Soft delete: mark user as inactive."""

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        await self._repo.soft_delete(user_id)

    async def delete_user(self, user_id: UUID):
        """Permanent deletion: remove user from storage."""

        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        await self._repo.delete_permanently(user_id)
