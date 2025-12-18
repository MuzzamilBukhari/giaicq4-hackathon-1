import logging
import sys
from src.config import settings


def setup_logging():
    """
    Configure logging for the application
    """
    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Clear any existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Add console handler to root logger
    root_logger.addHandler(console_handler)

    # Set specific loggers to WARNING level to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("qdrant_client").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    """
    logger = logging.getLogger(name)
    return logger


# Initialize logging when module is imported
setup_logging()