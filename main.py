import asyncio
import json
from kommersant_parser import KommersantParser

async def main():
    news = await KommersantParser().get_entites()
    json_data = json.dumps([n.__dict__ for n in news], indent=2, ensure_ascii=False)
    with open('news.json', 'w') as f:
        f.write(json_data)

if __name__ == '__main__':
    asyncio.run(main())
    