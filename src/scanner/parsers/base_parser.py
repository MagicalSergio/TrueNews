from src.scanner.models.news_item import NewsItem
from abc import ABC, abstractmethod
from src.util.create_logger import get_logger
import datetime as dt


class BaseParser(ABC):
    @abstractmethod
    async def get_entities(self) -> list[NewsItem]: ...

    def __init__(self, system_name: str):
        super().__init__()
        self._system_name = system_name
        self._date_created = dt.datetime.now()
        self._logger = get_logger(self._system_name)
        self._logger.info(f"Created {system_name} parser instance")
