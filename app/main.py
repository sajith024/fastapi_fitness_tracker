from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.dependencies import authenticate_swagger
from app.exception_handler import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.middleware import SimpleLoggingMiddleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_url=None,
)

# middlewares
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(SimpleLoggingMiddleware)

# exception_handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


# routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get(
    "/openapi.json",
    include_in_schema=False,
    tags=["documentation"],
    dependencies=[Depends(authenticate_swagger)],
)
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            summary=app.summary,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            webhooks=app.webhooks.routes,
            tags=app.openapi_tags,
            servers=app.servers,
            separate_input_output_schemas=app.separate_input_output_schemas,
        )
    )
    return response


@app.get("/docs", tags=["documentation"], include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


if app.swagger_ui_oauth2_redirect_url:

    @app.get(
        app.swagger_ui_oauth2_redirect_url,
        tags=["documentation"],
        include_in_schema=False,
    )
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", tags=["documentation"], include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc",
    )


@app.get("/", tags=["documentation"], include_in_schema=False)
async def home() -> dict[str, str]:
    return {"project": settings.PROJECT_NAME, "message": "Hello World! 🎉️🥳️🎉️🥳️🎉️"}
