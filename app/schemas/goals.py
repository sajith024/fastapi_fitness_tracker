from datetime import datetime

from pydantic.config import ConfigDict
from pydantic.main import BaseModel

class GoalPublic(BaseModel):
    target_exercise: str
    target_duration: int
    target_calories: float
    deadline: datetime