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


def parse(text):
    char_type_map = _type_map()
    index = line = column = 0
    for char in text:
        type = char_type_map.get(char, OTHER)
        yield _Char(index, line, column, type)
        index, line, column = _char_position(type, index, line, column)


# PRIVATE DEFINITIONS =======================

@functools.lru_cache(maxsize=1)
def _type_map():
    '''Build a map from char to type'''
    table = (
        (string.digits, DIGIT),
        (string.ascii_lowercase, LOWER),
        (string.ascii_uppercase, UPPER),
        (string.punctuation, SYMBOL),
        (' \t\x0b\x0c', SPACE),
        ('\n', NEWLINE),
        ('\r', OTHER),
    )
    char_map = {}
    for chars, type in table:
        map_for_type = {char: type for char in chars}
        char_map.update(map_for_type)
    return char_map


def _char_position(type, index, line, column):
    index += 1
    if type == NEWLINE:
        return index, line + 1, 0
    return index, line, column + 1


@dataclass
class _Char:
    index: int
    line: int
    column: int
    type: int