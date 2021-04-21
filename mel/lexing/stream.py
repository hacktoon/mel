import string

from .char import Char


class CharStream:
    def __init__(self, text='', config={}):
        # TODO: should update the map with provided separator chars
        self._chars = TextStream(text)
        self._index = 0

    def one_types(self, *types):
        # get one char of many types
        for type in types:
            char = self.one_type(type)
            if char is not None:
                return [char]
        return []

    def one_many_types(self, *types):
        # get a list of chars of many types
        chars = []
        while True:
            char = self.one_types(*types)
            if not char:
                break
            chars.extend(char)
        return chars

    def one_str(self, _str):
        # get one char equal to string
        if len(_str) > 1:
            raise ValueError('one char only')
        char = self._chars.read(self._index)
        if char.value == _str:
            self._index += 1
            return char
        return None

    def one_type(self, type=None):
        # get one char of type
        char = self._chars.read(self._index)
        if type is not None and char.type != type:
            return None
        self._index += 1
        return char

    @property
    def eof(self):
        return self._chars.read(self._index).type == Char.EOF


class TextStream:
    def __init__(self, text):
        # TODO: should update the map with provided separator chars
        self.type_map = self._build_type_map()
        self.chars = self._build(text)

    def read(self, index):
        try:
            return self.chars[index]
        except IndexError:
            return Char('', Char.EOF, -1, -1)

    def _build(self, text):
        line = col = 0
        chars = []
        for value in text:
            type = self.type_map.get(value, Char.OTHER)
            char = Char(value, type, line, col)
            line = line + 1 if type == Char.NEWLINE else line
            col = 0 if type == Char.NEWLINE else col + 1
            chars.append(char)
        return chars

    def _build_type_map(self, extra_space=''):
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
        return len(self.chars)
