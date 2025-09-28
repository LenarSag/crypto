from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.models.users import User as SqlUser


class UserRepository(IUserRepository):
    def __init__(self, session_factory: AsyncSession):
        self.session = session_factory

    async def add(self, user: User) -> None:
        self.session.add(
            SqlUser(
                id=str(user.id),
                email=user.email,
                password=user.password,
                is_active=user.is_active,
            )
        )
        await self.session.commit()

    async def get_by_email(self, email: str):
        async with self._session_factory() as session:
            row = await session.scalar(
                session.query(SqlUser).filter(SqlUser.email == email)
            )
            return (
                User(
                    id=row.id,
                    email=row.email,
                    password_hash=row.password_hash,
                    is_active=row.is_active,
                )
                if row
                else None
            )
