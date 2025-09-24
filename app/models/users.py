from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    telegram_id: Mapped[int | None]
    is_active: Mapped[bool]
    created_at: Mapped[datetime]

    subscriptions = relationship(back_populates='user')
