from datetime import datetime

from pydantic.types import UUID4
from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from .base import PaginationQuery
from .goals import GoalPublic


class WorkoutQuery(PaginationQuery):
    exercise: str = ""


class WorkoutPublic(BaseModel):
    id: UUID4
    exercise: str
    duration: int
    calories_burned: float
    date: datetime
    goal: GoalPublic

    model_config = ConfigDict(from_attributes=True)


class WorkoutCreate(BaseModel):
    exercise: str
    duration: int
    calories_burned: float
    date: datetime
    goal_id: UUID4 | None = None


class WorkoutUpdate(BaseModel):
    exercise: str | None = None
    duration: int | None = None
    calories_burned: float | None = None
    date: datetime | None = None
    goal_id: UUID4 | None = None
