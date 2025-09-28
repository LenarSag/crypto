from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.db.base import Base


class Coin(Base):
    __tablename__ = 'coins'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ticker: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[str] = mapped_column(server_default=func.now())

    prices = relationship('Price', back_populates='crypto')
    subscriptions = relationship('Subscription', back_populates='crypto')
