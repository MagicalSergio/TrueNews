import asyncio
from selectolax.parser import HTMLParser
from httpx import AsyncClient
from src.scanner.models.news_item import NewsItem
from src.util.date_normalizer import DateNormalizer
from src.scanner.parsers.base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient
import json


ROOT_URL = "https://ria.ru/"
NEWS_ROOT_URL = "https://ria.ru/lenta/"
NEXT_REQUEST_URL_WITH_FORM = "https://ria.ru/services/lenta/more.html?id={id}&date={date}T{time}&articlemask=lenta_common"


class RiaParser(BaseParser):
    _http_client: AsyncClient

    def __init__(self, system_name: str):
        super().__init__(system_name)
        self._http_client = SmartHttpClient()
        self._logger.info(f"Created {system_name} parser instance")

    async def get_entities(self, count=20) -> list[NewsItem]:
        async with self._http_client:
            links = await self._get_links(count)
            results = await asyncio.gather(*[self._parse_article(l) for l in links])
            filtered_results = [r for r in results if r is not None]

            self._logger.info(
                f"Created news items for: {json.dumps([r.url for r in filtered_results], ensure_ascii=False, indent=2)}"
            )

            return filtered_results


    async def _parse_article(self, url) -> NewsItem | None:
        try:
            response = await self._http_client.get(url)

            tree = HTMLParser(response.text)
            title = tree.css_first(".article__title").text().replace("\n", "").strip()

            paragraph_nodes = tree.css(".article__text")
            text = "\n ".join([p.text() for p in paragraph_nodes])

            iso_8601_time = tree.css_first(
                '[property="article:published_time"]'
            ).attributes["content"]
            time = DateNormalizer.from_iso_8601(iso_8601_time)

            return NewsItem(url, title, text, time)
        except Exception:
            self._logger.error(
                f"Failed parse article for {url}",
                exc_info=True,
            )
            return None

    async def _get_links(self, count) -> list[str]:
        try:
            links, last_link_time = await self._get_links_and_last_news_time(
                NEWS_ROOT_URL
            )

            while len(links) < count:
                last_link_id = links[-1].split("-")[-1].split(".")[0]
                last_link_date = links[-1].split("/")[-2]

                new_links, last_link_time = await self._get_links_and_last_news_time(
                    self._construct_req_url(
                        last_link_id, last_link_date, last_link_time
                    )
                )

                links.extend(new_links)

            return [l for l in links[:count] if l.startswith(ROOT_URL)]
        except Exception:
            self._logger.error(
                f"Failed get links for {NEWS_ROOT_URL}",
                exc_info=True,
            )
            return []

    async def _get_links_and_last_news_time(self, url):
        root_page = await self._http_client.get(url)
        tree = HTMLParser(root_page.text)
        items = tree.css(".list-item")
        articles = [item.css_first(".list-item__image") for item in items]

        last_item_time = items[-1].css_first(".list-item__info-item").text()
        last_item_time = last_item_time[:2] + last_item_time[3:] + "00"

        return [a.attributes["href"] for a in articles], last_item_time

    def _construct_req_url(self, id, date, time):
        return NEXT_REQUEST_URL_WITH_FORM.format(id=id, date=date, time=time)
