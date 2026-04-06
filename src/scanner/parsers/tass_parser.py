from .base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient
from src.scanner.models.news_item import NewsItem
from icecream import ic
import asyncio
import json
from selectolax.parser import HTMLParser, Node
from playwright.async_api import async_playwright

LINKS_API_URL = "https://tass.ru/tgap/api/v1/messages/search?lang=ru&limit=50"
ROOT_URL = "https://tass.ru"


class TassParser(BaseParser):
    def __init__(self, system_name):
        super().__init__(system_name)

        self._http_client = SmartHttpClient()
        self._playwright = async_playwright()

    async def get_entities(self) -> list[NewsItem]:
        async with self._playwright as p:
            browser = await p.chromium.launch(channel="chrome", headless=False)
            async with await browser.new_context() as context:
                page = await context.new_page()
                await page.goto(ROOT_URL, wait_until="domcontentloaded")
                response = await page.goto(LINKS_API_URL)
                json_data = await response.json()
                ic(json.dumps(json_data, ensure_ascii=False, indent=2))
            return []

            # self._playwright.
            # async with self._playwright.
            # links = (await self._get_links())[0:1]
            # results = await asyncio.gather(*[self._parse_article(l) for l in links])
            # filtered_results = [r for r in results if r is not None]

            # self._logger.info(
            #     f"Created news items for: {json.dumps([r.url for r in filtered_results], ensure_ascii=False, indent=2)}",
            # )

            # return filtered_results

    async def _parse_article(self, url) -> NewsItem | None:
        return None

    async def _get_links(self) -> list[str]:
        try:
            response = await self._http_client.get(LINKS_API_URL)
            ic(response.headers)
            ic(response.cookies.items())
            json = response.json()
            links = []
            for r in json["result"]:
                links.append(f"{ROOT_URL}{r['content_url']}")
            return links
        except Exception:
            self._logger.error(f"Failed getting links")
            return []
