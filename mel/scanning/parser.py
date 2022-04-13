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
    def __init__(self, index: int, chars: list[Char] = None):
        self.index = index
        self.chars = chars or []

    def line(self):
        if len(self.chars):
            return self.chars[0].line
        return -1

    def __add__(self, produce):
        self.chars.append(produce.chars)

    def __iadd__(self, produce):
        self.chars.append(produce.chars)

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
    def parse(self, index: int, stream: CharStream) -> Produce:
        raise NotImplementedError


########################################################################
# SINGLE RULE PARSER
########################################################################

class SingleRuleParser(Parser):
    def __init__(self, parser: Parser):
        self._parser = parser


class ZeroManyParser(SingleRuleParser):
    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = Produce(index + 1)
        while subproduce := self.__parser.parse(index + 1, stream):
            produce += subproduce
        return produce


class OneManyParser(SingleRuleParser):
    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = self.__parser.parse(index + 1, stream)
        while subproduce := self.__parser.parse(index + 1, stream):
            produce += subproduce
        return produce


########################################################################
# MULTI RULE PARSER
########################################################################

class MultiRuleParser(Parser):
    def __init__(self, parsers: list[Parser]):
        self._parsers = parsers


class SeqParser(MultiRuleParser):
    def parse(self, stream: CharStream) -> Produce:
        produce = Produce(self._index)
        for parser in self._parsers:
            subproduce = parser.parse(stream)
            produce += subproduce
            self._index += 1
        return produce


class OneOfParser(MultiRuleParser):
    def parse(self, stream: CharStream) -> Produce:
        produce = Produce(self._index)
        for parser in self._parsers:
            if subproduce := parser.parse(stream):
                return produce + subproduce
        return produce


########################################################################
# BASE CHAR PARSER
########################################################################

class CharParser(Parser):
    def __init__(self, index: int, expected: str = None):
        self._index = index
        self._expected = expected

    def parse(self, stream: CharStream) -> Produce:
        char = stream.get(self._index)
        chars = [char] if self._matches(char) else []
        return Produce(self._index, chars)

    def _matches(self, char: Char) -> bool:
        return char.value == self._expected


########################################################################
# CHAR PARSER
########################################################################

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
