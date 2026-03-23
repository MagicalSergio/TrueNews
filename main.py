import asyncio
from src.domain.parser_loader import ParserLoader
import json
from icecream import ic


async def main():
    news = []
    for p in ParserLoader().all():
        news.extend(await p.get_entities())

    json_data = json.dumps([n.__dict__ for n in news], indent=2, ensure_ascii=False)
    with open("./tmp/news.json", "w") as f:
        f.write(json_data)


if __name__ == "__main__":
    asyncio.run(main())
