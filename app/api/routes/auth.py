from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.crud import users as user_crud
from app.core.config import settings
from app.core.security import (
    PublicOAuth2PasswordRequestForm,
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
)
from app.dependencies import (
    CurrentUser,
    SessionDep,
)
from app.schemas.auth import TokenRefresh
from app.schemas.base import AppResponse
from app.schemas.users import UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def user_signup(session: SessionDep, user_in: UserCreate) -> AppResponse:
    user = await user_crud.get_user_by_email(session, user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist",
        )

    user = await user_crud.create_user(session=session, user_create=user_in)
    return AppResponse(message="Created successfully", status=status.HTTP_201_CREATED)


@router.post("/login")
async def user_login(
    session: SessionDep,
    form_data: Annotated[PublicOAuth2PasswordRequestForm, Depends()],
) -> JSONResponse:
    user = await user_crud.authenticate(
        session=session, email=form_data.email, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    return JSONResponse(
        content={
            "data": UserPublic.model_validate(user).model_dump(mode="json"),
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/refresh")
async def refresh_token(
    current_user: CurrentUser, refresh_token: TokenRefresh
) -> JSONResponse:
    if not refresh_token.refresh:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No refresh token"
        )

    decoded_token = decode_jwt_token(refresh_token.refresh, settings.SECRET_KEY)
    if decoded_token["sub"] != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
        )

    access_token = create_access_token(current_user.email)
    return JSONResponse({"access_token": access_token}, status_code=status.HTTP_200_OK)
