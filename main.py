import asyncio
import httpx
from selectolax.parser import HTMLParser

from news import News


main_url = "https://www.kommersant.ru/lenta?from=all_lenta&page=3"


async def parse(client, url, *html_classes):
    result = []

    resp = await client.get(url)
    tree = HTMLParser(resp.text)

    for html_class in html_classes:
        result.append(tree.css(f".{html_class}"))

    return result


async def main():
    urls = set()

    async with httpx.AsyncClient() as client:
        main_page_task = parse(client, main_url, "uho__link")
        top_news = await asyncio.gather(main_page_task)

        for item in top_news[0][0]:
            url = f"https://www.kommersant.ru{item.attributes.get("href")}"
            urls.add(url)

        print(urls)
        print(len(urls))

        news_tasks = [parse(client, url, "doc_header__name", "doc__text") for url in urls]
        news = await asyncio.gather(*news_tasks)

        urls = list(urls)

        for index in range(len(news)):
            item = News(
                urls[index],
                news[index][0][0].text().strip(),
                "\n".join([news[index][1][i].text().strip() for i in range(len(news[index][1]))])
            )

            print(item)


if __name__ == '__main__':
    asyncio.run(main())