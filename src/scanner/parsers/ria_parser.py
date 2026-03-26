from src.scanner.parsers.base_parser import BaseParser
from src.scanner.models.news_item import NewsItem


# Роман, пиши сюда :)
class RiaParser(BaseParser):
    async def get_entities(self) -> list[NewsItem]:
        return []
