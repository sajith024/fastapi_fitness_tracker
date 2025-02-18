import os
from pydantic import BaseModel

from app.utils import date_tz


def get_log_file_name():
    today = date_tz.now().strftime("%Y-%m-%d")
    log_folder = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_folder, exist_ok=True)
    return os.path.join(log_folder, f"{today}.log")


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(asctime)s - [%(levelname)s]:%(name)s - %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": get_log_file_name(),
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["file"], "level": LOG_LEVEL},
    }
