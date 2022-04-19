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
        index = self.index + len(produce)
        return Produce(chars, index)

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
        produce = Produce(index=index)
        while subproduce := self.__parser.parse(index + 1, stream):
            produce += subproduce
        return produce


class OneManyParser(SingleRuleParser):
    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = self.__parser.parse(index, stream)
        new_index = index + produce.index
        while subproduce := self.__parser.parse(new_index, stream):
            produce += subproduce
            new_index += subproduce.index
        return produce


########################################################################
# MULTI RULE PARSER
########################################################################

class MultiRuleParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self._parsers = parsers

    def parse(self, index: int, stream: CharStream) -> Produce:
        raise NotImplementedError


class SeqParser(MultiRuleParser):
    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = Produce(index=index)
        for parser in self._parsers:
            subproduce = parser.parse(produce.index, stream)
            produce += subproduce
        return produce


class OneOfParser(MultiRuleParser):
    def parse(self, index: int, stream: CharStream) -> Produce:
        produce = Produce(index=index)
        for parser in self._parsers:
            if subproduce := parser.parse(index, stream):
                return produce + subproduce
        return produce


########################################################################
# BASE CHAR PARSER
########################################################################

class CharParser(Parser):
    def __init__(self, expected: str = ''):
        self._expected = expected

    def parse(self, index: int, stream: CharStream) -> Produce:
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
