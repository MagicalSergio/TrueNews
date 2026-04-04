from .base_parser import BaseParser


class TassParser(BaseParser):
    def __init__(self, system_name):
        super().__init__(system_name)

    def get_entities(self):
        return super().get_entities()
