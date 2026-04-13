"""Logging configuration for the RISCO application."""

import logging
from pathlib import Path

log_dir = Path(__file__).parent.parent / "logs"

# db specific log
db_handler = logging.FileHandler(log_dir / "db.log")

# errors only
error_handler = logging.FileHandler(log_dir / "error.log")
error_handler.setLevel(logging.ERROR)  # only ERROR and CRITICAL

# sends logs in real time
stream_handler = logging.StreamHandler()

# configures logs settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[db_handler, error_handler, stream_handler],
)


def get_logger(name: str):
    """Sets up and returns the application logger."""
    return logging.getLogger(name)
