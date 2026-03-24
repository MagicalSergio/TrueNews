from sqlalchemy import create_engine
from icecream import ic
from src.config import PROJECT_ROOT
from .tables.main_base import MainBase
import importlib
import pkgutil
from src.util.singleton import singleton
import re


@singleton
class DBConn:
    _DB_PATH = PROJECT_ROOT / "data" / "app.db"
    _TABLES_PATH = PROJECT_ROOT / "src" / "db" / "tables"

    _engine = None

    def __init__(self):
        self._check_db_existence()
        self._load_tables()
        self._engine = create_engine(f"sqlite:///{self._DB_PATH}")
        MainBase.metadata.create_all(self._engine)

    def get_engine(self):
        return self._engine

    def _load_tables(self):
        modules = [m for m in pkgutil.iter_modules([str(self._TABLES_PATH)])]
        table_modules = [m for m in modules if m.name.startswith("table_")]
        table_paths = [f"{self._TABLES_PATH}/{m.name}.py" for m in table_modules]
        for tp in table_paths:
            module = re.search(r"(src/).+[^(.py)]", tp).group(0).replace("/", ".")
            importlib.import_module(module)

    def _check_db_existence(self):
        if not self._DB_PATH.exists():
            with open(self._DB_PATH, "w"):
                pass
