from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    threshold_value: Mapped[float] = mapped_column(nullable=False)
    control_value: Mapped[float] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    crypto_id: Mapped[int] = mapped_column(ForeignKey('cryptos.id'))

    user = relationship(back_populates='subscriptions', cascade='all, delete-orphan')
    crypto = relationship(back_populates='subscriptions', cascade='all, delete-orphan')
