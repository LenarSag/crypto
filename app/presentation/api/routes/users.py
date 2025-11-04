from fastapi import APIRouter, Depends, status

from app.domain.services.user_service import UserService
from app.infrastructure.schemas.user import UserCreate, UserResponse
from app.presentation.dependencies.deps import get_user_service

user_router = APIRouter()


@user_router.get('/login')
async def login():
    pass


@user_router.get('/{user_id}')
async def get_user():
    pass


@user_router.get('/')
async def list_users():
    pass


@user_router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        telegram_id=user_data.telegram_id,
    )

    return user


@user_router.patch('/{user_id}')
async def update_user():
    pass


@user_router.delete('/{user_id}/soft')
async def soft_delete_user():
    pass


@user_router.delete('/{user_id}')
async def delete_user():
    pass
