from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID

from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.users import User
from app.utils import date_tz

if TYPE_CHECKING:
    from app.models.goals import Goal


class Workout(Base):
    __tablename__ = "workout"
    exercise: Mapped[str] = mapped_column(String(150))
    duration: Mapped[int] = mapped_column()
    calories_burned: Mapped[float] = mapped_column(default=0)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    # relationship
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="workouts")

    goal_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("goal.id", ondelete="CASCADE")
    )
    goal: Mapped["Goal | None"] = relationship(back_populates="workouts")

    def __str__(self) -> str:
        return f"{self.exercise}: {self.calories_burned}"
