import re

from ..exceptions import ParsingError


class Stream:
    def __init__(self, text=''):
        self.text = text
        self.index = 0
        self._index_cache = 0

    def save(self):
        self._index_cache = self.index
        return self.index

    def restore(self, _index):
        self.index = self._index_cache if _index is None else _index

    def read_pattern(self, pattern_string):
        match = re.match(pattern_string, self.text[self.index:])
        if not match:
            raise ParsingError
        start, end = [offset + self.index for offset in match.span()]
        return self._read(match.group(0), (start, end))

    def read_string(self, string):
        text = self.text[self.index:]
        if not text.startswith(string):
            raise ParsingError
        index = self.index, self.index + len(string)
        return self._read(string, index)

    def _read(self, string, index):
        self.index += len(string)
        return string, index

    def close(self):
        if self.index < len(self.text):
            raise ParsingError('Unexpected EOF')
