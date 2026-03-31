from src.scanner.models.news_item import NewsItem
from abc import ABC, abstractmethod
import logging
import os
from src.util.logger_formatter import LOGGER_FORMATTER
from src.util.create_logger import get_logger


class BaseParser(ABC):
    @abstractmethod
    async def get_entities(self) -> list[NewsItem]: ...

    def __init__(self, system_name: str):
        super().__init__()
        self._system_name = system_name
        self._logger = get_logger(self._system_name)
