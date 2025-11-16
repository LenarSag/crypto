from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.token import InvalidTokenError, TokenExpiredError
from app.domain.exceptions.user import InactiveUserError
from app.domain.services.auth_service import AuthService
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.db.database import get_session
from app.infrastructure.exceptions.token_exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)
from app.infrastructure.exceptions.user_exceptions import InactiveUserException
from app.infrastructure.repositories.user_repo_impl import SQLAlchemyUserRepository
from app.infrastructure.security.jwt_token import JWTTokenProvider
from app.infrastructure.security.password import BCryptPasswordHasher


async def get_auth_service(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    user_repo = SQLAlchemyUserRepository(session)
    password_hasher = BCryptPasswordHasher()
    token_provider = JWTTokenProvider()
    cache = RedisCache(request.app.state.redis)

    return AuthService(
        user_repo=user_repo,
        password_hasher=password_hasher,
        token_provider=token_provider,
        cache=cache,
    )


async def resolve_current_user(
    request: Request, auth_service: AuthService = Depends(get_auth_service)
):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise InvalidTokenException()

    token = auth_header.removeprefix('Bearer ').strip()

    try:
        current_user = await auth_service.get_current_user(token)
    except InvalidTokenError:
        raise InvalidTokenException()
    except TokenExpiredError:
        raise TokenExpiredException()
    except InactiveUserError:
        raise InactiveUserException()

    return current_user


def require_roles(*roles: str):
    async def role_checker(
        current_user=Depends(resolve_current_user),
    ):
        if roles and current_user.role not in roles:
            raise InvalidTokenException()
        return current_user

    return role_checker


def require_same_user(param_name: str = 'user_id'):
    async def checker(
        request: Request,
        current_user=Depends(resolve_current_user),
    ):
        requested_id = request.path_params.get(param_name)
        if str(current_user.id) != str(requested_id):
            raise InvalidTokenException()
        return current_user

    return checker


def require_role_or_owner(*roles: str, param_name: str = 'user_id'):
    async def checker(
        request: Request,
        current_user=Depends(resolve_current_user),
    ):
        requested_id = request.path_params.get(param_name)

        is_role_allowed = current_user.role in roles
        is_owner = str(current_user.id) == str(requested_id)

        if not (is_role_allowed or is_owner):
            raise InvalidTokenException()

        return current_user

    return checker
