from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.domain.const.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from app.domain.exceptions.user import EmailAlreadyExistsError, InvalidCredentialsError
from app.domain.services.auth_service import AuthService
from app.domain.services.user_service import UserService
from app.infrastructure.exceptions.token_exceptions import InvalidTokenException
from app.infrastructure.exceptions.user_exceptions import EmailAlreadyExistsException
from app.infrastructure.schemas.token import TokenResponse
from app.infrastructure.schemas.user import UserCreate, UserLoginData, UserResponse
from app.presentation.dependencies.auth import (
    get_auth_service,
    require_role_or_owner,
    require_roles,
)
from app.presentation.dependencies.user import get_user_service

user_router = APIRouter()


@user_router.post(
    '/login', response_model=TokenResponse, status_code=status.HTTP_200_OK
)
async def login(
    user_login_data: UserLoginData,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = await auth_service.authenticate_user(user_login_data)
    except InvalidCredentialsError:
        raise InvalidTokenException()

    return token


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: UUID,
    _=Depends(require_role_or_owner('admin')),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_by_id(user_id)


@user_router.get('/', response_model=UserResponse)
async def list_users(
    _=Depends(require_roles('admin')),
    user_service: UserService = Depends(get_user_service),
    offset: int = Query(DEFAULT_OFFSET),
    limit: int = Query(DEFAULT_LIMIT),
):
    return await user_service.list_users(offset=offset, limit=limit)


@user_router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            telegram_id=user_data.telegram_id,
        )
        return user

    except EmailAlreadyExistsError:
        raise EmailAlreadyExistsException(user_data.email)


@user_router.patch('/{user_id}')
async def update_user():
    pass


@user_router.delete('/{user_id}/soft')
async def soft_delete_user():
    pass


@user_router.delete('/{user_id}')
async def delete_user():
    pass
