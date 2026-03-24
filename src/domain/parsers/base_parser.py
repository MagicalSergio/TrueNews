from src.models.news_item import NewsItem
from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    async def get_entities() -> list[NewsItem]: ...
