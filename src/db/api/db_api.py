from src.db.db_conn import DBConn
from src.util.singleton import singleton
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from src.db.tables import *
from dataclasses import dataclass
from icecream import ic
from src.util.create_logger import get_logger


@dataclass
class InsertNewsItemsDTO:
    url: str
    title: str
    text: str
    source_provider_id: int
    published_at: int


@dataclass
class InsertSourceProvidersDTO:
    system_name: str
    public_name: str
    canonical_url: str


@dataclass
class InsertSourcesDTO:
    system_name: str
    source_provider_id: int
    parser_id: int | None = None


@dataclass
class InsertParsersDTO:
    system_name: str
    module: str
    kwargs_json: str | None = None


@singleton
class DBApi:
    def __init__(self, conn: DBConn = None):
        self._conn = conn or DBConn()
        self._logger = get_logger("database")

    def insert_news_items(self, *dtos: InsertNewsItemsDTO):
        with Session(self._conn.get_engine()) as session:
            stmt = (
                insert(NewsItemDBEntity)
                .values(
                    [
                        dict(
                            url=dto.url,
                            title=dto.title,
                            text=dto.text,
                            source_id=dto.source_provider_id,
                            published_at=dto.published_at,
                        )
                        for dto in dtos
                    ]
                )
                .on_conflict_do_update(
                    index_elements=["url"],
                    set_=dict(
                        title=insert(NewsItemDBEntity).excluded.title,
                        text=insert(NewsItemDBEntity).excluded.text,
                        source_id=insert(NewsItemDBEntity).excluded.source_id,
                        published_at=insert(NewsItemDBEntity).excluded.published_at,
                    ),
                )
            )
            session.execute(stmt)
            session.commit()

    def insert_sources(self, *dtos: InsertSourcesDTO):
        with Session(self._conn.get_engine()) as session:
            for dto in dtos:
                source = SourceDBEntity()
                source.system_name = dto.system_name
                source.source_provider_id = dto.source_provider_id
                source.parser_id = dto.parser_id
                session.add(source)
            session.commit()

    def insert_source_providers(self, *dtos: InsertSourceProvidersDTO):
        with Session(self._conn.get_engine()) as session:
            for dto in dtos:
                source_provider = SourceProviderDBEntity()
                source_provider.system_name = dto.system_name
                source_provider.public_name = dto.public_name
                source_provider.canonical_url = dto.canonical_url
                session.add(source_provider)
            session.commit()

    def insert_parsers(self, *dtos: InsertParsersDTO):
        with Session(self._conn.get_engine()) as session:
            for dto in dtos:
                parser = ParserDBEntity()
                parser.system_name = dto.system_name
                parser.module = dto.module
                parser.kwargs_json = dto.kwargs_json
                session.add(parser)
            session.commit()

    def get_source_provider(self, id) -> SourceProviderDBEntity | None:
        try:
            with Session(self._conn.get_engine()) as session:
                return session.get(SourceProviderDBEntity, id)
        except Exception:
            self._logger.error(f"get_source_provider error", exc_info=True)
            return None

    def get_sources(self, *ids) -> list[SourceDBEntity]:
        try:
            with Session(self._conn.get_engine()) as session:
                stmt = select(SourceDBEntity)
                if ids:
                    stmt = stmt.where(SourceDBEntity.id.in_(ids))
                return session.scalars(stmt).all()
        except Exception:
            return []

    def get_active_sources(self, *ids) -> list[SourceDBEntity]:
        try:
            with Session(self._conn.get_engine()) as session:
                stmt = select(SourceDBEntity)
                if ids:
                    stmt = stmt.where(SourceDBEntity.id.in_(ids)).where(
                        SourceDBEntity.enabled
                    )
                return session.scalars(stmt).all()
        except Exception:
            return []

    def get_parsers(self, *ids) -> list[ParserDBEntity]:
        try:
            with Session(self._conn.get_engine()) as session:
                stmt = select(ParserDBEntity)
                if ids:
                    stmt = stmt.where(ParserDBEntity.id.in_(ids))
                return session.scalars(stmt).all()
        except Exception:
            self._logger.error(f"get_parsers error", exc_info=True)
            return []
