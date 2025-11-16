from typing import Optional, Sequence, Union
from uuid import UUID

from sqlalchemy import delete, func
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.user import User
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.models.users import User as UserModel


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user: User) -> User:
        user_model = UserMapper.to_model(user)
        self._session.add(user_model)
        await self._session.commit()
        return user

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(UserModel).filter_by(id=user_id)
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model:
            return UserMapper.to_entity(user_model)
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).filter_by(email=email)
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model:
            return UserMapper.to_entity(user_model)
        return None

    async def list_users(
        self,
        offset: int,
        limit: int,
    ) -> dict[str, Union[int, Sequence[User]]]:
        total_stmt = (
            select(func.count()).select_from(UserModel).where(UserModel.is_active)
        )
        total_result = await self._session.execute(total_stmt)
        total = total_result.scalar_one()

        stmt = select(UserModel).where(UserModel.is_active).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        user_models = result.scalars().all()
        users_list = [UserMapper.to_entity(user_model) for user_model in user_models]
        return {
            'users': users_list,
            'total': total,
            'offset': offset,
            'limit': limit,
        }

    async def update(self, user_id: UUID, update_data: dict) -> User:
        stmt = (
            sql_update(UserModel).where(UserModel.id == user_id).values(**update_data)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()

        user_model = result.scalar()
        return UserMapper.to_entity(user_model)

    async def soft_delete(self, user_id: UUID) -> None:
        stmt = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                is_active=False,
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_permanently(self, user_id: UUID) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
