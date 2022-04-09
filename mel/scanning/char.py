import string


type_map = {}


def _register_char(cls):
    '''Build a {char_str: char_type} dict for chars'''
    sub_map = {char: cls for char in cls.CHARS}
    type_map.update(sub_map)
    return cls


class Char:
    CHARS = ''
    SKIP = False

    @staticmethod
    def build(ch: str = None, line: int = 0, column: int = 0):
        # any char not mapped will be a generic Char
        _Char = type_map.get(ch, Char)
        return _Char(ch, line, column)

    def __init__(
        self,
        value: str = '',
        line: int = -1,
        column: int = -1
    ):
        self.value = value
        self.line = line
        self.column = column

    def is_eof(self) -> bool:
        return isinstance(self, EOFChar)

    def is_digit(self) -> bool:
        return isinstance(self, DigitChar)

    def is_lower(self) -> bool:
        return isinstance(self, LowerChar)

    def is_upper(self) -> bool:
        return isinstance(self, UpperChar)

    def is_symbol(self) -> bool:
        return isinstance(self, SymbolChar)

    def is_newline(self) -> bool:
        return isinstance(self, NewlineChar)

    def is_space(self) -> bool:
        return isinstance(self, SpaceChar)

    def is_other(self) -> bool:
        return isinstance(self, Char)

    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({self.value or ''})"


class EOFChar(Char):
    pass


@_register_char
class DigitChar(Char):
    CHARS = string.digits


@_register_char
class LowerChar(Char):
    CHARS = string.ascii_lowercase


@_register_char
class UpperChar(Char):
    CHARS = string.ascii_uppercase


@_register_char
class SymbolChar(Char):
    CHARS = string.punctuation


@_register_char
class SpaceChar(Char):
    CHARS = ' \t\r\b\a\v\f'
    SKIP = True


@_register_char
class NewlineChar(Char):
    CHARS = '\n'
    SKIP = True
