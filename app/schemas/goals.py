from datetime import datetime
from typing import Annotated

from pydantic import UUID4, AfterValidator, Field
from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from app.utils.validators import validate_exercise, validate_goal_deadline


class GoalPublic(BaseModel):
    id: UUID4
    target_exercise: str
    target_duration: int
    target_calories: float
    deadline: datetime

    model_config = ConfigDict(from_attributes=True)


class GoalCreate(BaseModel):
    target_exercise: Annotated[
        str, Field(max_length=100, min_length=5), AfterValidator(validate_exercise)
    ]
    target_duration: Annotated[int, Field(ge=10, le=120)]
    target_calories: Annotated[float, Field(ge=100, le=1000)]
    deadline: Annotated[datetime, AfterValidator(validate_goal_deadline)]


class GoalUpdate(BaseModel):
    target_exercise: Annotated[
        str | None,
        Field(max_length=100, min_length=5),
        AfterValidator(validate_exercise),
    ] = None
    target_duration: Annotated[int | None, Field(ge=10, le=120)] = None
    target_calories: Annotated[float | None, Field(ge=100, le=1000)] = None
    deadline: Annotated[datetime | None, AfterValidator(validate_goal_deadline)] = None
