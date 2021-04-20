from dataclasses import dataclass


@dataclass
class Char:
    EOF = None
    DIGIT = 1
    LOWER = 2
    UPPER = 3
    SYMBOL = 4
    SPACE = 5
    NEWLINE = 6
    OTHER = 7

    value: str
    type: int
    line: int
    column: int
