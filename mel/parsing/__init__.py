from .parsers import ParserHintMap


class Language:
    def __init__(self):
        self.hint_map = ParserHintMap()

    def parse(self, text):
        pass
