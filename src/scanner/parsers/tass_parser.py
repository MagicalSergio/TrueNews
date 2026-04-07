from .base_parser import BaseParser
from src.scanner.models.news_item import NewsItem
from icecream import ic
from selectolax.parser import HTMLParser
from src.util.smart_browser import SmartBrowser
from src.util.date_normalizer import DateNormalizer
import json

LINKS_API_URL = "https://tass.ru/tgap/api/v1/messages/search?lang=ru&limit=50"
ROOT_URL = "https://tass.ru"


class TassParser(BaseParser):
    def __init__(self, system_name):
        super().__init__(system_name)
        self._browser = SmartBrowser()

    async def get_entities(self) -> list[NewsItem]:
        async with self._browser:
            links = await self._get_links()
            parsed_articles = [await self._parse_article(l) for l in links]
            filtered_articles = [a for a in parsed_articles if a is not None]
            self._logger.info(
                f"Created news items for: {json.dumps([a.url for a in filtered_articles], ensure_ascii=False, indent=2,)}",
            )
            return filtered_articles

    async def _parse_article(self, url) -> NewsItem | None:
        try:
            response = await self._browser.get(url)
            body = await response.text()
            tree = HTMLParser(body)

            article = tree.css_first("article")
            title = article.css_first("h1").text()

            time: str
            for s in article.css("span"):
                if s.attrs["class"].startswith("Date_"):
                    time = s.text()
                    break

            for f in tree.css("figure"):
                f.decompose()
            for d in tree.css("article > div"):
                d.decompose()

            text = " ".join([p.text() for p in article.css("p")])

            return NewsItem(url, title, text, DateNormalizer.normalize(time))
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
