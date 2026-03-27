from src.scanner.parsers import *
import pkgutil
import importlib
import inspect
from src.util.singleton import singleton
from src.util.find_parent import find_root
from icecream import ic
import re


@singleton
class ParserLoader:
    def __init__(self):
        pass

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
