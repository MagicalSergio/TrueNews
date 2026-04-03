import logging
import os
from src.util.logger_formatter import LOGGER_FORMATTER


def get_logger(system_name: str) -> logging.Logger:
    if system_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(system_name)

    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(system_name)
    handler = logging.FileHandler(f"logs/{system_name}.log")
    handler.setFormatter(LOGGER_FORMATTER)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger
