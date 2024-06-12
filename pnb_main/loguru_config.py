# loguru_config.py

from loguru import logger
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Define log file path
log_file_path = os.path.join(BASE_DIR, 'django_loguru.log')

# Remove all existing handlers
logger.remove()

# Add a new handler for file output (write all logs to the file)
logger.add(log_file_path, level="DEBUG", format="{time} {level} {message}", rotation="10 MB", compression="zip")

# Function to intercept standard logging and route it to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logging call
        frame, depth = logging.currentframe(), 2
        while frame.f_globals["__name__"] == __name__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Configure Django's logging to use Loguru's handler
logging.basicConfig(handlers=[InterceptHandler()], level=0)
