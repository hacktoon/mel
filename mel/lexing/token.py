from ..scanning import char


class Token:
    def __init__(self, id, chars):
        self.id = id
        self.chars = chars

    def __repr__(self):
        classname = self.__class__.__name__
        value = ''.join(char.value for char in self.chars)
        return f'{classname}({value})'

    def __bool__(self):
        return len(self.chars)


class NullToken(Token):
    def __init__(self):
        super().__init__('null', None)

    def __bool__(self):
        return False


class IntToken:
    HINTS = char.DigitChar


class NameToken:
    HINTS = char.LowerChar
