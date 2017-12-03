import re


class LexingError(Exception):
    def __init__(self, message, index):
        super().__init__(message)
        self.index = index


class ParsingError(Exception):
    def __init__(self, message):
        super().__init__(message)
