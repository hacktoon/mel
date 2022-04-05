from ..scanning.stream import Char
from .nodes import Node


class ParserHintMap:
    def __init__(self):
        self._map = {
            cls.hint: cls for cls in
            BaseParser.__subclasses__()
        }

    def has(self, parser):
        return self._map.get(parser.hint)


class BaseParser:
    id = ''
    hint = ''

    def parse(self, stream):
        chars = self._read(stream)
        return Node(self.id, chars)

    def _read(self, stream):
        raise NotImplementedError()


# ======================================
class IntParser(BaseParser):
    id = 'integer'
    hint = Char.DIGIT

    def _read(self, stream):
        return stream.one_many_types(Char.DIGIT)


# ======================================
class StringParser(BaseParser):
    id = 'string'  # noqa
    hint = '"'  # noqa

    def _read(self, stream):
        return stream.one_str('"')
