from .char import Char, EOFChar


class CharStream:
    def __init__(self, text: str = ''):
        self._chars = self.__build(text)
        self._index = 0

    def peek(self) -> Char:
        if self._index < len(self._chars):
            return self._chars[self._index]
        return EOFChar()

    def read(self) -> Char:
        char = self.peek()
        self._index += 1
        return char

    def __build(self, text: str) -> list[Char]:
        line = column = 0
        chars = []
        for str_char in text:
            char = Char.build(str_char, line, column)
            chars.append(char)
            #  update line and columns for next char
            is_newline = char.is_newline()
            line = line + 1 if is_newline else line
            column = 0 if is_newline else column + 1
        return chars

    def __len__(self):
        return len(self._chars)
