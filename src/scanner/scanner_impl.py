from src.scanner.scanner_abc import ScannerABC
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from icecream import ic
from src.db.api.db_api import DBApi
from src.scanner.source_handler import SourceHandler
import asyncio
from src.util.create_logger import get_logger
import datetime as dt
from src.util.calculate_expiry import calculate_expiry


class ScannerImpl(ScannerABC):
    def __init__(self, interval: int):
        super().__init__()
        self._logger = get_logger("scanner")
        self._interval = interval

    def start(self):
        self._scheduler = AsyncIOScheduler()

        last_scan = DBApi().get_scan_timestamp()
        next_run_time: dt.datetime
        if not last_scan:
            next_run_time = dt.datetime.now()
        else:
            next_run_time = calculate_expiry(
                last_scan, dt.datetime.now().timestamp(), self._interval
            )

        self._scheduler.add_job(
            self.job,
            "interval",
            minutes=self._interval,
            misfire_grace_time=None,
            next_run_time=next_run_time,
        )
        self._scheduler.start()
        DBApi().set_scan_timestamp()
        self._logger.info(f"Started scanner with interval: {self._interval}")

    def stop(self):
        self._scheduler.shutdown()

    async def job(self):
        sources_raw = DBApi().get_active_sources()
        handlers: list[SourceHandler] = []

        for s in sources_raw:
            try:
                handlers.append(SourceHandler(s.id))
            except Exception as e:
                self._logger.error(
                    f"Error creating source handler for source_id{s.id}", exc_info=True
                )

        await asyncio.gather(*[h.process() for h in handlers])
        self._logger.info("Finished scan job")
