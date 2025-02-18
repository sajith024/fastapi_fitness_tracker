from datetime import datetime
from typing import Annotated, Optional

from pydantic import (
    UUID4,
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from app.utils.validators import validate_password


class UserCreate(BaseModel):
    first_name: Annotated[str, Field(max_length=100, min_length=3)]
    last_name: Annotated[str, Field(max_length=100, min_length=3)]
    email: EmailStr
    password: Annotated[str, AfterValidator(validate_password)]


class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(max_length=100, min_length=3)] = None
    last_name: Annotated[str | None, Field(max_length=100, min_length=3)] = None


class UserInfo(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: UUID4
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
