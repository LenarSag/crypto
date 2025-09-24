from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Price(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float]
    timestamp: Mapped[datetime]

    crypto_id: Mapped[int] = mapped_column(ForeignKey('cryptos.id'))

    crypto = relationship(
        'Crypto', back_populates='subscriptions', cascade='all, delete-orphan'
    )
