from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP

from app.utils import date_tz


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, sort_order=-1)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=date_tz.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=date_tz.now, onupdate=date_tz.now
    )

    def __str__(self) -> str:
        return str(self.id)
