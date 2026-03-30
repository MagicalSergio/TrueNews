from src.scanner.models.news_item import NewsItem
from abc import ABC, abstractmethod
import logging
import os

LOGGER_FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


class BaseParser(ABC):
    @abstractmethod
    async def get_entities(self) -> list[NewsItem]: ...

    def __init__(self, system_name: str):
        super().__init__()

        self._system_name = system_name
        self._init_logger()

    def _init_logger(self):
        self._logger = logging.getLogger(self._system_name)

        os.makedirs(os.path.dirname(f"logs/{self._system_name}.log"), exist_ok=True)
        handler = logging.FileHandler(f"logs/{self._system_name}.log")
        handler.setFormatter(LOGGER_FORMATTER)

        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False
