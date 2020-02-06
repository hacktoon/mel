import re

from ..exceptions import ParsingError


class TextStream:
    def __init__(self, text=''):
        self.text = text
        self.index = 0
        self._index_cache = 0

    def save(self):
        self._index_cache = self.index
        return self.index

    def restore(self, _index):
        self.index = self._index_cache if _index is None else _index

    def read_pattern(self, string):
        match = re.match(string, self.head_text)
        if not match:
            raise ParsingError(f'Unrecognized pattern "{string}"')
        start, end = [offset + self.index for offset in match.span()]
        return self._read(match.group(0), (start, end))

    def read_string(self, string):
        if not self.head_text.startswith(string):
            raise ParsingError(f'Unrecognized string "{string}"')
        index = self.index, self.index + len(string)
        return self._read(string, index)

    def _read(self, string, index):
        self.index += len(string)
        return string, index

    def close(self):
        if not self.eof:
            raise ParsingError('Unexpected EOF')

    @property
    def head_text(self):
        return self.text[self.index:]

    @property
    def head_char(self):
        return self.head_text[0]

    @property
    def eof(self):
        return self.index >= len(self.text)
