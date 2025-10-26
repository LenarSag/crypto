from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.domain.entities.subscription import ComparisonOperator
from app.infrastructure.db.base import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    threshold_value: Mapped[float] = mapped_column(nullable=False)
    comparsion_operator: Mapped[ComparisonOperator] = mapped_column(
        SqlEnum(ComparisonOperator)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    user_id: Mapped[PG_UUID] = mapped_column(ForeignKey('users.id'))
    coin_id: Mapped[PG_UUID] = mapped_column(ForeignKey('coins.id'))

    user = relationship(back_populates='subscriptions', cascade='all, delete-orphan')
    coin = relationship(back_populates='subscriptions', cascade='all, delete-orphan')
