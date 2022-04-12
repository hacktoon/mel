from .char import Char
from .stream import CharStream


'''
<NAME>
SeqParser(
    LowerParser(),
    ZeroManyParser(
        OneOfParser(
            Parser('_')
            LowerParser()
            DigitParser()
        )
    )
)
'''


class Produce:
    def __init__(self, index: int, chars: list[Char]):
        self.index = index
        self.chars = chars

    def append(self, produce):
        return self.chars.append(produce.chars)

    def line(self):
        if len(self.chars):
            return self.chars[0].line
        return -1

    def __bool__(self):
        return len(self.chars) > 0

    def __repr__(self):
        classname = self.__class__.__name__
        _str = [c.value for c in self.chars]
        return f'{classname}({"".join(_str)})'


########################################################################
# BASE PARSER
########################################################################

class Parser:
    def __init__(self, expected: str = None):
        self.expected = expected
        self.index = 0  # start parsing from here

    def parse(self, stream: CharStream) -> Produce:
        raise NotImplementedError


########################################################################
# PROCEDURE PARSERS
########################################################################

class SeqParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self.parsers = parsers

    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = Produce(index)
        for parser in self.parsers:
            produce.append(parser.parse(stream))
        return produce


class ZeroManyParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self.parsers = parsers

    def parse(self, stream: CharStream) -> Produce:
        produce = Produce()
        for parser in self.parsers:
            if subproduce := parser.parse():
                return subproduce
        return produce


class OneOfParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self.parsers = parsers

    def parse(self, stream: CharStream) -> Produce:
        produce = Produce()
        for parser in self.parsers:
            if subproduce := parser.parse():
                return subproduce
        return produce


########################################################################
# CHAR PARSERS
########################################################################

class CharParser:
    def __init__(self, index: int, expected: str = None):
        self.index = index
        self.expected = expected

    def parse(self, stream: CharStream) -> Produce:
        char = stream.get(self.index)
        chars = [char] if self._matches(char) else []
        return Produce(self.index, chars)

    def _matches(self, char: Char) -> bool:
        return char.value == self.expected


class LowerParser(CharParser):
    def _matches(self, char: Char) -> bool:
        return char.is_lower()


class UpperParser(CharParser):
    def _matches(self, char: Char) -> bool:
        return char.is_upper()


class DigitParser(CharParser):
    def _matches(self, char: Char) -> bool:
        return char.is_digit()


class SpaceParser(CharParser):
    def _matches(self, char: Char) -> bool:
        return char.is_space()


class NewlineParser(CharParser):
    def _matches(self, char: Char) -> bool:
        return char.is_newline()
