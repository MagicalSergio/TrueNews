from .base_parser import BaseParser
from src.util.smart_http_client import SmartHttpClient
from icecream import ic
from src.scanner.models.news_item import NewsItem
from selectolax.parser import HTMLParser, Node
from src.util.date_normalizer import DateNormalizer
import asyncio


class UniversalParser(BaseParser):
    def __init__(self, **kwargs):
        self._root_url = kwargs["root_url"]
        self._feed_url = kwargs["feed_url"]
        self._feed_nodes = kwargs["feed_nodes"]
        self._article_nodes = kwargs["article_nodes"]
        self._append_params = kwargs.get("append_params") or {}
        self._impersonate = kwargs.get("impersonate") or "chrome"

    async def get_entities(self) -> list[NewsItem]:
        async with SmartHttpClient(self._impersonate) as http_client:
            self._http_client = http_client
            links = await self._get_links()
            results = await asyncio.gather(
                *[self._parse_article(l) for l in links],
                return_exceptions=True,
            )
            return [r for r in results if not isinstance(r, Exception)]

    async def _get_links(self) -> list[str]:
        root_page = await self._http_client.get(self._normalize_url(self._feed_url))
        tree = HTMLParser(root_page.text).body
        link_nodes = tree.css(self._feed_nodes["link"]["selector"])
        return [
            value
            for l in link_nodes
            if (value := self._extract_value(l, self._feed_nodes["link"]["content"]))
            and self._normalize_url(value).startswith(self._root_url)
        ]

    async def _parse_article(self, url) -> NewsItem:
        absolute_url = self._normalize_url(url)
        article_raw = await self._http_client.get(absolute_url)
        tree = HTMLParser(article_raw.text)

        fields = {}
        for key in ("title", "text", "time"):
            if self._article_nodes[key]["selector"].startswith("*"):
                nodes = tree.css(
                    self._article_nodes[key]["selector"].replace("*", "").strip()
                )
                fields[key] = "\n ".join(
                    [
                        self._extract_value(n, self._article_nodes[key]["content"])
                        for n in nodes
                    ]
                )
            else:
                node = tree.css_first(self._article_nodes[key]["selector"])
                fields[key] = self._extract_value(
                    node, self._article_nodes[key]["content"]
                )

        return NewsItem(
            absolute_url,
            fields["title"],
            fields["text"],
            DateNormalizer.normalize(fields["time"]),
        )

    def _normalize_url(self, url: str) -> str:
        absolute = url if url.startswith("https") else f"{self._root_url}{url}"
        if not self._append_params:
            return absolute
        query = "&".join(f"{p}={val}" for p, val in self._append_params.items())
        return f"{absolute}?{query}"

    def _extract_value(self, node: Node, identity: str) -> str:
        """identity: text or [attribute]"""
        if identity.startswith("[") and identity.endswith("]"):
            return node.attributes[f"{identity.strip("[]")}"]
        elif identity == "text":
            return node.text().replace("\n", "").strip()
