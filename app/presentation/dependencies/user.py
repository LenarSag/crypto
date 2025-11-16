from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services.user_service import UserService
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.user_repo_impl import SQLAlchemyUserRepository
from app.infrastructure.security.password import BCryptPasswordHasher


async def get_user_service(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> UserService:
    user_repo = SQLAlchemyUserRepository(session)
    password_hasher = BCryptPasswordHasher()
    cache = RedisCache(request.app.state.redis)

    return UserService(
        user_repo=user_repo,
        password_hasher=password_hasher,
        cache=cache,
    )
