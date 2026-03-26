from src.db.db_conn import DBConn
from src.util.singleton import singleton
from sqlalchemy.orm import Session
from src.db.tables import *
from dataclasses import dataclass
from icecream import ic
import traceback


@dataclass
class SaveNewsItemDTO:
    url: str
    title: str
    text: str
    source_provider_id: int
    published_at: int


@dataclass
class SaveSourceProviderDTO:
    system_name: str
    public_name: str
    canonical_url: str


@dataclass
class SaveSourceDTO:
    source_provider_id: int
    parser_id: int | None


@singleton
class DBApi:
    def __init__(self, conn: DBConn = None):
        self._conn = conn or DBConn()

    def save_news_item(self, *dtos: SaveNewsItemDTO):
        with Session(self._conn.get_engine()) as session:
            for dto in dtos:
                news_item = NewsItemDBEntity()
                news_item.url = dto.url
                news_item.title = dto.title
                news_item.text = dto.text
                news_item.source_id = dto.source_provider_id
                news_item.published_at = dto.published_at
                session.add(news_item)
            session.commit()

    def save_source(self, *dtos: SaveSourceDTO):
        with Session(self._conn.get_engine()) as session:
            for dto in dtos:
                source = SourceDBEntity()
                source.source_provider_id = dto.source_provider_id
                source.parser_id = dto.parser_id
                session.add(source)
            session.commit()

    def save_source_provider(self, dto: SaveSourceProviderDTO):
        with Session(self._conn.get_engine()) as session:
            source_provider = SourceProviderDBEntity()
            source_provider.system_name = dto.system_name
            source_provider.public_name = dto.public_name
            source_provider.canonical_url = dto.canonical_url
            session.add(source_provider)
            session.commit()

    def get_source_provider(self, id) -> SourceProviderDBEntity | None:
        try:
            with Session(self._conn.get_engine()) as session:
                return session.get(SourceProviderDBEntity, id)
        except Exception:
            traceback.print_exc()
            return None
