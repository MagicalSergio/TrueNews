from src.scanner.parsers import *
from src.config import PROJECT_ROOT
import pkgutil
import importlib
import inspect
from src.util.singleton import singleton
from src.util.find_parent import find_root
from icecream import ic
import re


@singleton
class ParserLoader:
    _parsers: list[BaseParser] = []

    def __init__(self):
        self._load_parsers()

    def all(self):
        return self._parsers

    def instantiate_parser(self, module: str = "", **kwargs) -> BaseParser:
        parsers_dir = find_root(__file__, ".scanner_root") / "parsers"
        module = next(
            (
                module
                for module in pkgutil.iter_modules([str(parsers_dir)])
                if module.name == "kommersant_parser"
            ),
            None,
        )

        if not module:
            raise Exception("Parser module not found")

        module_str = f"{str(parsers_dir)}/{module.name}".replace("/", ".")
        module_import_str = re.search(r"src.\S+", module_str).group(0)
        imported = importlib.import_module(module_import_str)

        classes = inspect.getmembers(imported, inspect.isclass)
        parser = next(
            (
                cls[1]
                for cls in classes
                if issubclass(cls[1], BaseParser) and cls[1] is not BaseParser
            ),
            None
        )

        if not parser:
            raise Exception("Parser class not found")

        return parser(**kwargs)

    def _load_parsers(self) -> list[type[BaseParser]]:
        parsers_dir = PROJECT_ROOT / "src" / "scanner" / "parsers"
        for m in pkgutil.iter_modules([str(parsers_dir)]):
            imported_m = importlib.import_module(f"src.scanner.parsers.{m.name}")
            classes = inspect.getmembers(imported_m, inspect.isclass)
            for cls in classes:
                if issubclass(cls[1], BaseParser) and cls[1] is not BaseParser:
                    self._parsers.append(cls[1]())
