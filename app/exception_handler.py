from typing import cast
from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse


def request_validation_exception_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    exception = cast(RequestValidationError, exception)
    for err in exception.errors():
        if err.get("ctx"):
            for ctx_key, ctx_value in err["ctx"].items():
                if isinstance(ctx_value, ValueError):
                    err["ctx"] = str(ctx_value)

    detail = {
        "errors": exception.errors(),
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "success": False,
    }
    return JSONResponse(detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def http_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    exception = cast(HTTPException, exception)
    detail = {
        "errors": exception.detail,
        "status": exception.status_code,
        "success": False,
    }
    return JSONResponse(
        detail, status_code=exception.status_code, headers=exception.headers
    )
