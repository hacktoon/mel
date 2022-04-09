from ..scanning.char import Char
from ..scanning.stream import CharStream


'''
<NAME>
seq(
    lower(),
    zero_many(
        one_of(
            symbol('_')
            lower()
            digit()
        )
    )
)
'''


class CharProduce:
    def __init__(self, chars: list[Char] = None):
        self.chars = chars or []

    def __bool__(self):
        return len(self.chars)

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname}({"".join(self.chars)})'


class CharParser:
    def __init__(self, expected: str = None):
        self.expected = expected

    def parse(self, stream: CharStream) -> CharProduce:
        matched = self.__matches(stream.peek())
        chars = [stream.read()] if matched else []
        return CharProduce(chars)

    def __matches(self, char: Char) -> bool:
        raise NotImplementedError


class LowerParser(CharParser):
    def __matches(self, char: Char) -> bool:
        return char.is_lower()


class SymbolParser(CharParser):
    def __matches(self, char: Char) -> bool:
        return char.is_symbol()


def seq(*parsers: list[CharParser]) -> CharParser:
    produce = []
    for parser in parsers:
        produce.append(parser.parse())
    return produce
