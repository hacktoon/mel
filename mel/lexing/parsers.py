from .char import Char
from .token import Token


class BaseParser:
    id = ''
    hint = ''

    def parse(self, stream):
        chars = self._read(stream)
        return Token(self.id, chars)

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
