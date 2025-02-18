from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.models.base import Base


class User(Base):
    __tablename__ = "user"
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str] = mapped_column(String(255), default="")

    # relationship
    goals: Mapped[list["Goal"]] = relationship(  # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
    workouts: Mapped[list["Workout"]] = relationship(  # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
