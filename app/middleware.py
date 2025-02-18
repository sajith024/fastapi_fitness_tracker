import logging
from logging.config import dictConfig

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging_config import LogConfig

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("app")


class SimpleLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Request received: {request.method} {request.url}")
        return await call_next(request)
