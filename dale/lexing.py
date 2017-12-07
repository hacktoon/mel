import re
from .types import tokens
from .types.errors import LexingError, ParsingError
from collections import namedtuple


Token = namedtuple('Token', 'id, value, line, column')


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._emit_token()
            tokens.append(token)
        return tokens

    def _emit_token(self):
        for id, regex in tokens.specs.items():
            match = regex.match(self.text, self.index)
            if not match:
                continue
            index, value = self.index, match.group(0)
            self._update_counters(value)
            return Token(id, value, self.line, self.column)
        else:
            raise LexingError('invalid syntax', self.index)

    def _update_counters(self, value):
        length = len(value)
        self.index += length
        newlines = re.findall(r'[\r\n]+', value)
        if newlines:
            self.line += len(newlines)
            self.column = 0
        else:
            self.column += length


class TokenStream:
    def __init__(self, text):
        self.tokens = Lexer(text).tokenize()
        self.index = 0

    def read(self, token_id=None, value=None):
        token = self.current()
        if token_id is None:
            self.index += 1
            return token
        if self.is_current(token_id):
            if value:
                if value == token.value:
                    self.index += 1
                    return token
            else:
                self.index += 1
                return token

        template = 'expected a token of type {!r}, but found {!r}'
        message = template.format(token_id, token.id)
        raise ParsingError(message)

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        return self.current().id == token_id

    def is_next(self, token_id):
        return self.current(offset=1).id == token_id

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return Token('eof', '', -1, -1)
