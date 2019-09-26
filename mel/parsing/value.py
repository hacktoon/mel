from .constants import REFERENCE, LITERAL, LIST, OBJECT, VALUE
from .base import BaseParser, subparser


@subparser
class ValueParser(BaseParser):
    id = VALUE

    def parse(self):
        return self.read_any(REFERENCE, LITERAL, LIST, OBJECT)
