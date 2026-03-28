import asyncio
from src.db.api.db_api import DBApi
from src.scanner.source_handler import SourceHandler


async def main():
    sources_raw = DBApi().get_sources()
    handlers: list[SourceHandler] = []

    for s in sources_raw:
        handlers.append(SourceHandler(s.id))

    await asyncio.gather(*[h.process() for h in handlers])


if __name__ == "__main__":
    asyncio.run(main())
