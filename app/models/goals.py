from datetime import datetime
from uuid import UUID

from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.users import User


class Goal(Base):
    __tablename__ = "goal"
    target_exercise: Mapped[str] = mapped_column(String(150))
    target_duration: Mapped[int] = mapped_column()
    target_calories: Mapped[float] = mapped_column()
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    # relationship
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(
        back_populates="goals", cascade="all, delete-orphan"
    )

    workouts: Mapped[list["Workout"]] = relationship(  # type: ignore
        back_populates="goal", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.target_exercise}: {self.deadline}"
