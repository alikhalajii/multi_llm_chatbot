import logging
import logging.config
import os
from datetime import datetime

# Base log directory
LOG_DIR = os.getenv("CHATBOT_LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# File name with current date
DATE_STR = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_DIR, f"chatbot_{DATE_STR}.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": LOG_FILE,
            "mode": "a",
            "encoding": "utf-8",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def setup_logging():
    """Configure logging using dictConfig."""
    logging.config.dictConfig(LOGGING_CONFIG)
