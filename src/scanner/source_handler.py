from src.db.api.db_api import DBApi
from icecream import ic
from src.scanner.parsers.base_parser import BaseParser
from src.scanner.parser_loader import ParserLoader
from src.db.api.db_api import InsertNewsItemsDTO
import json
from src.util.create_logger import get_logger


class SourceHandler:
    _parser_instance: BaseParser

    def __init__(self, source_id: int):
        self._logger = get_logger(f"source_handler_source-id={source_id}")

        try:
            self._source = DBApi().get_sources(source_id)[0]
            self._parser_raw = DBApi().get_parsers(self._source.parser_id)[0]
            self._parser_kwargs = self._parser_raw.kwargs_json or {}
            self._parser_instance = ParserLoader().instantiate_parser(
                self._parser_raw.module,
                self._parser_raw.system_name,
                **self._parser_kwargs,
            )
        except Exception as e:
            msg = f"Failed to initialize source handler for source_id={source_id}"
            self._logger.error(msg, exc_info=True)
            raise RuntimeError(msg) from e

    async def process(self):
        news = await self._parser_instance.get_entities()
        DBApi().insert_news_items(
            *[
                InsertNewsItemsDTO(
                    n.url,
                    n.title,
                    n.text,
                    self._source.source_provider_id,
                    n.timestamp,
                )
                for n in news
            ]
        )
