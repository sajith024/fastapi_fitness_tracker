from datetime import datetime

from pydantic import UUID4
from pydantic.config import ConfigDict
from pydantic.main import BaseModel


class GoalPublic(BaseModel):
    id: UUID4
    target_exercise: str
    target_duration: int
    target_calories: float
    deadline: datetime

    model_config = ConfigDict(from_attributes=True)


class GoalCreate(BaseModel):
    target_exercise: str
    target_duration: int
    target_calories: float
    deadline: datetime


class GoalUpdate(BaseModel):
    target_exercise: str | None = None
    target_duration: int | None = None
    target_calories: float | None = None
    deadline: datetime | None = None
