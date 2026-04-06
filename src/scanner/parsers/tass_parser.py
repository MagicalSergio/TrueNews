from .base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient
from src.scanner.models.news_item import NewsItem
from icecream import ic
import asyncio
import json
from selectolax.parser import HTMLParser, Node
from playwright.async_api import async_playwright
from src.util.smart_browser import SmartBrowser

LINKS_API_URL = "https://tass.ru/tgap/api/v1/messages/search?lang=ru&limit=50"
ROOT_URL = "https://tass.ru"


class TassParser(BaseParser):
    def __init__(self, system_name):
        super().__init__(system_name)
        self._browser = SmartBrowser()

    async def get_entities(self) -> list[NewsItem]:
        async with self._browser:
            links = (await self._get_links())[:1]
            parsed_articles = [await self._parse_article(l) for l in links]
            return [a for a in parsed_articles if a is not None]

    # @dataclass
    # class NewsItem:
    #     url: str
    #     title: str
    #     text: str
    #     timestamp: int

    async def _parse_article(self, url) -> NewsItem | None:
        try:
            response = await self._browser.get(url)
            body = await response.text()
            tree = HTMLParser(body)

            article = tree.css_first("article")
            title = article.css_first("h1").text()

            for f in tree.css("figure"):
                f.decompose()
            for d in tree.css("article > div"):
                d.decompose()

            text = " ".join([p.text() for p in article.css("p")])
            # timestamp
            ic(url)
            ic(title)
            ic(text)
            # ic(text)
            return None
        except Exception:
            self._logger.error(
                f"Failed parsing article for {self._system_name}, url: {url}",
                exc_info=True,
            )
            return None

    async def _get_links(self) -> list[str]:
        try:
            response = await self._browser.get(LINKS_API_URL)
            json_data = await response.json()
            links = []
            for r in json_data["result"]:
                links.append(f"{ROOT_URL}{r['content_url']}")
            return links
        except Exception:
            self._logger.error(f"Failed getting links")
            return []
