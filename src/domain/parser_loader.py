from src.domain.parsers.base_parser import BaseParser
from src.config import PROJECT_ROOT
import pkgutil
import importlib
import inspect
from src.util.singleton import singleton
from icecream import ic


@singleton
class ParserLoader:
    _parsers: list[BaseParser] = []

    def __init__(self):
        self._load_parsers()

    def all(self):
        return self._parsers

    def _load_parsers(self) -> list[type[BaseParser]]:
        parsers_dir = PROJECT_ROOT / "src" / "domain" / "parsers"
        modules = [m for m in pkgutil.iter_modules([str(parsers_dir)])]
        for m in modules:
            imported_m = importlib.import_module(f"src.domain.parsers.{m.name}")
            classes = inspect.getmembers(imported_m, inspect.isclass)
            for cls in classes:
                if issubclass(cls[1], BaseParser) and cls[1] is not BaseParser:
                    self._parsers.append(cls[1]())
