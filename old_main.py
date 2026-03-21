import asyncio
import json

import httpx

from typing import Callable, Awaitable, Any

from httpx import AsyncClient
from selectolax.parser import HTMLParser, Node

from news_item import NewsItem


html_request_url = "https://www.kommersant.ru/lenta?from=all_lenta"
json_request_url = "https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=3&listid=77&date=&intervaltype=&idafter="


async def parse_html(client, url, *html_classes):
    result = []
    
    try:
        response = await client.get(url)
        if response.status_code != 200:
            print(f"status_code={response.status_code}, url={url}")
    except httpx.RequestError as exc:
        print(f"Ошибка запроса: {exc}, url={url}")
        return None
        
    tree = HTMLParser(response.text)

    for html_class in html_classes:
        result.append(tree.css(html_class))

    return result


async def parse_json(client, url, *parameters):
    result = []

    resp = await client.get(url)

    for parameter in parameters:
        result.append(json.loads(resp.text)[parameter])

    return result


async def parse_urls(
        client: AsyncClient,
        url_from: str,
        parse_func: Callable[[AsyncClient, str, str], Awaitable[list[list[dict[str, Any] | Node]]]],
        parameter: str,
        url_key: str,
        part_of_url: str
):
    urls = []
    parse_result = await parse_func(client, url_from, parameter)

    for item in parse_result[0]:
        if type(item) is Node:
            item = item.attributes

        if not str(item[url_key]).startswith("http"):
            urls.append(f"{part_of_url}{item[url_key]}")

    return urls


async def main():
    urls = []

    async with httpx.AsyncClient() as client:
        new_urls = await parse_urls(
            client,
            html_request_url,
            parse_html,
            ".uho__name.rubric_lenta__item_name .uho__link",
            url_key="href",
            part_of_url="https://www.kommersant.ru"
        )

        urls.extend(new_urls)

        print(urls)
        print(len(urls))

        for i in range(1, 5):
            last_id = urls[-1].split("/")[-1]
            print(last_id)

            json_url = f"{json_request_url}{last_id}"

            new_urls = await parse_urls(
                client,
                json_url,
                parse_json,
                "Items",
                url_key="DocsID",
                part_of_url="https://www.kommersant.ru/doc/"
            )

            urls.extend(new_urls)

        print(urls)
        print(len(urls))

        news_tasks = [parse_html(client, url, ".doc_header__name", ".doc__text") for url in urls]
        news = await asyncio.gather(*news_tasks)

        print(len(news))

        empty_news = []

        for index in range(len(news)):
            if news[index][0]:
                item = NewsItem(
                    urls[index],
                    news[index][0][0].text().strip(),
                    "\n".join([news[index][1][i].text().strip() for i in range(len(news[index][1]))])
                )

                print(item)
            else:
                empty_news.append(urls[index])

        print(f"empty news {len(empty_news)}: {empty_news}")


if __name__ == '__main__':
    asyncio.run(main())