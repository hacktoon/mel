from ..char import (
    Char,
    DigitChar,
    LowerChar,
    NewlineChar,
    SpaceChar,
    UpperChar,
)
from ..stream import CharStream
from ..produce import Produce, ValidProduce
from .base import Parser


########################################################################
# BASE CHAR PARSER
########################################################################
class CharParser(Parser):
    def __init__(self, expected: str = ''):
        self.__expected = expected

    def _hints(self) -> str:
        return self.__expected

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        char = stream.get(index)
        chars = [char] if self._matches(char) else []
        return Produce(chars, index)

    def _matches(self, char: Char) -> bool:
        if self.__expected:
            return char.value == self.__expected
        return True

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__expected})'


########################################################################
# SUBPARSER
########################################################################

class NotCharParser(CharParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = ValidProduce(index=index)
        char = stream.get(index)
        if self._matches(char):
            return Produce(index=index)
        return produce


class LowerParser(CharParser):
    def _hints(self) -> str:
        return LowerChar.CHARS

    def _matches(self, char: Char) -> bool:
        return char.is_lower()


class UpperParser(CharParser):
    def _hints(self) -> str:
        return UpperChar.CHARS

    def _matches(self, char: Char) -> bool:
        return char.is_upper()


class DigitParser(CharParser):
    def _hints(self) -> str:
        return DigitChar.CHARS

    def _matches(self, char: Char) -> bool:
        return char.is_digit()


class SpaceParser(CharParser):
    def _hints(self) -> str:
        return SpaceChar.CHARS

    def _matches(self, char: Char) -> bool:
        return char.is_space()


class NewlineParser(CharParser):
    def _hints(self) -> str:
        return NewlineChar.CHARS

    def _matches(self, char: Char) -> bool:
        return char.is_newline()


class AlphaNumParser(CharParser):
    def _hints(self) -> str:
        return (
            DigitChar.CHARS +
            LowerChar.CHARS +
            UpperChar.CHARS
        )

    def _matches(self, char: Char) -> bool:
        return char.is_digit() or \
               char.is_upper() or \
               char.is_lower()
