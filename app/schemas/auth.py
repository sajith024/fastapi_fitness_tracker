from pydantic import (
    BaseModel,
    EmailStr,
)


class TokenRefresh(BaseModel):
    refresh: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
