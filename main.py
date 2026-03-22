import asyncio
import json
from src.parsers.kommersant_parser import KommersantParser


async def main():
    news = await KommersantParser().get_entities()
    json_data = json.dumps([n.__dict__ for n in news], indent=2, ensure_ascii=False)
    with open("./tmp/news.json", "w") as f:
        f.write(json_data)


if __name__ == "__main__":
    asyncio.run(main())
