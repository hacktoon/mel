import string
from dataclasses import dataclass


DIGIT = 1
LOWER = 2
UPPER = 3
SYMBOL = 4
SPACE = 5
NEWLINE = 6
OTHER = 7
EOF = 8


class Stream:
    def __init__(self, text='', config={}):
        # TODO: should update the map with provided separator chars
        self.chars = CharStream(text)
        self.index = 0

    def read(self, expected_type=None):
        char = self.chars.read(self.index)
        if expected_type is not None and char.type != expected_type:
            return None
        self.index += 1
        return char

    def read_one(self, *types):
        for type in types:
            char = self.read(type)
            if char is not None:
                return [char]
        return []

    def read_many(self, *types):
        chars = []
        while True:
            char = self.read_one(*types)
            if not char:
                break
            chars.extend(char)
        return chars

    @property
    def eof(self):
        return self.chars.read(self.index).type == EOF


class TokenStream:
    def __init__(self, chars):
        self.chars = chars
        self.tokens = self._build()
        self.index = 0

    def _build(self):
        return []

    def read(self):
        char = self.tokens.read(self.index)
        self.index += 1
        return char

    @property
    def eof(self):
        return self.chars.read(self.index).type == EOF


class CharStream:
    def __init__(self, text):
        # TODO: should update the map with provided separator chars
        self.type_map = self._build_type_map()
        self.chars = self._build(text)

    def read(self, index):
        try:
            return self.chars[index]
        except IndexError:
            return Char('\0', EOF, -1, -1)

    def _build(self, text):
        line = col = 0
        chars = []
        for value in text:
            type = self.type_map.get(value, OTHER)
            chars.append(Char(value, type, line, col))
            line = line + 1 if type == NEWLINE else line
            col = 0 if type == NEWLINE else col + 1
        return chars

    def _build_type_map(self, extra_space=''):
        '''Build a {char_value: char_type} dict for each allowed char'''
        table = (
            (string.ascii_lowercase, LOWER),
            (string.ascii_uppercase, UPPER),
            (string.punctuation,     SYMBOL),
            (string.digits,          DIGIT),
            (' \r\t\b\a\v\f',        SPACE),
            ('\n',                   NEWLINE),
        )
        char_map = {}
        for chars, type in table:
            row_map = {char: type for char in chars}
            char_map.update(row_map)
        return char_map

    def __len__(self):
        return len(self.chars)


@dataclass
class Char:
    value: str
    type: int
    line: int
    column: int
