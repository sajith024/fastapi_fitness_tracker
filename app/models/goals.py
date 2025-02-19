from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID

from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.users import User

if TYPE_CHECKING:
    from app.models.workouts import Workout


class Goal(Base):
    __tablename__ = "goal"
    target_exercise: Mapped[str] = mapped_column(String(150))
    target_duration: Mapped[int] = mapped_column()
    target_calories: Mapped[float] = mapped_column()
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_notified: Mapped[bool] = mapped_column(default=False)

    # relationship
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="goals")

    workouts: Mapped[list["Workout"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.target_exercise}: {self.deadline}"
