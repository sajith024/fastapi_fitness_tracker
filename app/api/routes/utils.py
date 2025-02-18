from fastapi import APIRouter, status

from app.schemas.base import AppResponse


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check")
async def health_check() -> AppResponse[bool]:
    return AppResponse(
        data=True, message="Health is good 😃️", status=status.HTTP_200_OK
    )
