from datetime import datetime
from uuid import uuid4

from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.domain.entities.user import UserRole
from app.infrastructure.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    telegram_id: Mapped[int | None]
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    subscriptions = relationship(back_populates='user')
