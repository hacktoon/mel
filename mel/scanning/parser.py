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
    def __init__(self, chars: list[Char] = None):
        self.chars = chars or []

    def append(self, produce):
        return self.chars.append(produce.chars)

    def line(self):
        if len(self.chars):
            return self.chars[0].line
        return -1

    def __bool__(self):
        return len(self.chars)

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname}({"".join(self.chars)})'


########################################################################
# BASE PARSER
########################################################################

class Parser:
    def __init__(self, expected: str = None):
        self.expected = expected
        self.index = 0  # start parsing from here

    def parse(self, stream: CharStream) -> Produce:
        matched = self.__matches(stream.peek())
        chars = [stream.read()] if matched else []
        return Produce(chars)

    def __matches(self, char: Char) -> bool:
        return char.value == self.expected


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
# SUB PARSERS
########################################################################

class LowerParser(Parser):
    def __matches(self, char: Char) -> bool:
        return char.is_lower()


class UpperParser(Parser):
    def __matches(self, char: Char) -> bool:
        return char.is_upper()


class DigitParser(Parser):
    def __matches(self, char: Char) -> bool:
        return char.is_digit()


class SymbolParser(Parser):
    def __matches(self, char: Char) -> bool:
        return char.is_symbol()
