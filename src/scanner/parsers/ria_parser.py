import asyncio
import traceback
from selectolax.parser import HTMLParser
from httpx import AsyncClient
from src.scanner.models.news_item import NewsItem
from src.util.date_normalizer import DateNormalizer
from src.scanner.parsers.base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient


NEWS_ROOT_URL = "https://ria.ru/lenta/"
NEXT_REQUEST_URL_WITH_FORM = "https://ria.ru/services/lenta/more.html?id={id}&date={date}T{time}&articlemask=lenta_common"


class RiaParser(BaseParser):
    _http_client: AsyncClient

    async def get_entities(self, count=20) -> list[NewsItem]:
        async with SmartHttpClient() as http_client:
            self._http_client = http_client
            try:
                links = await self._get_links(count)
                parsing_coroutines = [self._parse_article(l) for l in links]
                results = await asyncio.gather(*parsing_coroutines)
                return results
            except Exception:
                traceback.print_exc()
                return []

    async def _parse_article(self, url):
        response = await self._http_client.get(url)

        tree = HTMLParser(response.text)
        title = tree.css_first(".article__title").text().replace("\n", "").strip()

        paragraph_nodes = tree.css(".article__text")
        text = " ".join([p.text() for p in paragraph_nodes])

        iso_8601_time = tree.css_first(
            '[property="article:published_time"]'
        ).attributes["content"]
        time = DateNormalizer.from_iso_8601(iso_8601_time)

        return NewsItem(url, title, text, time)

    async def _get_links(self, count):
        links, last_link_time = await self._get_links_and_last_news_time(NEWS_ROOT_URL)

        while len(links) < count:
            last_link_id = links[-1].split("-")[-1].split(".")[0]
            last_link_date = links[-1].split("/")[-2]

            new_links, last_link_time = await self._get_links_and_last_news_time(
                self._construct_req_url(last_link_id, last_link_date, last_link_time)
            )

            links.extend(new_links)

        return links[:count]

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
