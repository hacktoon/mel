import re


class LexingError(Exception):
    def __init__(self, message, index):
        super().__init__(message)
        self.index = index


class ParsingError(Exception):
    def __init__(self, error, text):
        super().__init__(self._build_message(error, text))
        self.index = error.index

    def _build_message(self, error, text):
        lines = text.splitlines()
        
        return 'error'
