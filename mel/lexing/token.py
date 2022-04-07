from ..scanning import char


class Token:
    def __init__(self, id, chars):
        self.id = id
        self.chars = chars

    def __repr__(self):
        return ''.join(char.value for char in self.chars)

    def __bool__(self):
        return len(self.chars)


class IntToken:
    HINTS = char.DigitChar