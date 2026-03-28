from src.scanner.models.news_item import NewsItem
from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    async def get_entities(self) -> list[NewsItem]: ...
