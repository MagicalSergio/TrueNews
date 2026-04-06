import asyncio
from selectolax.parser import HTMLParser
from httpx import AsyncClient
from src.scanner.models.news_item import NewsItem
from src.util.date_normalizer import DateNormalizer
from src.scanner.parsers.base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient
import json

DOCS_URL = "https://www.kommersant.ru/doc/"
NEWS_ROOT_URL = "https://www.kommersant.ru/lenta?from=all_lenta"
AJAX_REQUEST_URL = "https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=3&listid=77&date=&intervaltype=&idafter="


class KommersantParser(BaseParser):
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
            article_node = tree.css_first(f'article[data-article-url="{url}"]')
            title = article_node.css_first("h1").text().replace("\n", "").strip()

            paragraph_nodes = article_node.css(".doc__text")
            text = "\n ".join([p.text() for p in paragraph_nodes])

            iso_8601_time = article_node.css_first("time").attributes["datetime"]
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
            links = await self._get_root_page_links()
            last_link_id = links[-1].split("/")[-1]
            while len(links) < count:
                links.extend(await self._get_ajax_links_after(last_link_id))
                last_link_id = links[-1].split("/")[-1]
            return [l for l in links[:count] if l.startswith(DOCS_URL)]
        except Exception:
            self._logger.error(
                f"Failed getting links for {NEWS_ROOT_URL}",
                exc_info=True,
            )
            return []

    async def _get_root_page_links(self):
        root_page = await self._http_client.get(NEWS_ROOT_URL)
        tree = HTMLParser(root_page.text)
        articles = tree.css("article[data-article-url]")
        links = [a.attributes["data-article-url"] for a in articles]
        return [l for l in links if l.startswith(DOCS_URL)]

    async def _get_ajax_links_after(self, id):
        response = await self._http_client.get(self._construct_ajax_req_url(id))
        json_data = response.json()
        items = json_data["Items"]
        return [self._construct_doc_url_for(i["DocsID"]) for i in items]

    def _construct_ajax_req_url(self, id):
        return f"{AJAX_REQUEST_URL}{id}"

    def _construct_doc_url_for(self, id):
        return f"{DOCS_URL}{id}"
