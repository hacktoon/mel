from .char import Char


class Produce:
    def __init__(self, chars: list[Char] = None, index: int = 0):
        self.chars = chars or []
        self.index = index

    def line(self):
        return self.chars[0].line if len(self.chars) else -1

    def column(self):
        return self.chars[0].column if len(self.chars) else -1

    def __add__(self, produce):
        chars = self.chars + produce.chars
        return self.__class__(chars, self.index)

    def __iadd__(self, produce):
        return self + produce

    def __bool__(self):
        return len(self.chars) > 0

    def __len__(self):
        return len(self.chars)

    def __str__(self):
        return "".join(char.value for char in self.chars)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'


class ValidProduce(Produce):
    def __bool__(self):
        return True
