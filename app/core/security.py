from datetime import timedelta
from typing import Annotated, Any

import bcrypt
import jwt
from fastapi import Form, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.utils import date_tz


ALGORITHM = "HS256"


class PublicOAuth2PasswordBearer(OAuth2PasswordBearer):
    pass


class PublicOAuth2PasswordRequestForm:
    def __init__(
        self,
        password: Annotated[str, Form()],
        username: Annotated[str, Form()] = "",
        email: Annotated[str, Form()] = "",
    ):
        self.email = email if email else username
        self.password = password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    encoded_plain_password = plain_password.encode()
    encoded_hashed_password = hashed_password.encode()
    return bcrypt.checkpw(encoded_plain_password, encoded_hashed_password)


def get_password_hash(password: str) -> str:
    encoded_password = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt).decode()


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is not None:
        expires_at = date_tz.now() + expires_delta
    else:
        expires_at = date_tz.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_at, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is not None:
        expires_at = date_tz.now() + expires_delta
    else:
        expires_at = date_tz.now() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_at, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_jwt_token(
    token: str, secret: str = settings.JWT_SECRET_KEY
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials",
        )

    return payload
