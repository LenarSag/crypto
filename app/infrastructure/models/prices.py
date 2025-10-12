from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.db.base import Base


class Price(Base):
    __tablename__ = 'prices'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    price: Mapped[float]
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    coin_id: Mapped[UUID] = mapped_column(ForeignKey('coins.id'))

    coin = relationship('Coin', back_populates='prices')

    __table_args__ = (Index('idx_coin_timestamp_desc', 'coin_id', timestamp.desc()),)
