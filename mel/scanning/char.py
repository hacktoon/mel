import string


class BaseChar:
    def __init__(self, value, line=-1, column=-1):
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'"{self.value}"'


class EOFChar(BaseChar):
    chars = [None]


class DigitChar(BaseChar):
    chars = string.digits


class LowerChar(BaseChar):
    chars = string.ascii_lowercase


class UpperChar(BaseChar):
    chars = string.ascii_uppercase


class SymbolChar(BaseChar):
    chars = string.punctuation


class SpaceChar(BaseChar):
    chars = ' \t\r\b\a\v\f'


class NewlineChar(BaseChar):
    chars = '\n'
