import string


class BaseChar:
    CHARS = ''

    def __init__(self, value=None, line: int = -1, column: int = -1):
        self.value = self.__parse_value(value)
        self.line = line
        self.column = column

    def __parse_value(self, value) -> None | str:
        if value is not None and value in self.CHARS:
            return value
        return None

    def __eq__(self, other):
        eq_type = self.__class__.__name__ == other.__class__.__name__
        if self.value is not None and other.value is not None:
            return eq_type and self.value == other.value
        return eq_type

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}('{self.value}')"


class EOFChar(BaseChar):
    pass


class DigitChar(BaseChar):
    CHARS = string.digits


class LowerChar(BaseChar):
    CHARS = string.ascii_lowercase


class UpperChar(BaseChar):
    CHARS = string.ascii_uppercase


class SymbolChar(BaseChar):
    CHARS = string.punctuation


class SpaceChar(BaseChar):
    CHARS = ' \t\r\b\a\v\f'


class NewlineChar(BaseChar):
    CHARS = '\n'
