from .char import Char
from .stream import CharStream


'''
<NAME>
SeqParser(
    LowerParser(),
    ZeroManyParser(
        OneOfParser(
            CharParser('_')
            LowerParser()
            DigitParser()
        )
    )
)
'''


class Produce:
    def __init__(self, chars: list[Char] = None, index: int = 0):
        self.chars = chars or []
        self.index = index

    def line(self):
        if len(self.chars):
            return self.chars[0].line
        return -1

    def __add__(self, produce):
        chars = self.chars + produce.chars
        return Produce(chars, self.index)

    def __iadd__(self, produce):
        return self + produce

    def __bool__(self):
        return len(self.chars) > 0

    def __len__(self):
        return len(self.chars)

    def __str__(self):
        return "".join(char.value for char in self.chars)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'


########################################################################
# BASE PARSER
########################################################################

class Parser:
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        raise NotImplementedError


########################################################################
# SINGLE RULE PARSER
########################################################################

class SingleRuleParser(Parser):
    def __init__(self, parser: Parser):
        self._parser = parser


class ZeroManyParser(SingleRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = Produce(index=index)
        while subproduce := self.__parser.parse(stream, index):
            produce += subproduce
        return produce


class OneManyParser(SingleRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = self.__parser.parse(stream, index)
        while subproduce := self.__parser.parse(stream, index):
            produce += subproduce
        return produce


########################################################################
# MULTI RULE PARSER
########################################################################

class MultiRuleParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self._parsers = parsers

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        raise NotImplementedError


class SeqParser(MultiRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = Produce(index=index)
        current_index = index
        for parser in self._parsers:
            if subproduce := parser.parse(stream, current_index):
                produce += subproduce
                current_index += 1
            else:
                return Produce(index=index)
        return produce


class OneOfParser(MultiRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = Produce(index=index)
        for parser in self._parsers:
            if subproduce := parser.parse(stream, index):
                return produce + subproduce
        return produce


########################################################################
# BASE CHAR PARSER
########################################################################

class CharParser(Parser):
    def __init__(self, expected: str = ''):
        self._expected = expected

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        char = stream.get(index)
        chars = [char] if self._matches(char) else []
        return Produce(chars, index)

    def _matches(self, char: Char) -> bool:
        return char.value == self._expected

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._expected})'


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
