import secrets
from typing import Annotated

from fastapi import Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    PublicOAuth2PasswordBearer,
    decode_jwt_token,
)
from app.models.users import User
import app.crud.users as user_crud


oauth2_scheme_public = PublicOAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

SessionDep = Annotated[AsyncSession, Depends(get_db)]

TokenDep = Annotated[str, Security(oauth2_scheme_public)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    payload = decode_jwt_token(token)
    user = await user_crud.get_user_by_email(session, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


SuperUser = Annotated[User, Depends(get_current_superuser)]


def authenticate_swagger(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]
) -> None:
    correct_username = secrets.compare_digest(
        credentials.username, settings.SWAGGER_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.SWAGGER_PASSWORD
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
