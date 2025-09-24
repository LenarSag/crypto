from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Crypto(Base):
    __tablename__ = 'cryptos'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)

    prices = relationship('Price', back_populates='crypto')
    subscriptions = relationship('Subscription', back_populates='crypto')
