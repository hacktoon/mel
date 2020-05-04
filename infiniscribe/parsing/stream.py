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

EOF_VALUE = '\0'


class Stream:
    def __init__(self, text=''):
        self._type_map = create_type_map()
        self.skip_types = [SPACE]
        self.text = text
        self.index = 0
        self.line = 0
        self.column = 0

    def __len__(self):
        return len(self.text)

    def read(self, expected_type=None):
        value, type = self._peek()
        if expected_type is not None and type != expected_type:
            return None
        char = self._build_char(type, value)
        self.forward(type)
        return char

    def _peek(self, offset=0):
        index = self.index + offset
        value = self._peek_value(offset)
        type = self._type_map.get(value, OTHER)
        return value, type

    def _peek_value(self, offset=0):
        index = self.index + offset
        return EOF_VALUE if self.eof else self.text[index]

    def _build_char(self, type, value):
        return Char(self.index, self.line, self.column, type, value)

    def forward(self, type):
        if self.eof:
            return
        self.index += 1
        if type == NEWLINE:
            self.line += 1
            self.column = 0
        else:
            self.column += 1

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

    def read_string(self, text):
        cache_index = self.index
        chars = []
        for expected_char in enumerate(text):
            value, type = self.read()
            if value != expected_char:
                return []
            char = self._build_next_char(type, value)
            chars.append(char)
        return chars

    @property
    def eof(self):
        return self.index >= len(self.text)


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

    def is_eof(self):
        return self.type == EOF


@functools.lru_cache(maxsize=1)
def create_type_map():
    '''Build a dict {char: type} from constants'''
    table = (
        (string.digits,          DIGIT),
        (string.ascii_lowercase, LOWER),
        (string.ascii_uppercase, UPPER),
        (string.punctuation,     SYMBOL),
        (' \t\x0b\x0c',          SPACE),
        ('\n',                   NEWLINE),
        (EOF_VALUE,              EOF)
    )
    char_map = {}
    for chars, type in table:
        row_map = {char: type for char in chars}
        char_map.update(row_map)
    return char_map
