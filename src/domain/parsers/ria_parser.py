from src.domain.parsers.base_parser import BaseParser
from src.models.news_item import NewsItem


# Роман, пиши сюда :)
class RiaParser(BaseParser):
    async def get_entities(self) -> list[NewsItem]:
        return []
