import string
import functools
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
        self.chars = build_char_data(text)
        self.index = 0

    def __len__(self):
        return len(self.chars)

    def read(self, expected_type=None):
        char = self.char_at(self.index)
        if expected_type is not None and char.type != expected_type:
            return None
        self.index += 1
        return char

    def char_at(self, index=0):
        if self.eof:
            return Char('\0', EOF, -1, -1)
        return self.chars[index]

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
        return self.index >= len(self.chars)


@dataclass
class Char:
    value: str
    type: int
    line: int
    column: int

    def is_digit(self):
        return self.type == DIGIT

    def is_lower(self):
        return self.type == LOWER

    def is_upper(self):
        return self.type == UPPER

    def is_symbol(self):
        return self.type == SYMBOL

    def is_space(self):
        return self.type == SPACE

    def is_newline(self):
        return self.type == NEWLINE

    def is_other(self):
        return self.type == OTHER

    def is_eof(self):
        return self.type == EOF


def build_char_data(text):
    line = col = 0
    type_map = build_type_map()
    chars = []
    for value in text:
        type = type_map.get(value, OTHER)
        chars.append(Char(value, type, line, col))
        line = line + 1 if type == NEWLINE else line
        col = 0 if type == NEWLINE else col + 1
    return chars


@functools.lru_cache(maxsize=1)
def build_type_map(extra_space=''):
    '''Build a dict {char: type} from constants'''
    table = (
        (string.ascii_lowercase, LOWER),
        (string.ascii_uppercase, UPPER),
        (string.punctuation,     SYMBOL),
        (string.digits,          DIGIT),
        (' \t\b\a\v\f',          SPACE),
        ('\r\n',                 NEWLINE),
    )
    char_map = {}
    for chars, type in table:
        row_map = {char: type for char in chars}
        char_map.update(row_map)
    return char_map
