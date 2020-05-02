import string
import functools
from dataclasses import dataclass


# PUBLIC DEFINITIONS =======================

DIGIT = 1
LOWER = 2
UPPER = 3
SYMBOL = 4
SPACE = 5
NEWLINE = 6
OTHER = 7


class CharStream:
    def __init__(self, text=''):
        self.text = text.rstrip()
        self._stream = char_generator(self.text)

    def read(self):
        char = next(self._stream)
        return char

    def read_spaces(self):
        char = next(self._stream)
        return self.text[char.index]


def char_generator(text):
    char_type_map = _type_map()
    index = line = column = 0
    for char in text:
        type = char_type_map.get(char, OTHER)
        yield Char(index, line, column, type, char)
        index, line, column = _update_position(type, index, line, column)


@dataclass
class Char:
    index: int
    line: int
    column: int
    type: int
    value: str

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


# PRIVATE DEFINITIONS =======================

@functools.lru_cache(maxsize=1)
def _type_map():
    '''Build a dict {char: type} from constants'''
    table = (
        (string.digits, DIGIT),
        (string.ascii_lowercase, LOWER),
        (string.ascii_uppercase, UPPER),
        (string.punctuation, SYMBOL),
        (' \t\x0b\x0c', SPACE),
        ('\n', NEWLINE)
    )
    char_map = {}
    for chars, type in table:
        row_map = {char: type for char in chars}
        char_map.update(row_map)
    return char_map


def _update_position(type, index, line, column):
    '''Return updated position markers depending on char's type'''
    index += 1
    if type == NEWLINE:
        return index, line + 1, 0
    return index, line, column + 1
