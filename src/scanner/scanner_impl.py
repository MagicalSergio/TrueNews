from src.scanner.scanner_abc import ScannerABC
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from icecream import ic
from src.db.api.db_api import DBApi
from src.scanner.source_handler import SourceHandler
import asyncio
import datetime
import logging


class ScannerImpl(ScannerABC):
    def start(self):
        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_job(
            self.job,
            "interval",
            minutes=10,
            misfire_grace_time=None,
            next_run_time=datetime.datetime.now(),
        )
        self._scheduler.start()
        self._logger = logging.getLogger("scanner")

    def stop(self):
        self._scheduler.shutdown()

    async def job(self):
        sources_raw = DBApi().get_sources()
        handlers: list[SourceHandler] = []

        for s in sources_raw:
            try:
                handlers.append(SourceHandler(s.id))
            except Exception as e:
                self._logger.error(f"Error creating source handler for source_id{s.id}", exc_info=True)

        await asyncio.gather(*[h.process() for h in handlers])
