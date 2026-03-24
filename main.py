import asyncio
from src.domain.parser_loader import ParserLoader
import json
from icecream import ic
from src.db.api.db_api import DBApi, SaveSourceProviderDTO, SaveSiteNewsItemDTO
from src.models.news_item import NewsItem


async def main():
    db_api = DBApi()
    source_provider = db_api.get_source_provider(1)
    if not source_provider:
        db_api.save_source_provider(SaveSourceProviderDTO("kommersant", "Коммерсант"))
        source_provider = db_api.get_source_provider(1)

    news: list[NewsItem] = []
    for p in ParserLoader().all():
        news.extend(await p.get_entities())

    news_dto_list = [
        SaveSiteNewsItemDTO(n.url, n.title, n.text, source_provider.id, n.timestamp)
        for n in news
    ]
    db_api.save_news_item(*news_dto_list)


if __name__ == "__main__":
    asyncio.run(main())
