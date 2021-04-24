
class Char:
    EOF = None
    DIGIT = 1
    LOWER = 2
    UPPER = 3
    SYMBOL = 4
    SPACE = 5
    NEWLINE = 6
    OTHER = 7

    def __init__(self, value, type, line=-1, column=-1):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

    def __repr__(self):
        return f'"{self.value}"'
