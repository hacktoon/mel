import string

from . import char
from .char import Char


class CharStream:
    def __init__(self, text=''):
        self._chars = CharList(text)
        self._index = 0

    def is_eof(self) -> bool:
        ch = self._chars.read(self._index)
        return isinstance(ch, char.EOFChar)

    def is_next(self, expected: Char) -> bool:
        ch = self._chars.read(self._index)
        return ch == expected


    #  read(Char('('))

    # def one_types(self, *types):
    #     # get one char of many types
    #     for type in types:
    #         char = self.one_type(type)
    #         if char is not None:
    #             return [char]
    #     return []

    # def one_many_types(self, *types):
    #     # get a list of chars of many types
    #     chars = []
    #     while True:
    #         char = self.one_types(*types)
    #         if not char:
    #             break
    #         chars.extend(char)
    #     return chars

    # def one_str(self, _str):
    #     # get one char equal to string
    #     if len(_str) > 1:
    #         raise ValueError('one char only')
    #     char = self._chars.read(self._index)
    #     if char.value == _str:
    #         self._index += 1
    #         return char
    #     return None


class CharList:
    def __init__(self, text):
        self._chars = self._build(text)

    def read(self, index):
        try:
            return self._chars[index]
        except IndexError:
            return char.EOFChar()

    def _build(self, text):
        line = column = 0
        chars = []
        _type_map = self._build_type_map()
        for char_str in text:
            type = _type_map.get(char_str, Char.OTHER)
            char = Char(char_str, type, line, column)
            chars.append(char)
            #  update line and columns for next char
            line = line + 1 if type == Char.NEWLINE else line
            column = 0 if type == Char.NEWLINE else column + 1
        return chars

    def _build_type_map(self):
        '''Build a {char_value: char_type} dict for each allowed char'''
        table = (
            (string.ascii_lowercase, Char.LOWER),
            (string.ascii_uppercase, Char.UPPER),
            (string.punctuation,     Char.SYMBOL),
            (string.digits,          Char.DIGIT),
            (' \r\t\b\a\v\f',        Char.SPACE),
            ('\n',                   Char.NEWLINE),
        )
        char_map = {}
        for chars, type in table:
            row_map = {char: type for char in chars}
            char_map.update(row_map)
        return char_map

    def __len__(self):
        return len(self._chars)
