import logging
import os
from src.util.logger_formatter import LOGGER_FORMATTER

def get_logger(system_name: str):
    logger = logging.getLogger(system_name)
    os.makedirs(os.path.dirname(f"logs/{system_name}.log"), exist_ok=True)
    handler = logging.FileHandler(f"logs/{system_name}.log")
    handler.setFormatter(LOGGER_FORMATTER)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger
