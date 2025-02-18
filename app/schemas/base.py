from typing import Annotated, TypeVar, Generic

from pydantic import (
    BaseModel,
    Field,
)

TORNone = TypeVar("TORNone", default=None)
T = TypeVar("T")


class EmailData(BaseModel):
    html_content: str
    subject: str


class AppResponse(BaseModel, Generic[TORNone]):
    data: TORNone | None = None
    message: str = ""
    status: int


class AppPaginatedResponse(BaseModel, Generic[T]):
    result: list[T]
    page: int
    limit: int
    total: int
    status: int


class PaginationQuery(BaseModel):
    page: Annotated[int, Field(ge=1, le=100)] = 1
    limit: Annotated[int, Field(ge=10, le=100)] = 10
