from ..scanning import Char
from ..scanning.stream import CharStream
from .token import Token


'''
<NAME>
seq(
    lower(),
    zero_many(
        any(
            char('_')
            lower()
            digit()
        )
    )
)
'''


class TokenParser:
    def __init__(self):
        pass


class SymbolParser(TokenParser):
    def parse(self, stream: CharStream) -> Token:
        next_char = stream.peek()
        return Token()


def char():
    return SymbolParser('@')
