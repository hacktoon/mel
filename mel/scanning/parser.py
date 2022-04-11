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

    def __bool__(self):
        return len(self.chars)

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname}({"".join(self.chars)})'


class Parser:
    def __init__(self, expected: str = None):
        self.expected = expected

    def parse(self, stream: CharStream) -> Produce:
        matched = self.__matches(stream.peek())
        chars = [stream.read()] if matched else []
        return Produce(chars)

    def __matches(self, char: Char) -> bool:
        raise char.value == self.expected


########################################################################
# PROCEDURE PARSERS
########################################################################

class ZeroManyParser(Parser):
    def parse(self, *parsers: list[Parser]) -> Produce:
        return


class OneOfParser(Parser):
    def __matches(self, char: Char) -> bool:
        return

    def parse(self, *parsers: list[Parser]) -> Produce:
        return


class SeqParser(Parser):
    def parse(self, *parsers: list[Parser]) -> Produce:
        produce = []
        for parser in parsers:
            produce.append(parser.parse())
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
