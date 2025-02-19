from typing import Annotated

from pydantic import AfterValidator, Field
from pydantic.types import UUID4
from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from app.utils.validators import validate_exercise

from .base import PaginationQuery
from .goals import GoalPublic


class WorkoutQuery(PaginationQuery):
    exercise: Annotated[
        str, Field(max_length=100), AfterValidator(validate_exercise)
    ] = ""


class WorkoutPublic(BaseModel):
    id: UUID4
    exercise: str
    duration: int
    calories_burned: float
    goal: GoalPublic

    model_config = ConfigDict(from_attributes=True)


class WorkoutCreate(BaseModel):
    exercise: Annotated[
        str, Field(max_length=100, min_length=5), AfterValidator(validate_exercise)
    ]
    duration: Annotated[int, Field(ge=10, le=120)]
    calories_burned: Annotated[float, Field(ge=100, le=1000)]
    goal_id: UUID4 | None = None


class WorkoutUpdate(BaseModel):
    exercise: Annotated[
        str | None,
        Field(max_length=100, min_length=5),
        AfterValidator(validate_exercise),
    ] = None
    duration: Annotated[int | None, Field(ge=10, le=120)] = None
    calories_burned: Annotated[float | None, Field(ge=100, le=1000)] = None
    goal_id: UUID4 | None = None
