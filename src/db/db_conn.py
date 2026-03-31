from src.db.tables import *
from sqlalchemy import create_engine, Engine, text
from icecream import ic
from src.config import PROJECT_ROOT
from .settings import DB_PATH
from src.util.singleton import singleton


@singleton
class DBConn:
    _TABLES_PATH = PROJECT_ROOT / "src" / "db" / "tables"

    _engine: Engine

    def __init__(self):
        self._check_db_existence()
        self._engine = create_engine(
            f"sqlite:///{DB_PATH}",
            connect_args={
                "timeout": 15,
                "check_same_thread": False,
            },
        )

        with self._engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL"))
            conn.execute(text("PRAGMA busy_timeout=5000"))

        MainBase.metadata.create_all(self._engine)

    def get_engine(self):
        return self._engine

    def _check_db_existence(self):
        if not DB_PATH.exists():
            with open(DB_PATH, "w"):
                pass
