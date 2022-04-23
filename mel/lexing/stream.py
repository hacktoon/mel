# from ..scanning.char import Char
from ..scanning.stream import CharStream
from .token import Token, EOFToken


class TokenStream:
    def __init__(self, text: str = ''):
        self._tokens = self.__build(text)

    def get(self, index: int = 0) -> Token:
        if index < len(self._tokens):
            return self._tokens[index]
        return EOFToken()

    def __build(self, text: str) -> list[Token]:
        char_stream = CharStream(text)  # noqa
        index = 0
        char = char_stream.get(index)
        parsers = Token.parsers(char)
        parsers.parse(char_stream)

    def __len__(self):
        return len(self._tokens)
